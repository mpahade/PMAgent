"""PM Sprint Status Agent - render step: injects reports.json + narratives.json into template.html.

Usage:
  python3 build.py template.html reports.json narratives.json out.html               # for a Claude artifact
  python3 build.py template.html reports.json narratives.json index.html --standalone # full page for GitHub Pages / any browser
"""
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
standalone = "--standalone" in sys.argv
tpl, reports, narr, out = args[:4]

s = open(tpl).read()
s = s.replace("/*__REPORTS__*/[]", json.dumps(json.load(open(reports))))
s = s.replace("/*__NARR__*/{}", json.dumps(json.load(open(narr))))

if standalone:
    # The artifact viewer adds the document skeleton itself; a plain browser needs it in the file.
    s = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
         "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
         "<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
         "</head>\n<body>\n" + s + "\n</body>\n</html>\n")

open(out, "w").write(s)
print("wrote", out, len(s), "bytes")
