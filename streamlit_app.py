import streamlit as st
import random
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Club: Human or AI?",
    page_icon="🤖",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.title { text-align:center; font-size:36px; font-weight:900; }
.sub { text-align:center; color:#888; margin-bottom:20px; }
.box { padding:10px; border-radius:8px; margin-bottom:10px; }
.correct { background:#16a34a; color:white; }
.wrong { background:#dc2626; color:white; }
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<div class='title'>🤖 Human or AI? – PRO Edition</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Can you detect who wrote the sentence — a Human or an AI model?</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- QUESTION BANK (text, answer, difficulty) ----------
STATEMENTS = [
    ("Sometimes I feel like technology is moving faster than our ability to understand it.", "Human", "Easy"),
    ("Artificial intelligence enables scalable optimization of frameworks for future-driven cognitive models.", "AI", "Easy"),
    ("لو تعرف قديش الذكاء الاصطناعي بخوّف، خصوصًا لما يكتب كلام مضبوط بدون ما ينام ولا يزهق.", "Human", "Easy"),
    ("The future is not written in code; it is generated, optimized, and versioned.", "AI", "Easy"),
    ("أنا مش ضد التكنولوجيا، بس بخاف يوم أصحى ألاقيها بتفهمني أكثر من نفسي.", "Human", "Easy"),

    ("Human cognition is merely a transitional substrate toward post-biological intelligence.", "AI", "Medium"),
    ("أنا بكتب البرمجة كأني بحكي مع صاحبتي، كل سطر له مزاج!", "Human", "Medium"),
    ("Emotions are datasets we haven't fully decoded yet.", "AI", "Medium"),
    ("إذا الروبوتات صارت تفهم النكات، وقتها بلش الخطر الحقيقي.", "Human", "Medium"),
    ("The universe is a neural network and consciousness is just backpropagation.", "AI", "Medium"),

    ("I sometimes wonder if algorithms dream of patterns we can't perceive.", "Human", "Medium"),
    ("Language is simply compression — meaning squeezed into symbols.", "AI", "Hard"),
    ("Entropy isn't chaos; it's an invitation for intelligence to reorganize reality.", "AI", "Hard"),
    ("لو يوم من الأيام صار الذكاء الاصطناعي يزعل مني، كيف بدي أعتذرله؟", "Human", "Medium"),
    ("Predictive models are simply mirrors trained on tomorrow’s shadows.", "AI", "Hard"),

    ("To understand intelligence, remove the observer — what remains is patterns learning patterns.", "AI", "Hard"),
    ("Sometimes silence feels like a programming bug in my thoughts.", "Human", "Medium"),
    ("Reality is a dataset, and perception is just preprocessing.", "AI", "Hard"),
    ("أحيانًا بحس حياتي مثل كود ناقص سيمي كولون.", "Human", "Medium"),
    ("My emotions feel like variables that keep getting overwritten.", "Human", "Medium"),
]

# ---------- SESSION STATE ----------
if "questions" not in st.session_state: st.session_state.questions = []
if "answers" not in st.session_state: st.session_state.answers = {}
if "submitted" not in st.session_state: st.session_state.submitted = False
if "leaderboard" not in st.session_state: st.session_state.leaderboard = []

# ---------- SIDEBAR SETTINGS ----------
with st.sidebar:
    st.header("🎮 Settings")
    name = st.text_input("Player Name:", placeholder="Your name...")
    difficulty = st.selectbox("Difficulty:", ["Mixed", "Easy", "Medium", "Hard"])
    count = st.selectbox("Number of questions:", [5, 10, 15, 20])

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
        st.experimental_rerun()

# ---------- GAME DISPLAY ----------
if not st.session_state.questions:
    st.info("Select settings in the sidebar and start the game 👈")
else:
    st.subheader("🧠 Guess the author of each statement")

    for i, (text, correct, level) in enumerate(st.session_state.questions):
        key = f"q{i}"
        st.markdown(f"**Q{i+1}.** {text}")
        ans = st.radio("Select:", ["Human", "AI"], key=key, label_visibility="collapsed")
        st.session_state.answers[key] = ans
        st.caption(f"Difficulty: {level}")
        st.markdown("---")

    if st.button("✅ Submit"):
        st.session_state.submitted = True
        score = 0
        details = []

        for i, (text, correct, level) in enumerate(st.session_state.questions):
            user = st.session_state.answers.get(f"q{i}")
            result = user == correct
            details.append((text, user, correct, result))
            if result: score += 1

        display_name = name if name.strip() else "Anonymous"
        st.session_state.leaderboard.append({
            "name": display_name, "score": score,
            "total": len(st.session_state.questions),
            "time": time.time()
        })

        st.markdown("## 📊 Results")
        st.subheader(f"Your Score: **{score} / {len(details)}**")

        if score == len(details):
            st.success("🎉 PERFECT! You're an AI Mind Reader!")
        elif score >= len(details) * 0.75:
            st.success("🔥 Excellent! You can spot AI like a pro.")
        elif score >= len(details) * 0.5:
            st.info("🙂 Good job! You're improving.")
        else:
            st.warning("😅 The AI fooled you! Try again.")

        with st.expander("🔍 Detailed Review"):
            for text, user, correct, ok in details:
                css = "correct" if ok else "wrong"
                icon = "✔️" if ok else "❌"
                st.markdown(
                    f"<div class='box {css}'>{icon} <b>{text}</b><br/>"
                    f"Your answer: {user} | Correct: {correct}</div>",
                    unsafe_allow_html=True
                )

# ---------- LEADERBOARD ----------
if st.session_state.leaderboard:
    st.markdown("## 🏆 Leaderboard")
    board = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
    for i, p in enumerate(board[:10], 1):
        st.write(f"**{i}. {p['name']}** — {p['score']} / {p['total']}")
