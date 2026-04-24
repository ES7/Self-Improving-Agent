"""
app.py
------
Streamlit UI for the Self-Improving Agent.
Run with: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from config import MAX_ITERATIONS, TARGET_SCORE
from prompts import DEFAULT_AGENT_PROMPT
from agent import run_agent
from evaluator import evaluate
from improver import improve_prompt
from prompt_memory import save_iteration, get_best_prompt, get_history

st.set_page_config(page_title="Self-Improving Agent", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.iteration-card {
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #3B82F6;
    background: #f8fafc;
}
.score-low    { border-left-color: #ef4444; }
.score-mid    { border-left-color: #f59e0b; }
.score-high   { border-left-color: #22c55e; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Self-Improving Agent")
st.markdown("Give it any task. The agent runs, gets evaluated, improves its own prompt, and tries again — automatically.")
st.divider()

# ── Sidebar settings ──────────────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Settings")
    max_iter = st.slider("Max iterations", 1, 5, MAX_ITERATIONS)
    target = st.slider("Target score (stop early)", 7, 10, TARGET_SCORE)
    st.divider()
    st.subheader("📜 Prompt History")
    history = get_history()
    if history:
        st.caption(f"{len(history)} iterations stored")
        for h in history[-5:]:
            st.markdown(f"**Score {h['score']}/10** — iter {h['iteration']}")
            st.caption(h['timestamp'])
    else:
        st.caption("No history yet")

# ── Input ─────────────────────────────────────────────────
task = st.text_area(
    "What task should the agent solve?",
    placeholder="Explain the concept of transformer architecture to a beginner.\n\nOR\n\nWrite a Python function to detect palindromes.\n\nOR\n\nAnalyze the pros and cons of microservices architecture.",
    height=120,
)

run_btn = st.button("🚀 Run & Improve", type="primary", use_container_width=True)

if run_btn and task:
    st.divider()

    # Check memory for a good starting prompt
    remembered_prompt = get_best_prompt(task)
    if remembered_prompt:
        st.info("💾 Found a high-scoring prompt in memory — starting from there!")
        current_prompt = remembered_prompt
    else:
        current_prompt = DEFAULT_AGENT_PROMPT

    iterations_data = []
    best_output = ""
    best_score = 0

    progress = st.progress(0, text="Starting...")

    for i in range(max_iter):
        progress.progress((i) / max_iter, text=f"Iteration {i+1}/{max_iter} running...")

        with st.expander(f"Iteration {i+1}", expanded=(i == 0)):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("**Prompt used:**")
                st.code(current_prompt, language="text")

            # Run agent
            with st.spinner(f"Agent running..."):
                output = run_agent(task, current_prompt)

            st.markdown("**Output:**")
            st.markdown(output)

            # Evaluate
            with st.spinner("Evaluating..."):
                evaluation = evaluate(task, output)

            score = evaluation.get("score", 0)

            with col2:
                css = "score-high" if score >= 8 else "score-mid" if score >= 6 else "score-low"
                st.markdown(
                    f'<div class="iteration-card {css}">'
                    f'<h2 style="margin:0">{score}/10</h2>'
                    f'<p style="margin:0;font-size:0.8rem">Quality score</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                criteria = evaluation.get("criteria_scores", {})
                for k, v in criteria.items():
                    st.metric(k.capitalize(), f"{v}/10")

            if evaluation.get("strengths"):
                st.markdown("**✅ Strengths:**")
                for s in evaluation["strengths"]:
                    st.markdown(f"- {s}")

            if evaluation.get("weaknesses"):
                st.markdown("**⚠️ Weaknesses:**")
                for w in evaluation["weaknesses"]:
                    st.markdown(f"- {w}")

            # Save to memory
            save_iteration(task, current_prompt, output, evaluation, i + 1)
            iterations_data.append({"iteration": i+1, "score": score, "output": output, "prompt": current_prompt})

            if score > best_score:
                best_score = score
                best_output = output

            # Stop if target reached
            if score >= target:
                st.success(f"🎯 Target score {target}/10 reached! Stopping early.")
                progress.progress(1.0, text="Done!")
                break

            # Improve prompt for next iteration
            if i < max_iter - 1:
                with st.spinner("Improving prompt for next iteration..."):
                    current_prompt = improve_prompt(task, current_prompt, evaluation)
                st.info(f"🔧 Prompt improved. Running iteration {i+2}...")

        progress.progress((i + 1) / max_iter, text=f"Iteration {i+1} complete — score: {score}/10")

    # Final summary
    st.divider()
    st.subheader("📊 Improvement Summary")

    cols = st.columns(len(iterations_data))
    for col, data in zip(cols, iterations_data):
        col.metric(f"Iteration {data['iteration']}", f"{data['score']}/10")

    if len(iterations_data) > 1:
        first = iterations_data[0]["score"]
        last = iterations_data[-1]["score"]
        delta = last - first
        if delta > 0:
            st.success(f"📈 Score improved by {delta} points across {len(iterations_data)} iterations!")
        elif delta == 0:
            st.info("Score stayed the same — prompt was already optimal.")
        else:
            st.warning("Score decreased — try with more iterations.")

    st.subheader("🏆 Best Output")
    st.markdown(best_output)

    # Download
    report = f"# Self-Improving Agent Report\n\n**Task:** {task}\n\n**Best Score:** {best_score}/10\n\n---\n\n## Best Output\n\n{best_output}\n\n---\n\n## All Iterations\n\n"
    for d in iterations_data:
        report += f"### Iteration {d['iteration']} — Score {d['score']}/10\n\n{d['output']}\n\n---\n\n"

    st.download_button("⬇️ Download Report", report, file_name="self_improving_report.md", mime="text/markdown")

elif run_btn:
    st.warning("Please enter a task first.")

st.divider()
st.caption("Built by Ebad Sayed · Self-Improving Agent · GPT-4o-mini")
