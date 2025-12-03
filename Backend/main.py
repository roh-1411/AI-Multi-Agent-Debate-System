from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv

# Load environment
load_dotenv()

from Backend.models import DebateRequest
from Backend.prompt_advisor import improve_prompt
from Backend.domain_router import detect_domain, get_agents_for_domain
from Backend.debate_engine import run_debate
from Backend.utils.history_manager import save_history

app = FastAPI(title="AI Debate System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/debate")
def debate(req: DebateRequest):

    # 1. DOMAIN DETECTION
    domain = detect_domain(req.question)
    agents = get_agents_for_domain(domain)

    # 2. PROMPT IMPROVEMENT CHECK
    if not req.use_improved:
        # ✅ unpack (improved_prompt, reason)
        improved_prompt, reason = improve_prompt(
            req.question,
            note="This version makes the request clearer, more structured, and easier for AI models to answer well.",
        )

        if improved_prompt.strip() != req.question.strip():
            # Return "needs confirmation" response structure expected by frontend
            return {
                "status": "needs_confirmation",
                "domain": domain,
                "original_prompt": req.question,
                "improved_prompt": improved_prompt,
                "improvement_reason": reason,
                "explanation": "Your original prompt was short, vague, or could lead to lower-quality AI answers.",
                "message": "Your prompt was improved. Approve?",
            }

        used_prompt = req.question
    else:
        # When user clicked “Use Improved”, frontend sends improved_prompt here
        used_prompt = req.improved_prompt or req.question

    # 3. RUN DEBATE PIPELINE
    initial, critiques, defenses, judge_output, judge_raw = run_debate(
        agents, used_prompt
    )

    winner = judge_output["winner"]
    chat_id = req.chat_id or str(uuid.uuid4())

    # 4. SAVE HISTORY
    save_history(chat_id, used_prompt, initial, critiques, defenses, judge_output)

    # 5. RETURN FULL DEBATE RESULT
    return {
        "status": "debated",
        "chat_id": chat_id,
        "domain": domain,
        "used_prompt": used_prompt,
        "agents": agents,
        "initial": initial,
        "critiques": critiques,
        "defenses": defenses,
        "winner": winner,
        "scoreboard": judge_output.get("scoreboard", {}),
        "answer": initial[winner],
        "reason": judge_output.get("reason", ""),
        "judge_raw": judge_raw,
    }
