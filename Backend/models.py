from pydantic import BaseModel, RootModel
from typing import Optional, Dict, List, Any

class DebateRequest(BaseModel):
    question: str
    chat_id: Optional[str] = None
    use_improved: bool = False
    improved_prompt: Optional[str] = None


class NeedsConfirmationResponse(RootModel[Dict[str, Any]]):
    """
    Previously defined as a BaseModel with `__root__`.
    Now uses RootModel to be compatible with pydantic v2.
    Access the payload via instance.root
    """
    pass


class DebateResult(BaseModel):
    status: str = "debated"
    chat_id: str
    domain: str
    used_prompt: str
    agents: List[str]
    initial: Dict[str, str]
    critiques: Dict[str, str]
    defenses: Dict[str, str]
    winner: str
    scoreboard: Dict[str, float]
    answer: str
    reason: str
    judge_raw: str



