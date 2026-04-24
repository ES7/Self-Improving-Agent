from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)


def run_agent(task: str, prompt_template: str) -> str:
    """
    Run the agent with the given prompt template.
    {task} in the template gets replaced with the actual task.
    """
    system_prompt = prompt_template.replace("{task}", task)

    print(f"[Agent] Running with prompt ({len(system_prompt)} chars)...")

    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ],
        temperature=0.7,
    )

    output = response.choices[0].message.content.strip()
    print(f"[Agent] Output generated ({len(output)} chars)")
    return output
