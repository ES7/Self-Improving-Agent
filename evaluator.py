"""
evaluator.py
------------
Scores the agent's output quality.
Returns a score 1-10 + detailed feedback.
This feedback is what the improver uses to fix the prompt.
"""

import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from prompts import EVALUATOR_PROMPT

_client = OpenAI(api_key=OPENAI_API_KEY)


def evaluate(task: str, output: str) -> dict:
    """
    Score the agent output.
    Returns dict with score, strengths, weaknesses, suggestions.
    """
    prompt = EVALUATOR_PROMPT.format(task=task, output=output)

    print("[Evaluator] Scoring output...")

    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "score": 5,
            "criteria_scores": {},
            "strengths": [],
            "weaknesses": ["Could not parse evaluation"],
            "improvement_suggestions": ["Try again"]
        }

    print(f"[Evaluator] Score: {result.get('score', 0)}/10")
    return result
