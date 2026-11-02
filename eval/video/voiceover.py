"""Voiceover with Kokoro (ONNX) from hand-written misaki-style US phonemes; one clip per scene, fitted to its slot."""
import json, sys, wave, numpy as np, onnxruntime as ort

D = "/home/claude/video/tts/"
VOCAB = json.load(open(D + "src/src/kokoro_onnx/config.json"))["vocab"]
VOICES = np.load(D + "voices-v1.0.bin")
sess = ort.InferenceSession(D + "kokoro-v1.0.int8.onnx", providers=["CPUExecutionProvider"])
names = {i.name: i for i in sess.get_inputs()}
tok_in = "input_ids" if "input_ids" in names else "tokens"
SR = 24000
VOICE = sys.argv[1] if len(sys.argv) > 1 else "af_heart"

# (scene start s, slot length s, text, phonemes)
LINES = [
 (0.0, 5.0, "How good are the PM agent's weekly reports? We judged all six.",
  "hˈW ɡˈʊd ɑɹ ðə pˌiˈɛm ˈAʤənts wˈikli ɹəpˈɔɹts? wi ʤˈʌʤd ˈɔl sˈɪks."),
 (5.0, 6.0, "Two blind passes: twenty-eight number checks against Jira, and a separate Claude model as judge.",
  "tˈu blˈInd pˈæsᵻz: tˈwɛnti ˈAt nˈʌmbɚ ʧˈɛks əɡˈɛnst ʤˈiɹə, ænd ə sˈɛpɹət klˈɔd mˈɑdᵊl æz ʤˈʌʤ."),
 (11.0, 6.0, "The judge scores seven criteria, led by accuracy and risk coverage.",
  "ðə ʤˈʌʤ skˈɔɹz sˈɛvən kɹIˈtɪɹiə, lˈɛd bI ˈækjəɹəsi ænd ɹˈɪsk kˈʌvəɹɪʤ."),
 (17.0, 7.0, "The average was three point eight eight. Three weeks passed, two needed edits, and one failed.",
  "ði ˈævəɹɪʤ wʌz θɹˈi pˈYnt ˈAt ˈAt. θɹˈi wˈiks pˈæst, tˈu nˈidᵻd ˈɛdᵻts, ænd wˈʌn fˈAld."),
 (24.0, 6.0, "The numbers were right; the timing wasn't. Next: limit the agent to what it knew that day.",
  "ðə nˈʌmbɚz wɚ ɹˈIt; ðə tˈImɪŋ wˈʌzᵊnt. nˈɛkst: lˈɪmᵻt ði ˈAʤənt tə wˌʌt ɪt nˈu ðˈæt dˈA."),
]

def synth(ph, speed):
    toks = [VOCAB[c] for c in ph if c in VOCAB]
    missing = {c for c in ph if c not in VOCAB}
    if missing: print("missing", missing)
    style = VOICES[VOICE][min(len(toks), len(VOICES[VOICE])) - 1]
    feed = {tok_in: np.array([[0, *toks, 0]], dtype=np.int64), "style": np.asarray(style, np.float32),
            "speed": np.array([speed], dtype=np.float32 if names["speed"].type == "tensor(float)" else np.int32)}
    a = np.asarray(sess.run(None, feed)[0]).ravel()
    nz = np.where(np.abs(a) > 0.01)[0]  # trim leading/trailing silence
    return a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a

track = np.zeros(int(30 * SR), np.float32)
LEAD = 0.35
for start, slot, txt, ph in LINES:
    speed, a = 1.0, synth(ph, 1.0)
    room = slot - LEAD - 0.35
    while len(a) / SR > room and speed < 1.35:
        speed = round(speed + 0.05, 2); a = synth(ph, speed)
    print(f"{start:5.1f}s  {len(a)/SR:4.2f}s / {room:.2f}s  speed {speed}  | {txt}")
    i = int((start + LEAD) * SR); track[i:i + len(a)] += a[: len(track) - i]
peak = np.abs(track).max(); track = track / peak * 0.89
with wave.open("/home/claude/video/voiceover.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((track * 32767).astype("<i2").tobytes())
print("wrote voiceover.wav")
