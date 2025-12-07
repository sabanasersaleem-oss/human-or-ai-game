import streamlit as st
import os
import random
import time

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="AI vs Human — Image Game",
    page_icon="🧠",
    layout="centered"
)

# ---------------------------------
# CUSTOM CSS
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

h1, h2, h3 {
    text-align:center;
    color: var(--purple);
    font-weight:900;
}

.result-box {
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
# TITLE
# ---------------------------------
st.markdown("<h1>🧠 AI vs Human — Image Detection Game</h1>", unsafe_allow_html=True)
st.write("Can you guess if the image was created by a **Human** or **Artificial Intelligence**?")

# ---------------------------------
# IMAGE FOLDERS
# ---------------------------------
AI_FOLDER = "images/ai"
HUMAN_FOLDER = "images/human"

ai_images = [os.path.join(AI_FOLDER, img) for img in os.listdir(AI_FOLDER)]
human_images = [os.path.join(HUMAN_FOLDER, img) for img in os.listdir(HUMAN_FOLDER)]

all_images = [(img, "AI") for img in ai_images] + [(img, "Human") for img in human_images]
random.shuffle(all_images)

# ---------------------------------
# SESSION STATE INIT
# ---------------------------------
if "index" not in st.session_state: st.session_state.index = 0
if "score" not in st.session_state: st.session_state.score = 0
if "leaderboard" not in st.session_state: st.session_state.leaderboard = []
if "player" not in st.session_state: st.session_state.player = ""

# ---------------------------------
# SIDEBAR (Settings)
# ---------------------------------
with st.sidebar:
    st.header("🎮 Game Settings")
    name = st.text_input("Player Name:", placeholder="Enter your name")

    if st.button("Save Name"):
        st.session_state.player = name if name.strip() else "Anonymous"
        st.success(f"Welcome, {st.session_state.player}!")

    if st.button("Restart Game"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()

# ---------------------------------
# GAME LOGIC
# ---------------------------------
if st.session_state.index < len(all_images):

    img_path, correct_answer = all_images[st.session_state.index]
    st.image(img_path, use_column_width=True)

    guess = st.radio("Your guess:", ["Human", "AI"])

    if st.button("Submit Answer"):
        if guess == correct_answer:
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Wrong! It was: **{correct_answer}** 😅")

        st.session_state.index += 1
        time.sleep(0.8)
        st.rerun()

else:
    st.subheader(f"🏁 Final Score: {st.session_state.score} / {len(all_images)}")
    st.balloons()

    st.session_state.leaderboard.append({
        "name": st.session_state.player or "Anonymous",
        "score": st.session_state.score,
        "total": len(all_images),
        "time": time.time()
    })

    if st.button("Play Again"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()

# ---------------------------------
# LEADERBOARD
# ---------------------------------
if st.session_state.leaderboard:
    st.markdown("## 🏆 Leaderboard (Local Session)")
    sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)

    for i, entry in enumerate(sorted_board[:10], start=1):
        st.write(f"**{i}. {entry['name']}** — {entry['score']} / {entry['total']}")
