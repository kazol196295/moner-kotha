# 🌿 মনের কথা — Bengali Mental Health Counsellor
[![Model](https://img.shields.io/badge/🤗%20Model-kazol196295%2Fllama--3.1--8b--bengali--mental--health--counsellor-teal)](https://huggingface.co/kazol196295/llama-3.1-8b-bengali-mental-health-counsellor)
[![Training Repo](https://img.shields.io/badge/GitHub-Training%20Repo-181717?logo=github)](https://github.com/kazol196295/llama-3.1-8b-bengali-mental-health-counsellor)
[![Live App](https://img.shields.io/badge/🌿%20Live%20App-moner--kotha-green)](https://moner-kotha-kazol.streamlit.app)

**A compassionate AI-powered mental health counselling chatbot in Bengali, built with a fine-tuned LLaMA 3.1 8B model.**


🔗 **Live App:** [moner-kotha-kazol.streamlit.app](https://moner-kotha-kazol.streamlit.app)

---
## 🔗 Related Repositories

This app is powered by a custom fine-tuned model. The full training pipeline
lives in a separate repository:

| Repo | Purpose |
|------|---------|
| [llama-3.1-8b-bengali-mental-health-counsellor](https://github.com/kazol196295/llama-3.1-8b-bengali-mental-health-counsellor) | Fine-tuning (QLoRA + Unsloth), evaluation, model weights |
| [kazol196295/llama-3.1-8b-bengali-mental-health-counsellor](https://huggingface.co/kazol196295/llama-3.1-8b-bengali-mental-health-counsellor) | Published model on HuggingFace Hub |

## 🏗️ Architecture

```
👤 User
   ↓
🌐 Streamlit Cloud  (always-on frontend — moner-kotha-kazol.streamlit.app)
   ↓  HTTP streaming
🔗 ngrok tunnel     (public HTTPS bridge — changes each Colab session)
   ↓
🖥️ Google Colab T4 GPU  (my fine-tuned LLaMA 3.1 8B model)
```

---

## 📁 Project Structure

```
moner-kotha/
├── app.py                  ← Streamlit frontend (deployed on Streamlit Cloud)
├── requirements.txt        ← Python dependencies for Streamlit Cloud
├── README.md               ← This file
└── colab/
    └── backend.py          ← FastAPI backend — run this in Google Colab (T4 GPU)
```

---

## 🤖 Model

| Property | Value |
|---|---|
| **Base model** | `meta-llama/Llama-3.1-8B-Instruct` |
| **Fine-tuned model** | [`kazol196295/llama-3.1-8b-bengali-mental-health-counsellor`](https://huggingface.co/kazol196295/llama-3.1-8b-bengali-mental-health-counsellor) |
| **Training data** | Bengali Empathetic Conversations Corpus |
| **Method** | QLoRA (4-bit, r=16) with Unsloth |
| **Training framework** | Unsloth + TRL SFTTrainer |

---

## 🚀 How to Run

### Step 1 — Get free tokens (one time only)

| Token | Where to get |
|---|---|
| **HuggingFace token** | [huggingface.co](https://huggingface.co) → Settings → Access Tokens → New token |
| **ngrok authtoken** | [ngrok.com](https://ngrok.com) → Sign up free → Dashboard → Your Authtoken |

---

### Step 2 — Start the Colab backend (every session)

1. Open [Google Colab](https://colab.research.google.com)
2. Upload `colab/backend.py` or paste it into a code cell
3. **Runtime → Change runtime type → T4 GPU**
4. Fill in your tokens at the top of the file:

   ```python
   HF_TOKEN    = "hf_xxxxxxxxxxxx"
   NGROK_TOKEN = "2abc123_xxxxxxxxxxxxxxxx"
   ```

5. Run the cell — wait ~3–5 min for the model to load
6. Copy the printed **PUBLIC URL**:

   ```
   ══════════════════════════════════════════════
     🌐  PUBLIC URL:  https://xxxx.ngrok-free.app
   ══════════════════════════════════════════════
   ```

7. ⚠️ **Keep the Colab tab open** — closing it stops the server

---

### Step 3 — Connect Streamlit to Colab

1. Open the live app: [moner-kotha-kazol.streamlit.app](https://moner-kotha-kazol.streamlit.app)
2. In the **sidebar**, paste your ngrok URL into the **"Colab Backend URL"** box
3. The status badge turns **green** when connected ✓
4. Start chatting!

> No secrets or config files needed — just paste the URL in the UI.

---

## 🖥️ Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/moner-kotha.git
cd moner-kotha

# Install dependencies
pip install streamlit requests

# Run Streamlit locally
streamlit run app.py
# → Open http://localhost:8501
# → Paste your Colab ngrok URL in the sidebar
```

---

## 💬 Features

- **10 mental health topics** — Depression, Anxiety, Relationship Issues, Family Issues, Work Stress, Loneliness, Low Self-esteem, Grief, Anger, and more
- **Streaming responses** — tokens appear in real time as the model generates
- **Fully Bengali UI** — interface and responses in Bengali
- **No login required** — open and use instantly
- **Connection status** — live indicator shows if the Colab backend is online

---

## ⚠️ Disclaimer

This AI counsellor is **not a substitute** for professional mental health care. It is an educational and supportive tool only.

**Emergency contacts (Bangladesh):**

| Service | Number |
|---|---|
| কান পেতরই | 01521474251 |
| জাতীয় মানসিক স্বাস্থ্য হেল্পলাইন | 16789 |

---

## 📄 License

MIT License — free to use, modify, and distribute.
