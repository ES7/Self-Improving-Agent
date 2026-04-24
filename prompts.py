# Default starting prompt for the agent
# The improver will rewrite this automatically each iteration
DEFAULT_AGENT_PROMPT = """You are a helpful AI assistant. Complete the following task as best as you can.

Task: {task}

Provide a thorough, well-structured response."""

EVALUATOR_PROMPT = """You are a strict output quality evaluator.

The user's original task was:
{task}

The agent produced this output:
{output}

Evaluate the output on these criteria:
1. Completeness — does it fully address the task?
2. Accuracy — is the content correct and reliable?
3. Clarity — is it well-structured and easy to understand?
4. Depth — does it go beyond surface level?
5. Usefulness — would this actually help someone?

Respond in EXACT JSON only:
{{
    "score": 7,
    "criteria_scores": {{
        "completeness": 7,
        "accuracy": 8,
        "clarity": 7,
        "depth": 6,
        "usefulness": 7
    }},
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "improvement_suggestions": ["specific suggestion 1", "specific suggestion 2", "specific suggestion 3"]
}}"""

IMPROVER_PROMPT = """You are an expert prompt engineer. Your job is to improve an AI agent's system prompt based on evaluation feedback.

Original task the agent needs to solve:
{task}

Current agent prompt:
{current_prompt}

Evaluation score: {score}/10
Weaknesses identified: {weaknesses}
Improvement suggestions: {suggestions}

Rewrite the agent prompt to fix these weaknesses and incorporate the suggestions.
The new prompt should make the agent produce a significantly better output for this task.

Rules:
- Keep the {{task}} placeholder exactly as is
- Make the prompt more specific and directive
- Add explicit instructions to address the weaknesses
- Be concise — don't make it unnecessarily long

Return ONLY the new prompt text, nothing else. No explanation, no JSON, just the prompt."""
