import streamlit as st
import json
import re

from voice_engine import transcribe_audio
from ai_feedback import get_feedback


st.set_page_config(
    page_title="AI Voice Assistant for Students",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Voice Assistant for Students")
st.write("Practice your viva answers and get instant AI feedback.")


# Load question bank
with open("questions.json", "r") as file:
    question_bank = json.load(file)


# Select subject
category = st.selectbox(
    "📚 Select Subject",
    list(question_bank.keys())
)


# Select question
question = st.selectbox(
    "❓ Select Viva Question",
    question_bank[category]
)


# Record answer
audio = st.audio_input("🎙️ Record your answer")


if audio:

    st.success("Voice recorded successfully! ✅")
    st.audio(audio)

    if st.button("🚀 Evaluate My Answer"):

        # Speech to text
        with st.spinner("🎙️ Converting voice to text..."):
            text = transcribe_audio(audio)

        st.subheader("📝 Your Answer")
        st.info(text)

        # Gemini evaluation
        with st.spinner("🤖 AI is evaluating your answer..."):
            feedback = get_feedback(question, text)

        st.divider()
        st.header("📊 AI Evaluation")


        # ---------------- SCORE ----------------

        score_match = re.search(
            r"Score:\s*(\d+)\s*/\s*10",
            feedback,
            re.IGNORECASE
        )

        if score_match:
            score = int(score_match.group(1))

            st.subheader("⭐ Score")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Your Score",
                    value=f"{score}/10"
                )

            with col2:
                if score >= 8:
                    st.success("Excellent! 🎉")
                elif score >= 5:
                    st.warning("Good, but can improve 👍")
                else:
                    st.error("Needs improvement 📚")


        # ---------------- CORRECT POINTS ----------------

        st.subheader("✅ Correct Points")

        correct_match = re.search(
            r"Correct Points:\s*(.*?)(?=\n\s*Mistakes:|\Z)",
            feedback,
            re.IGNORECASE | re.DOTALL
        )

        if correct_match:
            correct_text = correct_match.group(1).strip()

            for line in correct_text.splitlines():
                line = line.strip()

                if line.startswith("-"):
                    st.success(line[1:].strip())


        # ---------------- MISTAKES ----------------

        st.subheader("❌ Mistakes")

        mistakes_match = re.search(
            r"Mistakes:\s*(.*?)(?=\n\s*Suggestions:|\Z)",
            feedback,
            re.IGNORECASE | re.DOTALL
        )

        if mistakes_match:
            mistakes_text = mistakes_match.group(1).strip()

            for line in mistakes_text.splitlines():
                line = line.strip()

                if line.startswith("-"):
                    st.error(line[1:].strip())


        # ---------------- SUGGESTIONS ----------------

        st.subheader("💡 Suggestions")

        suggestions_match = re.search(
            r"Suggestions:\s*(.*?)(?=\n\s*Model Answer:|\Z)",
            feedback,
            re.IGNORECASE | re.DOTALL
        )

        if suggestions_match:
            suggestions_text = suggestions_match.group(1).strip()

            for line in suggestions_text.splitlines():
                line = line.strip()

                if line.startswith("-"):
                    st.info(line[1:].strip())


        # ---------------- MODEL ANSWER ----------------

        st.subheader("📖 Model Answer")

        model_match = re.search(
            r"Model Answer:\s*(.*)",
            feedback,
            re.IGNORECASE | re.DOTALL
        )

        if model_match:
            model_answer = model_match.group(1).strip()

            st.success(model_answer)


        st.divider()

        st.caption(
            "🤖 Feedback generated using Gemini AI | "
            "🎙️ Speech recognition powered by Faster-Whisper"
        )