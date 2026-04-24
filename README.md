# Self-Improving Agent

An AI agent that automatically improves its own prompt. Give it any task — it runs, evaluates its own output, rewrites its prompt based on the feedback, and tries again. Each iteration gets better.

Built from scratch. No LangChain. No AutoGen. Just Python + GPT-4o-mini.

---

## How it works

```
User gives a task
      ↓
Agent runs with current prompt → produces output
      ↓
Evaluator scores output (1-10) across 5 criteria
      ↓
Improver reads score + weaknesses → rewrites the prompt
      ↓
Agent runs again with the improved prompt
      ↓
Repeat until target score reached or max iterations hit
      ↓
Best output wins
```

The prompt literally rewrites itself every iteration based on what the evaluator found wrong.

---

## Demo

**Iteration 1** — Generic prompt → Score 7/10  
**Iteration 2** — Improver adds analogies, examples, comparisons → Score 8/10  
**Iteration 3** — Improver refines persona + adds summary instruction → Accuracy 9/10  

Score improved from 7 → 8 → 8 across 3 iterations on "Explain transformer architecture to a beginner."

---

## Project structure

```
self-improving-agent/
├── app.py              # Streamlit UI with iteration viewer
├── agent.py            # Runs the task with current prompt
├── evaluator.py        # Scores output across 5 criteria
├── improver.py         # Rewrites prompt based on feedback
├── prompt_memory.py    # Saves all prompt versions + scores
├── prompts.py          # Base prompts for all 3 agents
├── config.py           # Settings + API keys from .env
└── requirements.txt
```

---

## Tech stack

| Layer | Tool |
|---|---|
| LLM | GPT-4o-mini (OpenAI) |
| Frontend | Streamlit |
| Memory | JSON persistence |
| Pattern | Meta-agent / self-optimization loop |
| Config | python-dotenv |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/ES7/self-improving-agent
cd self-improving-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up API key**
```bash
cp .env.example .env
```

Fill in `.env`:
```
OPENAI_API_KEY=your_openai_key_here
```

**4. Run**
```bash
streamlit run app.py
```

---

## Evaluation criteria

Every output is scored across 5 dimensions:

| Criteria | What it measures |
|---|---|
| Completeness | Does it fully address the task? |
| Accuracy | Is the content correct? |
| Clarity | Is it well-structured and easy to understand? |
| Depth | Does it go beyond surface level? |
| Usefulness | Would this actually help someone? |

The improver uses weak scores to rewrite the prompt specifically for those gaps.

---

## Settings

Adjustable from the sidebar:
- **Max iterations** — how many times the agent improves (1-5)
- **Target score** — stop early when this score is reached (7-10)

---

## What makes this different

Most AI systems run once and return an output. This one:
- Runs multiple times with an evolving prompt
- Has a separate evaluator agent with strict scoring criteria
- Has a separate improver agent that does prompt engineering automatically
- Remembers high-scoring prompts across sessions and reuses them

This is the foundation of how production AI systems do automated prompt optimization.

---

## Author

**Ebad Sayed** — Final year, IIT (ISM) Dhanbad, Co-founder of Voke AI

Connect: [LinkedIn](https://www.linkedin.com/in/ebad-sayed-0861a6227/) · [GitHub](https://github.com/ES7) · [X](https://x.com/EbadOnAI)
