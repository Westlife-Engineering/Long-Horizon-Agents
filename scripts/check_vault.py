"""Read-only structural/source checks for this vault.

Run from any directory: python scripts/check_vault.py
Use --allow-pending-index while newly read pages are awaiting shared integration.
No files are written. This does not establish scholarly correctness or UI rendering.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
import subprocess
from urllib.parse import unquote

import fitz


ROOT = Path(__file__).resolve().parent.parent
HISTORICAL_WITHDRAWN = {"wiki/foundations/Foundation.canvas"}
WIKILINK = re.compile(r"\[\[([^\]\n]+)\]\]")
HASH = re.compile(r"(?<![A-Za-z0-9])[0-9a-fA-F]{64}(?![A-Za-z0-9])")


def split_target(link: str) -> tuple[str, str]:
    target = link.replace("\\|", "|").split("|", 1)[0].strip()
    path, _, anchor = target.partition("#")
    return unquote(path), unquote(anchor)


def resolve(path: str, source: Path) -> Path:
    candidate = ROOT / path if path else source
    # Titles may contain periods, so test the actual path before adding .md.
    if not candidate.exists() and candidate.suffix.lower() not in {
        ".md", ".pdf", ".canvas", ".html", ".png", ".jpg", ".jpeg", ".svg", ".webp"
    }:
        candidate = Path(str(candidate) + ".md")
    return candidate


def metadata(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
    if not match:
        return {}, ""
    fm = match.group(1)
    fields = {m.group(1): m.group(2).strip().strip("\"'")
              for m in re.finditer(r"^([A-Za-z_][\w-]*):\s*([^\n]*)", fm, re.M)}
    return fields, fm


def heading_forms(text: str) -> set[str]:
    headings = set()
    for line in re.findall(r"^#{1,6}[ \t]+(.+)$", text, re.M):
        raw = re.sub(r"[ \t]+#+[ \t]*$", "", line).strip()
        headings.add(raw)
        plain = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", raw)
        plain = re.sub(r"[*_`]", "", plain)
        headings.add(plain)
    return headings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-pending-index", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    files = [ROOT / "AGENTS.md", *sorted((ROOT / "workflows").glob("*.md")),
             *sorted((ROOT / "wiki").rglob("*.md")), *sorted((ROOT / "maintenance").rglob("*.md"))]
    texts: dict[Path, str] = {}
    errors: list[dict] = []
    warnings: list[dict] = []
    historical: list[dict] = []
    hash_cache: dict[Path, str] = {}
    pdf_pages: dict[Path, int] = {}
    ids: dict[str, list[str]] = defaultdict(list)
    paper_hashes: list[dict] = []
    count = 0

    def issue(bucket: list, path: Path, kind: str, detail: str, line: int | None = None):
        record = {"file": str(path.relative_to(ROOT)).replace("\\", "/"),
                  "check": kind, "detail": detail}
        if line is not None:
            record["line"] = line
        bucket.append(record)

    def get_text(path: Path) -> str:
        if path not in texts:
            texts[path] = path.read_text(encoding="utf-8-sig")
        return texts[path]

    def get_hash(path: Path) -> str:
        if path not in hash_cache:
            h = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
            hash_cache[path] = h.hexdigest().upper()
        return hash_cache[path]

    manifests = [json.loads(p.read_text(encoding="utf-8"))
                 for p in sorted((ROOT / "maintenance/migrations").glob("*.json"))]
    migration = {"raw": [], "pages": [], "anchors": {}}
    for manifest in manifests:
        migration["raw"].extend(manifest.get("raw", []))
        migration["pages"].extend(manifest.get("pages", []))
        migration["anchors"].update(manifest.get("anchors", {}))
        if manifest.get("log_prefix"):
            prefix = manifest["log_prefix"]
            original = (ROOT / "wiki/log.md").read_bytes()[:prefix["bytes"]]
            if hashlib.sha256(original).hexdigest() != prefix["sha256"]:
                errors.append({"check": "historical_log_prefix_changed"})
    anchors = migration.get("anchors", {})
    old_paths = {row["old_path"]: row for row in migration["raw"]}
    old_paths.update({row["old_path"]: row for row in migration["pages"]})
    old_paths.update({row["old_path"][:-3]: row for row in migration["pages"]})

    for path in files:
        try:
            text = get_text(path)
        except (OSError, UnicodeError) as exc:
            issue(errors, path, "read", str(exc))
            continue
        # These checks concern the actual Markdown links, including examples.
        for line_num, line in enumerate(text.splitlines(), 1):
            for match in WIKILINK.finditer(line):
                count += 1
                link = match.group(1)
                if line.lstrip().startswith("|") and re.search(r"(?<!\\)\|", link):
                    issue(errors, path, "table_alias_escape", link, line_num)
                target, anchor = split_target(link)
                dest = resolve(target, path)
                try:
                    dest.resolve().relative_to(ROOT)
                except ValueError:
                    issue(errors, path, "outside_vault_link", target, line_num)
                    continue
                if not dest.exists():
                    if path == ROOT / "wiki/log.md" and (target in old_paths or target + "#" + anchor in anchors):
                        row = old_paths.get(target)
                        mapped = anchors.get(target + "#" + anchor)
                        if mapped:
                            replacement, replacement_anchor = split_target(mapped)
                            resolved = resolve(replacement, path)
                            if not resolved.exists() or (replacement_anchor and replacement_anchor not in heading_forms(get_text(resolved))):
                                issue(errors, path, "historical_mapping", mapped, line_num)
                            else:
                                issue(historical, path, "documented_heading_migration", target + "#" + anchor, line_num)
                        elif row and row["new_path"]:
                            resolved = ROOT / row["new_path"]
                            valid = resolved.exists() and (not target.startswith("raw/") or get_hash(resolved).lower() == row["sha256"].lower())
                            issue(historical if valid else errors, path, "documented_path_migration", target, line_num)
                        elif row and row.get("action") == "delete" and row.get("recovery_commit"):
                            try:
                                original = subprocess.check_output(["git", "show", row["recovery_commit"] + ":" + row["old_path"]], cwd=ROOT)
                                valid = hashlib.sha256(original).hexdigest().lower() == row["sha256"].lower()
                            except subprocess.CalledProcessError:
                                valid = False
                            issue(historical if valid else errors, path, "documented_auxiliary_deletion", target, line_num)
                        else:
                            issue(errors, path, "historical_mapping", target, line_num)
                    elif path == ROOT / "wiki/log.md" and target in HISTORICAL_WITHDRAWN:
                        issue(historical, path, "documented_withdrawal", target, line_num)
                    else:
                        issue(errors, path, "link_target", target, line_num)
                    continue
                try:
                    if anchor and dest.suffix.lower() == ".md":
                        dest_text = get_text(dest)
                        if anchor.startswith("^"):
                            valid = bool(re.search(r"\^" + re.escape(anchor[1:]) + r"\s*$", dest_text, re.M))
                        else:
                            valid = anchor in heading_forms(dest_text)
                        if not valid:
                            mapped = anchors.get(target + "#" + anchor) if path == ROOT / "wiki/log.md" else None
                            if mapped:
                                replacement, replacement_anchor = split_target(mapped)
                                resolved = resolve(replacement, path)
                                valid = resolved.exists() and (not replacement_anchor or replacement_anchor in heading_forms(get_text(resolved)))
                                issue(historical if valid else errors, path, "documented_heading_migration", mapped, line_num)
                            else:
                                issue(errors, path, "link_anchor", f"{target}#{anchor}", line_num)
                    if dest.suffix.lower() == ".pdf" and anchor:
                        page_match = re.search(r"(?:^|&)page=(\d+)(?:&|$)", anchor)
                        if page_match:
                            if dest not in pdf_pages:
                                with fitz.open(dest) as pdf:
                                    pdf_pages[dest] = len(pdf)
                            page = int(page_match.group(1))
                            if not 1 <= page <= pdf_pages[dest]:
                                issue(errors, path, "pdf_page", f"{target}: page {page}, length {pdf_pages[dest]}", line_num)
                except (OSError, ValueError, RuntimeError) as exc:
                    issue(errors, path, "linked_file_read", f"{target}: {exc}", line_num)

        fields, fm = metadata(text)
        if path.is_relative_to(ROOT / "wiki") and path not in {
            ROOT / "wiki/index.md", ROOT / "wiki/log.md"
        }:
            for field in ("type", "created", "updated", "sources"):
                if field not in fields:
                    issue(errors, path, "frontmatter", f"missing {field}")
            for field in ("created", "updated"):
                if field in fields:
                    try:
                        date.fromisoformat(fields[field])
                    except ValueError:
                        issue(errors, path, "frontmatter_date", f"{field}: {fields[field]}")
            if "sources" in fields and not re.search(r"^sources:\s*(?:\[|\n\s+-)", fm, re.M):
                issue(errors, path, "frontmatter_sources", "sources must be a list")

        if fields.get("type") in {"paper", "survey"}:
            sid = fields.get("source_id", "")
            if not sid:
                table_id = re.search(r"\|\s*来源\s*ID\s*\|\s*(S\d+)\s*\|", text, re.I)
                sid = table_id.group(1) if table_id else ""
            if not re.fullmatch(r"S\d+", sid):
                issue(errors, path, "source_id", "missing or invalid source ID")
            else:
                ids[sid].append(path.relative_to(ROOT).as_posix())

            registered = {m.group(0).upper() for m in HASH.finditer(text)}
            raw_paths = set()
            for link in WIKILINK.findall(text):
                target, _ = split_target(link)
                if target.startswith("raw/"):
                    dest = resolve(target, path)
                    if dest.is_file():
                        raw_paths.add(dest)
            actual = {get_hash(p): p for p in raw_paths}
            if not registered:
                issue(errors, path, "paper_hash", "no SHA-256 registered")
            for digest in sorted(registered):
                if digest not in actual:
                    issue(errors, path, "paper_hash", f"registered SHA-256 matches no linked Raw: {digest}")
                else:
                    paper_hashes.append({"paper": path.relative_to(ROOT).as_posix(),
                                         "raw": actual[digest].relative_to(ROOT).as_posix(),
                                         "sha256": digest})

    for sid, paths in ids.items():
        if len(paths) > 1:
            errors.append({"check": "duplicate_source_id", "source_id": sid, "files": paths})

    index_file = ROOT / "wiki/index.md"
    index_targets = {resolve(split_target(link)[0], index_file).resolve()
                     for link in WIKILINK.findall(get_text(index_file))}
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        if path in {index_file, ROOT / "wiki/log.md"}:
            continue
        if path.resolve() not in index_targets:
            issue(warnings if args.allow_pending_index else errors, path,
                  "index_coverage", "not linked from wiki/index.md")

    source_rows = {row["source_id"]: row for row in migration["pages"]}
    if not set(source_rows).issubset(ids):
        errors.append({"check": "source_id_set", "actual": sorted(ids), "expected": sorted(source_rows)})
    expected_raw = {row["new_path"] for row in migration["raw"] if row["new_path"]}
    current_sources = []
    for page in (ROOT / "wiki").rglob("*.md"):
        fields, _ = metadata(get_text(page))
        if fields.get("type") not in {"paper", "survey"}:
            continue
        current_sources.append(page)
        for link in WIKILINK.findall(get_text(page)):
            target, _ = split_target(link)
            if target.startswith("raw/") and resolve(target, page).is_file():
                expected_raw.add(resolve(target, page).relative_to(ROOT).as_posix())
        if fields["type"] == "paper":
            direction = fields.get("primary_direction", "")
            expected_page = ROOT / ("wiki/papers/" + direction + "/" + page.name)
            expected_pdf = ROOT / ("raw/papers/" + direction + "/" + page.stem + ".pdf")
            if not direction or page != expected_page or not expected_pdf.is_file():
                issue(errors, page, "primary_mirror", direction)
        elif page.parent != ROOT / "wiki/surveys":
            issue(errors, page, "survey_directory", str(page))
    actual_raw = {p.relative_to(ROOT).as_posix() for p in (ROOT / "raw").rglob("*") if p.is_file()}
    if expected_raw != actual_raw:
        errors.append({"check": "raw_inventory", "extra": sorted(actual_raw - expected_raw), "missing": sorted(expected_raw - actual_raw)})
    for row in migration["raw"]:
        if row["new_path"] and (not (ROOT / row["new_path"]).is_file() or get_hash(ROOT / row["new_path"]).lower() != row["sha256"].lower()):
            errors.append({"check": "manifest_hash", "path": row["new_path"]})
        if row["action"] == "delete":
            if (ROOT / row["old_path"]).exists():
                errors.append({"check": "deleted_auxiliary_still_present", "path": row["old_path"]})
            original = subprocess.check_output(["git", "show", row["recovery_commit"] + ":" + row["old_path"]], cwd=ROOT)
            if hashlib.sha256(original).hexdigest().lower() != row["sha256"].lower():
                errors.append({"check": "deletion_recovery_hash", "path": row["old_path"]})
    hashes = defaultdict(list)
    for row in migration["pages"]:
        page = ROOT / row["new_path"]
        fields, _ = metadata(get_text(page))
        hashes[row["sha256"]].append(row["source_id"])
        if row["primary_direction"]:
            direction = row["primary_direction"]
            expected_page = "wiki/papers/" + direction + "/" + page.name
            expected_pdf = "raw/papers/" + direction + "/" + page.stem + ".pdf"
            if fields.get("primary_direction") != direction or row["new_path"] != expected_page or row["raw_new"] != expected_pdf:
                errors.append({"check": "primary_mirror", "source_id": row["source_id"]})
            for related in [direction, *row["related_directions"]]:
                theme = ROOT / ("wiki/" + related + ".md")
                if not theme.exists() or row["new_path"][:-3] not in get_text(theme) or "wiki/" + related not in get_text(page):
                    errors.append({"check": "theme_backlink", "source_id": row["source_id"], "direction": related})
        elif fields.get("type") != "survey":
            errors.append({"check": "survey_type", "source_id": row["source_id"]})
    for digest, sources in hashes.items():
        if len(sources) > 1:
            errors.append({"check": "duplicate_main_pdf", "source_ids": sources})
    for tree in [ROOT / "raw", ROOT / "wiki", ROOT / "maintenance", ROOT / "scripts"]:
        for p in tree.rglob("*"):
            if p.is_symlink() or p.stat().st_file_attributes & 0x400:
                errors.append({"check": "reparse_point", "path": str(p)})
            if p.is_dir() and not any(p.iterdir()):
                errors.append({"check": "empty_directory", "path": str(p)})
    if (ROOT / "wiki/foundations/wiki").exists():
        errors.append({"check": "nested_wiki"})
    baseline_results = []
    for rel, expected in {row["new_path"]: row["sha256"].upper()
                          for row in migration["raw"] if row["new_path"]}.items():
        path = ROOT / rel
        actual = get_hash(path) if path.is_file() else None
        ok = actual == expected
        baseline_results.append({"raw": rel, "unchanged": ok})
        if not ok:
            issue(errors, path, "baseline_raw_integrity", f"expected {expected}; actual {actual}")

    result = {
        "scope": "structural checks only; no scholarly or Obsidian UI validation",
        "markdown_files": len(files), "wikilinks": count,
        "paper_pages": sum(len(v) for v in ids.values()),
        "pdfs_checked": len(pdf_pages),
        "registered_hashes_matched": len(paper_hashes),
        "raw_files": len(actual_raw),
        "source_pages": dict(Counter(metadata(get_text(page))[0].get("type")
                                     for page in current_sources)),
        "baseline_raw": {"checked": len(baseline_results),
                         "unchanged": sum(row["unchanged"] for row in baseline_results)},
        "allow_pending_index": args.allow_pending_index,
        "errors": errors, "warnings": warnings,
        "documented_historical_links": historical,
        "passed": not errors,
    }
    result["documented_historical_link_count"] = len(result.pop("documented_historical_links"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
