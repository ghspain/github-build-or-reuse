#!/usr/bin/env python3
"""Generate the README demo assets from one auditable evidence snapshot."""
from __future__ import annotations

import argparse
import html
import json
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE, SVG, CAST = ROOT / "assets/demo.json", ROOT / "assets/demo.svg", ROOT / "assets/demo.cast"
ALLOWED_VERDICTS = {"USE", "CONTRIBUTE", "FORK", "BUILD"}


def load_demo():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    required = {"schema_version", "request", "checked_at", "candidate", "verdict", "confidence", "reason", "next_action", "note"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError("demo.json missing fields: " + ", ".join(missing))
    candidate = data["candidate"]
    for key in ("repository", "url", "license", "last_push", "verified_fit", "display_fit", "evidence"):
        if key not in candidate:
            raise ValueError(f"demo.json candidate missing field: {key}")
    if data["verdict"] not in ALLOWED_VERDICTS:
        raise ValueError(f"unsupported verdict: {data['verdict']}")
    if not candidate["verified_fit"]:
        raise ValueError("demo candidate must contain verified_fit evidence")
    return data


def xml(value):
    return html.escape(str(value), quote=True)


def render_cast(data):
    candidate = data["candidate"]
    fit = candidate["display_fit"]
    events = [
        (0.2, f"$ Ask: {data['request']}\r\n"),
        (1.0, "\r\n[FRAME] self-hosted · editable PPTX · multiple LLM providers · API\r\n"),
        (1.8, "[DISCOVER] searching GitHub by concept, synonyms and adjacent projects...\r\n"),
        (2.8, f"[VERIFY] {candidate['repository']} | {candidate['license']} | last push {candidate['last_push']}\r\n"),
        (3.8, f"[FIT] {fit}\r\n"),
        (5.0, f"\r\nVERDICT: {data['verdict']} ({data['confidence']})\r\n"),
        (5.5, f"{data['reason']}\r\n"),
        (6.2, f"Next action: {data['next_action']}\r\n"),
        (7.2, f"\r\n# Evidence snapshot checked {data['checked_at']}; not a benchmark or permanent endorsement.\r\n"),
    ]
    header = {
        "version": 2,
        "width": 120,
        "height": 26,
        "timestamp": 1788291000,
        "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"},
    }
    return "\n".join(
        [json.dumps(header, separators=(",", ":"))]
        + [json.dumps([time, "o", output], ensure_ascii=False, separators=(",", ":")) for time, output in events]
    ) + "\n"


def render_svg(data):
    candidate = data["candidate"]
    request_lines = textwrap.wrap(data["request"], width=86)
    reason_lines = textwrap.wrap(data["reason"], width=90)
    next_lines = textwrap.wrap(data["next_action"], width=91)
    rows = [
        ("01", "FRAME", "self-hosted · editable PPTX · multiple LLM providers · API", "#d2a8ff"),
        ("02", "DISCOVER", "concept search · synonyms · adjacent projects", "#79c0ff"),
        ("03", "VERIFY", f"{candidate['repository']} · {candidate['license']} · pushed {candidate['last_push']}", "#ffa657"),
        ("04", "FIT", candidate["display_fit"], "#a5d6ff"),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="0 0 1200 650" role="img" aria-labelledby="title desc">',
        '  <title id="title">GitHub Build or Reuse real evidence demo</title>',
        f'  <desc id="desc">Evidence snapshot checked {xml(data["checked_at"])} showing a {xml(data["verdict"])} verdict for {xml(candidate["repository"])}.</desc>',
        '  <rect width="1200" height="650" rx="24" fill="#0d1117"/>',
        '  <rect x="0" y="0" width="1200" height="54" rx="24" fill="#161b22"/>',
        '  <circle cx="30" cy="27" r="7" fill="#ff7b72"/><circle cx="54" cy="27" r="7" fill="#d29922"/><circle cx="78" cy="27" r="7" fill="#3fb950"/>',
        f'  <text x="600" y="34" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="17" fill="#8b949e">real public-repository evidence · checked {xml(data["checked_at"])}</text>',
        '  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="20">',
    ]
    y = 96
    out.append(f'    <text x="42" y="{y}" fill="#58a6ff">❯</text>')
    for index, line in enumerate(request_lines):
        out.append(f'    <text x="76" y="{y + index * 28}" fill="#f0f6fc">{xml(line)}</text>')
    y += len(request_lines) * 28 + 28
    for number, label, detail, color in rows:
        out += [
            f'    <text x="42" y="{y}" fill="#8b949e">{number}</text>',
            f'    <text x="86" y="{y}" fill="{color}" font-weight="700">{label}</text>',
            f'    <text x="220" y="{y}" fill="#c9d1d9">{xml(detail)}</text>',
        ]
        y += 43
    box_y = y + 3
    out.append(f'    <rect x="38" y="{box_y}" width="1124" height="162" rx="14" fill="#161b22" stroke="#30363d"/>')
    text_y = box_y + 38
    out.append(f'    <text x="65" y="{text_y}" fill="#3fb950" font-weight="800">VERDICT: {xml(data["verdict"])} · {xml(data["confidence"])}</text>')
    text_y += 34
    for line in reason_lines:
        out.append(f'    <text x="65" y="{text_y}" fill="#f0f6fc">{xml(line)}</text>')
        text_y += 28
    for index, line in enumerate(next_lines):
        prefix = "Next → " if index == 0 else "       "
        out.append(f'    <text x="65" y="{text_y}" fill="#8b949e">{prefix}{xml(line)}</text>')
        text_y += 28
    out += [
        f'    <text x="42" y="620" fill="#8b949e">{xml(data["note"])}</text>',
        "  </g>",
        "</svg>",
        "",
    ]
    return "\n".join(out)


def check_or_write(path, expected, check):
    if check:
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual != expected:
            print(f"ERROR: {path.relative_to(ROOT)} is stale; run python scripts/generate_demo.py", file=sys.stderr)
            return False
        return True
    path.write_text(expected, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated assets differ from demo.json")
    args = parser.parse_args()
    try:
        data = load_demo()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: invalid demo source: {exc}", file=sys.stderr)
        raise SystemExit(1)
    ok = check_or_write(SVG, render_svg(data), args.check) & check_or_write(CAST, render_cast(data), args.check)
    if not ok:
        raise SystemExit(1)
    if args.check:
        print("OK: generated demo assets match assets/demo.json")


if __name__ == "__main__":
    main()
