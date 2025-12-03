from typing import Tuple

def improve_prompt(prompt: str, note: str = None) -> Tuple[str, str]:
    """
    Simple safe prompt improver.
    Returns (improved_prompt, reason)
    """

    if not prompt:
        return "", "Prompt was empty."

    original = prompt.strip()

    # If the prompt is already long & clear, don’t change it
    if len(original.split()) > 6:
        return original, "Prompt already looks clear."

    # Otherwise improve it
    improved = f"Provide a detailed, well-structured explanation about: {original}"

    # Reason message
    reason = note or "The prompt was too short and lacked context."

    return improved, reason
