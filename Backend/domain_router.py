from Backend.ai_providers import AGENTS

DOMAINS = ["coding", "mechanical", "math", "physics", "general"]

DOMAIN_AGENTS = {
    "coding": ["gpt4_coder", "deepseek_chat", "groq_llama", "gemini_flash"],
    "mechanical": ["groq_llama", "gpt4_coder", "gemini_flash"],
    "math": ["deepseek_chat", "gpt4_coder", "groq_llama"],
    "physics": ["groq_llama", "gpt4_coder", "gemini_flash"],
    "general": ["gpt4_coder", "groq_llama", "gemini_flash", "deepseek_chat"]
}

def detect_domain(question: str) -> str:
    prompt = f"""
Classify: coding, mechanical, math, physics, general.
Question: {question}
Return ONLY domain.
"""

    try:
        out = AGENTS["gpt4_coder"].ask(prompt).strip().lower()
        return out if out in DOMAINS else "general"
    except:
        return "general"


def get_agents_for_domain(domain: str):
    return DOMAIN_AGENTS.get(domain, DOMAIN_AGENTS["general"])
