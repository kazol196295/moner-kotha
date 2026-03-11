# ╔══════════════════════════════════════════════════════════════════╗
# ║  মনের কথা — COLAB BACKEND                                       ║
# ║                                                                  ║
# ║  HOW TO USE:                                                     ║
# ║  1. Open Google Colab → Runtime → Change runtime type → T4 GPU  ║
# ║  2. Upload this file (or paste into a code cell)                 ║
# ║  3. Fill in HF_TOKEN and NGROK_TOKEN below                       ║
# ║  4. Run the cell                                                 ║
# ║  5. Copy the printed PUBLIC URL                                  ║
# ║  6. Paste it in Streamlit Cloud → Settings → Secrets:           ║
# ║       BACKEND_URL = "https://xxxx.ngrok-free.app"               ║
# ║  7. Keep this Colab tab open while your app is live!             ║
# ╚══════════════════════════════════════════════════════════════════╝

# ── STEP 1: Install packages ───────────────────────────────────────────────────
import subprocess, sys

def install(pkg):
    subprocess.check_call([sys.executable, "-q", "-m", "pip", "install", pkg])

for pkg in [
    "fastapi", "uvicorn[standard]", "pyngrok", "nest_asyncio",
    "transformers", "accelerate", "bitsandbytes", "peft",
    "huggingface_hub", "sentencepiece", "protobuf",
]:
    install(pkg)

print("✅ Packages installed")

# ── STEP 2: Your tokens ────────────────────────────────────────────────────────
HF_TOKEN    = ""   # ← HuggingFace token (huggingface.co → Settings → Tokens)
                   #   Required only if your model repo is private
NGROK_TOKEN = ""   # ← Free ngrok authtoken (ngrok.com → Dashboard → Your Authtoken)

# ── STEP 3: Config ─────────────────────────────────────────────────────────────
MODEL_ID = "kazol196295/llama-3.1-8b-bengali-mental-health-counsellor"
PORT     = 8000

# ── STEP 4: Load model ─────────────────────────────────────────────────────────
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TextIteratorStreamer,
)

print(f"⏳ Loading model: {MODEL_ID}")
print("   (first run downloads ~5 GB — takes 3–5 min; cached on reruns)")

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    token=HF_TOKEN or None,
    trust_remote_code=True,
)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=quant_config,
    device_map="auto",
    token=HF_TOKEN or None,
    trust_remote_code=True,
    torch_dtype=torch.float16,
)
model.eval()
print("✅ Model loaded and ready!")

# ── STEP 5: FastAPI app ────────────────────────────────────────────────────────
import threading, asyncio, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="মনের কথা Backend")

# Allow requests from Streamlit Cloud (different origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    topic:   str
    message: str


@app.get("/health")
def health():
    """Streamlit pings this to check if the backend is alive."""
    return {"status": "ok", "model": MODEL_ID}


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Streams tokens one-by-one as NDJSON lines:
      {"token": "আমি"}
      {"token": " বুঝতে"}
      ...
      {"done": true}
    """
    # Prompt format matches your training data exactly
    prompt = (
        f"[INST]\n"
        f"Topic: {req.topic}\n"
        f"User: {req.message}\n"
        f"Respond empathetically as a counselor.\n"
        f"[/INST]\n"
        f"Counselor:\n"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024,
    ).to(model.device)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )

    gen_kwargs = dict(
        **inputs,
        max_new_tokens=400,
        temperature=0.75,
        do_sample=True,
        top_p=0.92,
        repetition_penalty=1.15,
        pad_token_id=tokenizer.eos_token_id,
        streamer=streamer,
    )

    # Run generation in background thread so we can stream tokens
    thread = threading.Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    async def token_generator():
        for token in streamer:
            if token:
                yield json.dumps({"token": token}, ensure_ascii=False) + "\n"
                await asyncio.sleep(0)          # yield control back to event loop
        yield json.dumps({"done": True}) + "\n"
        thread.join()

    return StreamingResponse(token_generator(), media_type="application/x-ndjson")


# ── STEP 6: Start ngrok tunnel + uvicorn ──────────────────────────────────────
import uvicorn, nest_asyncio
from pyngrok import ngrok, conf

# Authenticate ngrok
conf.get_default().auth_token = NGROK_TOKEN
ngrok.kill()                                    # kill any leftover tunnels

tunnel     = ngrok.connect(PORT, "http")
PUBLIC_URL = tunnel.public_url

print()
print("=" * 62)
print(f"  🌐  PUBLIC URL:  {PUBLIC_URL}")
print("=" * 62)
print()
print("  👆 Copy the URL above, then go to:")
print("     Streamlit Cloud → your app → Settings → Secrets")
print()
print("  Paste this line into the Secrets box:")
print(f'     BACKEND_URL = "{PUBLIC_URL}"')
print()
print("  ⚠️  Keep THIS Colab tab open while your Streamlit app is live!")
print("=" * 62)
print()

# Run FastAPI (blocks the cell — that's intentional)
nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=PORT)
