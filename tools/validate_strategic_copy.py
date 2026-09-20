#!/usr/bin/env python3
"""Flowmatic strategic-copy lint.

Profiles:
- strategic-report: pitch/IR/business-plan/report copy. Strict report style.
- public-web: public website strategic copy. Formal headings; CTA controls exempt.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

KO_HARD = [
    r"보여드(?:립니다|리겠습니다)",
    r"지금\s*작동",
    r"우리가\s*만들",
    r"\b우리가\b|\b저희\b|\b여러분\b|\b당신\b",
    r"있습니까\?|합니까\?|할까요\?|인가요\?|나요\?|까요\?",
    r"돈이\s*되는",
    r"먹(?:는다|고|어|습니다)",
    r"장악(?:한다|합니다|하고)",
    r"찌른(?:다|다\.|다\s)",
    r"갈아엎",
    r"경쟁사(?:가|는)?\s*잘",
]
KO_REPORT_BODY = [
    r"드립니다|보여드립니다|하겠습니다",
    r"\b우리가\b|\b저희\b|\b여러분\b|\b당신\b",
]
KO_HEADING = [
    r"보여드립니다",
    r"(?:합니다|됩니다|있습니다|입니다)\.?$",
    r"(?:습니까|나요|까요)\?$",
    r"\?$",
    r"돈이\s*되는",
    r"지금\s*작동",
    r"우리가\s*만들",
]
EN_HARD = [
    r"\bWhat works today\b",
    r"\bWhat we are building\b",
    r"\bWhere is .+\?",
]
EN_PUBLIC_BODY = [
    r"\bwe\b|\bour\b|\byou\b|\byour\b",
]
EN_REPORT_BODY = EN_PUBLIC_BODY
EN_HEADING = [
    r"^(?:See|Start|Prove|Show|Discover|Meet)\b",
    r"^(?:Where|What|Who)\b.*\?$",
    r"^Not another\b",
    r"\?$",
]
AR_HEADING = [
    r"؟$",
    r"^(?:شاهد|ابدأ|أثبت|أين)\b",
]

def visible_parts(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() not in {".html", ".htm"}:
        return [], [("document", text)]
    doc = BeautifulSoup(text, "html.parser")
    for tag in doc(["script", "style", "noscript"]):
        tag.decompose()
    heads = []
    for h in doc.find_all(re.compile(r"^h[1-6]$")):
        heads.append((h.name, " ".join(h.stripped_strings)))
    body = []
    # Controls are functional UI and are exempt from presentation-style lint.
    for node in doc.find_all(["p", "li", "td", "th", "strong", "span"]):
        if node.find_parent(["a", "button", "form"]):
            continue
        s = " ".join(node.stripped_strings)
        if s:
            body.append((node.name, s))
    return heads, body

def scan(patterns, parts, code):
    failures=[]
    for label, text in parts:
        for pat in patterns:
            if re.search(pat, text, flags=re.I):
                failures.append((code, label, pat, text[:240]))
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--profile", choices=("strategic-report","public-web"), required=True)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("files", nargs="*")
    args=ap.parse_args()

    if args.self_test:
        bad_head=[("h2","현재 작동하는 제품부터 보여드립니다.")]
        good_head=[("h2","현재 구현 범위 및 검증 자산")]
        assert scan(KO_HEADING,bad_head,"KO-HEAD")
        assert not scan(KO_HEADING,good_head,"KO-HEAD")
        assert scan(EN_HEADING,[("h2","See what works today.")],"EN-HEAD")
        assert not scan(EN_HEADING,[("h2","Current Implementation Scope & Validation Assets")],"EN-HEAD")
        print("PASS: strategic-copy linter self-test")
        if not args.files:
            return 0

    failures=[]
    for raw in args.files:
        path=Path(raw)
        if not path.exists():
            failures.append(("FILE","missing","",str(path)))
            continue
        heads,body=visible_parts(path)
        failures += [(str(path),*x) for x in scan(KO_HEADING,heads,"KO-HEAD")]
        failures += [(str(path),*x) for x in scan(EN_HEADING,heads,"EN-HEAD")]
        failures += [(str(path),*x) for x in scan(AR_HEADING,heads,"AR-HEAD")]
        failures += [(str(path),*x) for x in scan(KO_HARD,body,"KO-HARD")]
        failures += [(str(path),*x) for x in scan(EN_HARD,body,"EN-HARD")]
        failures += [(str(path),*x) for x in scan(EN_PUBLIC_BODY,body,"EN-PUBLIC")]
        if args.profile=="strategic-report":
            failures += [(str(path),*x) for x in scan(KO_REPORT_BODY,body,"KO-REPORT")]
            failures += [(str(path),*x) for x in scan(EN_REPORT_BODY,body,"EN-REPORT")]

    if failures:
        for f in failures:
            print("FAIL:", " | ".join(map(str,f)))
        print(f"Strategic copy QA: {len(failures)} failure(s)")
        return 1
    print("PASS: strategic copy QA")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
