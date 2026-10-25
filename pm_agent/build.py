"""PM Sprint Status Agent - render step: injects reports.json + narratives.json into template.html."""
import json, sys
tpl, reports, narr, out = sys.argv[1:5]
s = open(tpl).read()
s = s.replace("/*__REPORTS__*/[]", json.dumps(json.load(open(reports))))
s = s.replace("/*__NARR__*/{}", json.dumps(json.load(open(narr))))
open(out, "w").write(s)
print("wrote", out, len(s), "bytes")
