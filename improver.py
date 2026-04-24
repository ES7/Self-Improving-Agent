from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from prompts import IMPROVER_PROMPT

_client = OpenAI(api_key=OPENAI_API_KEY)


def improve_prompt(task: str, current_prompt: str, evaluation: dict) -> str:
    """
    Takes the current prompt + evaluation feedback.
    Returns an improved prompt for the next iteration.
    """
    score = evaluation.get("score", 0)
    weaknesses = "\n".join(evaluation.get("weaknesses", []))
    suggestions = "\n".join(evaluation.get("improvement_suggestions", []))

    prompt = IMPROVER_PROMPT.format(
        task=task,
        current_prompt=current_prompt,
        score=score,
        weaknesses=weaknesses,
        suggestions=suggestions,
    )

    print(f"[Improver] Rewriting prompt based on score {score}/10...")

    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    new_prompt = response.choices[0].message.content.strip()
    print(f"[Improver] New prompt ready ({len(new_prompt)} chars)")
    return new_prompt
