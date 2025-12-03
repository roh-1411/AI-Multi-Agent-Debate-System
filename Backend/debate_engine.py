import json
from Backend.ai_providers import AGENTS

class DebateEngine:

    def __init__(self, agents, prompt):
        self.agents = agents
        self.prompt = prompt

    def initial_round(self):
        out = {}
        for aid in self.agents:
            out[aid] = AGENTS[aid].ask(self.prompt)
        return out

    def critique_round(self, initial):
        out = {}
        for aid in self.agents:
            text = "Critique all answers:\n"
            for other, ans in initial.items():
                text += f"[{other}] {ans}\n"

            out[aid] = AGENTS[aid].ask(text)
        return out

    def defense_round(self, initial, critiques):
        out = {}
        for aid in self.agents:
            txt = f"Your answer: {initial[aid]}\nCritiques:\n"
            for other, c in critiques.items():
                txt += f"[{other}] {c}\n"

            out[aid] = AGENTS[aid].ask(txt)
        return out

    def judge(self, initial, critiques, defenses):
        judge_prompt = {
            "initial": initial,
            "critiques": critiques,
            "defenses": defenses
        }

        prompt = f"""
Evaluate this JSON debate. Score each agent 1–10.
Return JSON: winner, scoreboard, reason.

{json.dumps(judge_prompt)}
"""

        raw = AGENTS["gpt4_coder"].ask(prompt)

        try:
            data = json.loads(raw)
            return data, raw
        except:
            first = list(initial.keys())[0]
            return {
                "winner": first,
                "scoreboard": {},
                "reason": "Judge fallback"
            }, raw


def run_debate(agents, prompt):
    eng = DebateEngine(agents, prompt)

    initial = eng.initial_round()
    critiques = eng.critique_round(initial)
    defenses = eng.defense_round(initial, critiques)
    judge_output, judge_raw = eng.judge(initial, critiques, defenses)

    return initial, critiques, defenses, judge_output, judge_raw
