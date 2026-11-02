"""30-second explainer of the PM agent eval method. Usage: python3 render.py [scene_index|all] [--still t]"""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + {"r": "Inter-Regular.otf", "m": "Inter-Medium.otf", "s": "Inter-SemiBold.otf",
                                               "b": "InterDisplay-Bold.otf", "x": "InterDisplay-ExtraBold.otf"}[w], s)
MONO = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", s)

BG = (245, 246, 244); SURF = (255, 255, 255); INK = (27, 35, 33); MUTED = (93, 106, 102); LINE = (221, 226, 223)
ACC = (15, 107, 99); ACC_S = (225, 239, 236); RED = (194, 59, 46); RED_S = (251, 233, 230)
AMB = (183, 116, 10); AMB_S = (253, 241, 220); GRN = (44, 122, 63); GRN_S = (228, 242, 230)
M = 140  # side margin

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def mix(c, a): return tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))

class Canvas:
    def __init__(s): s.im = Image.new("RGB", (W, H), BG); s.d = ImageDraw.Draw(s.im)
    def text(s, xy, txt, f, col, a=1.0, dy=0, anchor="la"):
        s.d.text((xy[0], xy[1] + dy), txt, font=f, fill=mix(col, a), anchor=anchor)
    def rect(s, box, col, a=1.0, r=14, outline=None):
        s.d.rounded_rectangle(box, r, fill=mix(col, a), outline=mix(outline, a) if outline else None, width=2)

def appear(t, start, dur=0.5): a = ease((t - start) / dur); return a, (1 - a) * 24

def header(c, t, eyebrow, title):
    a, dy = appear(t, 0.1)
    c.text((M, 110), eyebrow, MONO(26), MUTED, a, dy)
    a, dy = appear(t, 0.25)
    c.text((M, 150), title, font("x", 76), INK, a, dy)

def wrap(txt, f, width, d):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= width: line = t
        else: out.append(line); line = w
    return out + [line]

# ---------------- scenes ----------------
def s1(c, t):
    a, dy = appear(t, 0.15); c.text((M, 250), "PM SPRINT STATUS AGENT  ·  EVALUATION", MONO(28), ACC, a, dy)
    a, dy = appear(t, 0.35)
    c.text((M, 300), "How we judged the", font("x", 110), INK, a, dy)
    c.text((M, 425), "agent's weekly reports", font("x", 110), INK, a, dy)
    a, dy = appear(t, 0.8)
    c.text((M, 580), "6 reports  ·  Atlas demo project  ·  Sep 18 – Oct 23, 2026", font("m", 38), MUTED, a, dy)
    steps = ["Jira snapshots", "Agent's report", "Two-pass judge", "Score + fixes"]
    x = M
    for i, s in enumerate(steps):
        a, dy = appear(t, 1.4 + i * 0.45)
        f = font("s", 34); w = c.d.textlength(s, font=f) + 64
        hl = i == 2
        c.rect((x, 720 + dy, x + w, 810 + dy), ACC_S if hl else SURF, a, outline=ACC if hl else LINE)
        c.text((x + 32, 765 + dy), s, f, ACC if hl else INK, a, anchor="lm")
        x += w
        if i < len(steps) - 1:
            c.text((x + 22, 765), "→", font("s", 40), MUTED, a, anchor="lm"); x += 70

def s2(c, t):
    header(c, t, "STEP 1  ·  TWO INDEPENDENT PASSES", "Two passes, blind to each other")
    cards = [
        ("1", "Deterministic checks", "28", "number checks",
         "Recompute the ground truth from the Jira snapshots, then check every number in the report: points, %, days blocked, velocity."),
        ("2", "Blind LLM judge", "7", "weighted criteria",
         "A separate Claude Opus sees only facts known on the report date and labels each claim."),
    ]
    cw = (W - 2 * M - 60) // 2
    for i, (n, ttl, big, unit, body) in enumerate(cards):
        a, dy = appear(t, 0.7 + i * 0.6)
        x0 = M + i * (cw + 60); y0 = 330 + dy
        c.rect((x0, y0, x0 + cw, y0 + 620), SURF, a, outline=LINE)
        c.rect((x0 + 48, y0 + 48, x0 + 108, y0 + 108), ACC, a, r=30)
        c.text((x0 + 78, y0 + 78), n, font("b", 36), SURF, a, anchor="mm")
        c.text((x0 + 132, y0 + 78), ttl, font("b", 46), INK, a, anchor="lm")
        c.text((x0 + 48, y0 + 150), big, font("x", 120), ACC, a)
        bw = c.d.textlength(big, font=font("x", 120))
        c.text((x0 + 60 + bw, y0 + 222), unit, font("m", 36), MUTED, a)
        for j, ln in enumerate(wrap(body, font("r", 33), cw - 96, c.d)):
            c.text((x0 + 48, y0 + 320 + j * 46), ln, font("r", 33), INK, a)
        if i == 1:
            labels = [("Supported", GRN, GRN_S), ("Contradicted", RED, RED_S), ("Unsupported", AMB, AMB_S), ("Lookahead", AMB, AMB_S)]
            x, yc = x0 + 48, y0 + 492
            for k, (lb, fg, bgc) in enumerate(labels):
                a2, _ = appear(t, 2.2 + k * 0.25, 0.35); a2 *= a
                f = MONO(24); w = c.d.textlength(lb, font=f) + 32
                if x + w > x0 + cw - 48: x, yc = x0 + 48, yc + 60
                c.rect((x, yc - 24, x + w, yc + 24), bgc, a2, r=6)
                c.text((x + 16, yc), lb, f, fg, a2, anchor="lm"); x += w + 14

def s3(c, t):
    header(c, t, "STEP 2  ·  THE RUBRIC", "Seven criteria, weighted by impact")
    rows = [("Factual accuracy", 25), ("Risk coverage", 20), ("Grounding (as of report date)", 15), ("Actionability", 15),
            ("RAG calibration", 10), ("Clarity", 10), ("Internal consistency", 5)]
    y = 320; lx = M; bx = M + 640; bmax = W - M - bx - 120
    for i, (lb, w) in enumerate(rows):
        a, dy = appear(t, 0.6 + i * 0.22, 0.4)
        g = ease((t - 0.8 - i * 0.22) / 0.8)
        yy = y + i * 82
        c.text((lx, yy + 30), lb, font("m", 38), INK, a, anchor="lm")
        c.rect((bx, yy + 8, bx + bmax, yy + 52), LINE, a * 0.6, r=8)
        if g > 0: c.rect((bx, yy + 8, bx + max(16, bmax * (w / 25) * g), yy + 52), ACC if i < 3 else (76, 150, 140), a, r=8)
        c.text((bx + bmax + 24, yy + 30), f"{round(w * g)}%", font("b", 40), INK, a, anchor="lm")
    a, dy = appear(t, 3.4)
    c.rect((M, 930 + dy, W - M, 1010 + dy), ACC_S, a, r=10)
    c.text((M + 36, 970 + dy), "PASS = weighted score ≥ 4.0 and no contradicted claim     FAIL = below 3.0", font("s", 36), ACC, a, anchor="lm")

def s4(c, t):
    header(c, t, "STEP 3  ·  RESULTS", "")
    a, dy = appear(t, 0.25)
    c.text((M, 150), "Average", font("x", 76), INK, a, dy)
    n = ease((t - 0.4) / 1.2) * 3.88
    f = font("x", 76); x = M + c.d.textlength("Average ", font=f)
    c.text((x, 150), f"{n:.2f}", f, ACC, a, dy)
    c.text((x + c.d.textlength("3.88 ", font=f), 150), "/ 5", f, MUTED, a, dy)
    data = [("Sep 18", 3.10, AMB, "edits"), ("Sep 25", 2.85, RED, "fail"), ("Oct 2", 4.30, GRN, "pass"),
            ("Oct 9", 4.40, GRN, "pass"), ("Oct 16", 4.35, GRN, "pass"), ("Oct 23", 4.25, AMB, "edits")]
    x0, x1, yb, yt = M + 80, W - M - 330, 940, 330
    ys = lambda v: yb - (v / 5) * (yb - yt)
    for v in (0, 1, 2, 3, 4, 5):
        c.d.line((x0, ys(v), x1, ys(v)), fill=LINE, width=2)
        c.text((x0 - 24, ys(v)), str(v), MONO(26), MUTED, anchor="rm")
    slot = (x1 - x0) / 6; bw = slot * 0.56
    for i, (wk, v, col, vd) in enumerate(data):
        g = ease((t - 0.9 - i * 0.2) / 0.8)
        cx = x0 + slot * (i + 0.5)
        if g > 0:
            c.rect((cx - bw / 2, ys(v * g), cx + bw / 2, yb), col, 1, r=8)
            c.text((cx, ys(v * g) - 34), f"{v * g:.2f}", font("b", 36), INK, g, anchor="mm")
        c.text((cx, yb + 40), wk, font("m", 32), INK, anchor="mm")
    a, _ = appear(t, 2.4)
    c.d.line((x0, ys(4.0), x1, ys(4.0)), fill=mix(INK, a), width=4)
    c.text((x1 + 20, ys(4.0)), "pass ≥ 4.0", font("s", 30), INK, a, anchor="lm")
    leg = [("3 pass", GRN), ("2 pass with edits", AMB), ("1 fail", RED)]
    for k, (lb, col) in enumerate(leg):
        a, dy = appear(t, 3.0 + k * 0.25)
        y = 520 + k * 64 + dy
        c.rect((x1 + 22, y - 14, x1 + 50, y + 14), col, a, r=5)
        c.text((x1 + 66, y), lb, font("m", 32), INK, a, anchor="lm")
    a, dy = appear(t, 3.9)
    c.text((x1 + 22, 760 + dy), "24 of 28", font("b", 44), ACC, a)
    c.text((x1 + 22, 816 + dy), "number checks", font("m", 30), MUTED, a)
    c.text((x1 + 22, 854 + dy), "passed", font("m", 30), MUTED, a)

def s5(c, t):
    header(c, t, "STEP 4  ·  WHAT IT CAUGHT, WHAT TO FIX", "Right numbers, wrong timing")
    items = [(RED, "Lookahead", "Early reports used facts not yet on the board, like Sprint 41's plan."),
             (RED, "Plan breaks its own cap", "Oct 23 lists 28 pts of work under a 23-pt cap."),
             (AMB, "Missed release risk", "No link to the Nov 6 GA date before Oct 16.")]
    for i, (col, ttl, body) in enumerate(items):
        a, dy = appear(t, 0.6 + i * 0.4)
        y = 320 + i * 128 + dy
        c.rect((M, y, M + 12, y + 96), col, a, r=4)
        c.text((M + 40, y + 6), ttl, font("b", 42), INK, a)
        c.text((M + 40, y + 58), body, font("r", 32), MUTED, a)
    a, dy = appear(t, 2.4)
    y = 740 + dy
    c.rect((M, y, W - M, y + 230), ACC, a, r=14)
    c.text((M + 48, y + 44), "NEXT", MONO(26), (190, 225, 220), a)
    c.text((M + 48, y + 84), "Cut the agent's context at the report date.", font("b", 44), SURF, a)
    c.text((M + 48, y + 146), "Run the judge in n8n and hold any Fail for approval.", font("b", 44), SURF, a)

SCENES = [(s1, 5.0), (s2, 6.0), (s3, 6.0), (s4, 7.0), (s5, 6.0)]
FADE = 0.35

def frame(i, t):
    fn, dur = SCENES[i]; c = Canvas(); fn(c, t)
    k = min(1.0, t / FADE if i else 1.0, (dur - t) / FADE if i < len(SCENES) - 1 else 1.0)
    if k < 1: c.im = Image.blend(Image.new("RGB", (W, H), BG), c.im, max(0.0, k))
    return c.im

def render(i):
    fn, dur = SCENES[i]; tmp, out = f"scene{i}.tmp.mp4", f"scene{i}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in range(int(round(dur * FPS))): p.stdin.write(frame(i, f / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out)
    else: sys.exit(f"scene {i} failed")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--still":
        i, t = int(sys.argv[1]), float(sys.argv[3]); frame(i, t).save(f"still{i}.png"); print("still", i)
    else:
        for i in range(len(SCENES)): render(i); print("scene", i)
        open("list.txt", "w").write("".join(f"file 'scene{i}.mp4'\n" for i in range(len(SCENES))))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy",
                        "-movflags", "+faststart", "pm_agent_eval_explainer.mp4"], check=True)
        print("done")
