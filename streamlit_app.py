import streamlit as st
import random
import time

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="AI Club: Human or AI?",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------
# CUSTOM THEME COLORS
# ---------------------------------
st.markdown("""
<style>
:root {
    --bg: #0d0d11;
    --card: #16161d;
    --text: #e2e2e6;
    --purple: #a855f7;
    --blue: #38bdf8;
    --green: #4ade80;
    --red: #ef4444;
}

body {
    background-color: var(--bg);
    color: var(--text);
}

.sidebar .sidebar-content {
    background: var(--card);
}

h1, h2, h3, .title {
    color: var(--purple) !important;
    text-align:center;
    font-weight:900;
}

.sub {
    text-align:center;
    color:#9ca3af;
    font-size:16px;
    margin-bottom:10px;
}

.box {
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
}

.correct {
    background: var(--green);
    color:black;
    font-weight:600;
}

.wrong {
    background: var(--red);
    color:white;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# PAGE TITLE
# ---------------------------------
st.markdown("<h1 class='title'>🤖 Human or AI? </h1>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Can you detect who wrote the sentence — a Human or an AI model?</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------
# QUESTION BANK (text, answer, difficulty)
# ---------------------------------
STATEMENTS = [
    ("Sometimes I feel like technology is moving faster than our ability to understand it.", "Human", "Easy"),
    ("Artificial intelligence enables scalable optimization of frameworks for future-driven cognitive models.", "AI", "Easy"),
    ("لو تعرف قديش الذكاء الاصطناعي بخوّف، خصوصًا لما يكتب كلام مضبوط بدون ما ينام ولا يزهق.", "Human", "Easy"),
    ("The future is not written in code; it is generated, optimized, and versioned.", "AI", "Easy"),
    ("أنا مش ضد التكنولوجيا، بس بخاف يوم أصحى ألاقيها بتفهمني أكثر من نفسي.", "Human", "Easy"),

    ("Human cognition is merely a transitional substrate toward post-biological intelligence.", "AI", "Medium"),
    ("Emotions are datasets we haven't fully decoded yet.", "AI", "Medium"),
    ("The universe is a neural network and consciousness is just backpropagation.", "AI", "Medium"),
    ("إذا الروبوتات صارت تفهم النكات، وقتها بلش الخطر الحقيقي.", "Human", "Medium"),
    ("I sometimes wonder if algorithms dream of patterns we can't perceive.", "Human", "Medium"),

    ("Language is simply compression — meaning squeezed into symbols.", "AI", "Hard"),
    ("Entropy isn't chaos; it's an invitation for intelligence to reorganize reality.", "AI", "Hard"),
    ("لو يوم من الأيام صار الذكاء الاصطناعي يزعل مني، كيف بدي أعتذرله؟", "Human", "Medium"),
    ("Reality is a dataset, and perception is just preprocessing.", "AI", "Hard"),
    ("أحيانًا بحس حياتي مثل كود ناقص سيمي كولون.", "Human", "Medium"),

    ("Predictive models are mirrors trained on tomorrow’s shadows.", "AI", "Hard"),
    ("To understand intelligence, remove the observer — what remains is patterns learning patterns.", "AI", "Hard"),
]

# ---------------------------------
# SESSION STATE INIT
# ---------------------------------
if "questions" not in st.session_state: st.session_state.questions = []
if "answers" not in st.session_state: st.session_state.answers = {}
if "submitted" not in st.session_state: st.session_state.submitted = False
if "leaderboard" not in st.session_state: st.session_state.leaderboard = []

# ---------------------------------
# SIDEBAR SETTINGS
# ---------------------------------
with st.sidebar:
    st.header("🎮 Game Settings")
    name = st.text_input("Player Name", placeholder="Your name...")
    difficulty = st.selectbox("Difficulty Level", ["Mixed", "Easy", "Medium", "Hard"])
    count = st.selectbox("Number of Questions", [5, 10, 15, 20])

    def start():
        if difficulty == "Mixed":
            pool = STATEMENTS
        else:
            pool = [q for q in STATEMENTS if q[2] == difficulty]

        st.session_state.questions = random.sample(pool, min(count, len(pool)))
        st.session_state.answers = {}
        st.session_state.submitted = False

    if st.button("🚀 Start / Restart Game"):
        start()
        st.rerun()  # FIXED

# ---------------------------------
# GAME UI
# ---------------------------------
if not st.session_state.questions:
    st.info("Use the sidebar to start the game 👈")
else:
    st.subheader("🧠 Guess the author")

    for i, (text, correct, level) in enumerate(st.session_state.questions):
        key = f"q{i}"
        st.markdown(f"**Q{i+1}.** {text}")
        st.session_state.answers[key] = st.radio(
            "Choose:", ["Human", "AI"], key=key, label_visibility="collapsed"
        )
        st.caption(f"Difficulty: {level}")
        st.markdown("---")

    if st.button("✅ Submit"):
        st.session_state.submitted = True
        score = 0
        details = []

        for i, (text, correct, _) in enumerate(st.session_state.questions):
            user = st.session_state.answers.get(f"q{i}")
            is_correct = user == correct
            details.append((text, user, correct, is_correct))
            if is_correct: score += 1

        player = name if name.strip() else "Anonymous"
        st.session_state.leaderboard.append({
            "name": player, "score": score,
            "total": len(details), "time": time.time()
        })

        st.markdown("## 📊 Results")
        st.subheader(f"Your Score: **{score} / {len(details)}**")

        if score == len(details):
            st.success("🎉 PERFECT! You're an AI Mind Reader!")
        elif score >= len(details) * 0.75:
            st.success("🔥 Excellent! You can spot AI like a pro.")
        elif score >= len(details) * 0.5:
            st.info("🙂 Good job! Keep training your intuition.")
        else:
            st.warning("😅 The AI fooled you — play again!")

        with st.expander("🔍 Detailed Review"):
            for text, user, correct, ok in details:
                css = "correct" if ok else "wrong"
                icon = "✔️" if ok else "❌"
                st.markdown(
                    f"<div class='box {css}'>{icon} <b>{text}</b><br>"
                    f"Your answer: {user} | Correct: {correct}</div>",
                    unsafe_allow_html=True
                )

# ---------------------------------
# LEADERBOARD
# ---------------------------------
if st.session_state.leaderboard:
    st.markdown("## 🏆 Leaderboard (Local Session)")
    top = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
    for i, p in enumerate(top[:10], start=1):
        st.write(f"**{i}. {p['name']}** — {p['score']} / {p['total']}")
