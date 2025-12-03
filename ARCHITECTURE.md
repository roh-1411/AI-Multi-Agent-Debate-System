# 🏗 AI Multi-Agent Debate System — Architecture Design

This document describes the internal architecture of the **AI Multi-Agent Debate System**, including major components, data flow, debate pipeline, and mixed online/offline execution modes.

---

# 📌 High-Level Architecture

```
                   ┌───────────────────────────┐
                   │         Frontend           │
                   │  (Next.js / React UI)      │
                   │ - Prompt input             │
                   │ - Improvement UI           │
                   │ - Debate viewer            │
                   │ - Agent outputs            │
                   └─────────────┬─────────────┘
                                 │  POST /debate
                                 ▼
                 ┌───────────────────────────────────┐
                 │              Backend               │
                 │             (FastAPI)              │
                 └─────────────────┬─────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
┌────────────┐             ┌─────────────┐             ┌────────────────┐
│ Prompt     │             │ Domain       │             │ Multi-Agent     │
│ Advisor    │             │ Router       │             │ Debate Engine   │
│ (Rewrite)  │────────────▶│ (General /   │────────────▶│ - Initial round │
└────────────┘             │  Coding / AI)│             │ - Critiques     │
                           └─────────────┘             │ - Defenses      │
                                                      └────────────────┘
                                                               │
                                                               ▼
                                                       ┌─────────────┐
                                                       │   Judge     │
                                                       │ (LLM or     │
                                                       │ Offline)    │
                                                       └─────┬──────┘
                                                             ▼
                                                  ┌─────────────────────┐
                                                  │ Winner + Final Answer│
                                                  └─────────────────────┘
```

---

# 📦 Component Breakdown

### **1. Frontend (Next.js + React)**
- UI for entering prompts  
- Displays improved prompts  
- Shows debate outputs from all agents  
- Displays winner + judge reasoning  
- Calls backend via `/debate`  

---

### **2. Prompt Advisor**
Improves low-quality prompts:
- Detects vague or ambiguous queries  
- Provides refined version  
- Explains improvements  
- Requires user confirmation  

---

### **3. Domain Router**
Routes the question to the correct agent set:
- Coding  
- General knowledge  
- AI/Tech  
Improves accuracy by assigning specialized agents.

---

### **4. AI Provider Layer**
Supports:
- OpenAI  
- Groq  
- Gemini  
- DeepSeek  
- Offline simulation mode  

Automatically falls back to offline if no API keys exist.

---

### **5. Multi-Agent Debate Engine**
Core reasoning module:
- Initial response  
- Cross-critique  
- Defense  
Handles debate flow and produces structured outputs.

---

### **6. Judge System**
Evaluates all agents based on:
- correctness  
- clarity  
- coherence  
- completeness  
Selects a winner and produces reasoning.

---

# 🔄 Data Flow

```
User Prompt
   │
   ▼
Prompt Advisor → (optional improvement)
   │
   ▼
Domain Router → Select Agents
   │
   ▼
Multi-Agent Debate Engine
   ├── Initial Answers
   ├── Critiques
   ├── Defenses
   ▼
Judge System → Winner + Final Answer
   │
   ▼
Frontend Output
```

---

# 🔥 Mixed Mode Architecture (Online + Offline)

```
           ┌───────────────┐
           │  API Keys?     │
           └───────┬───────┘
                   │
        ┌──────────┴───────────┐
        ▼                        ▼
 Online Mode                Offline Mode
 (Real LLM APIs)         (Simulated Responses)
```

System auto-selects mode at runtime.

---

# 🧠 Debate Pipeline Diagram

```
┌──────────────┐
│ User Prompt  │
└───────┬──────┘
        ▼
┌─────────────────────┐
│ Prompt Improvement?  │
└───────┬─────────────┘
        │Yes
        ▼
 ┌────────────┐
 │ Improved   │
 │ Prompt     │
 └────────────┘

        ▼
┌──────────────┐
│ Initial Round│
└───────┬──────┘
        ▼
┌──────────────┐
│ Critiques    │
└───────┬──────┘
        ▼
┌──────────────┐
│ Defenses     │
└───────┬──────┘
        ▼
┌──────────────┐
│   Judge       │
└───────┬──────┘
        ▼
┌──────────────┐
│ Final Answer │
└──────────────┘
```

---

# 📄 End of Architecture Document
