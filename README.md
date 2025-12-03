# 🧠 AI Multi-Agent Debate System

A research-grade AI framework that improves user prompts, runs structured multi-agent debates, and selects the best answer using a judging model.

Supports **mixed operation mode**:
- ✔ **Online Mode** (OpenAI / Groq / Gemini / DeepSeek)
- ✔ **Offline Mode** (no API keys required — simulated local responses)

---

# 📌 Overview

This project is inspired by research in:

- Multi-Agent Debate  
- Constitutional AI  
- Deliberative Alignment  
- Critique-and-Refinement Reasoning  

The system includes:

- Prompt Advisor  
- Domain Router  
- Multi-Agent Debate Engine  
- Judge Module  
- Offline/Online Agents  
- React Frontend  

---

# ⚙ Backend Setup

## Create virtual environment
```
cd Backend
python -m venv venv
venv\Scripts\activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Configure .env
```
OPENAI_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
OPENAI_JUDGE_MODEL=gpt-4.1
```

Leave empty for offline mode.

## Start backend
```
cd ..
uvicorn Backend.main:app --reload --port 8000
```

---

# 🎨 Frontend Setup

```
cd Frontend
npm install
npm run dev
```

---

# 📡 API Documentation

## POST /debate

### Request
```
{
  "question": "string",
  "use_improved": false,
  "improved_prompt": null,
  "chat_id": null
}
```

### Responses

#### Prompt Improvement
```
{
  "status": "needs_confirmation",
  "improved_prompt": "...",
  "message": "Your prompt was improved. Approve?"
}
```

#### Full Debate
```
{
  "status": "debated",
  "winner": "agent_name",
  "answer": "final_answer"
}
```

---

# 🧭 Roadmap

- Agent personalities  
- Streaming responses  
- Model selection  
- PDF export  
- Analytics dashboard  

---

# 📄 License

MIT License.
