import streamlit as st
import openai

# OpenAI API 키
openai.api_key = "YOUR_API_KEY"

st.title("📘 AI 출제기 (교재 기반)")

# 교재 내용 입력
context = st.text_area("✍️ 교재 내용을 붙여 넣으세요:", height=200)

# 세션 상태 초기화
if "question" not in st.session_state:
    st.session_state["question"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []

# 문제 출제
if st.button("문제 출제") and context:
    prompt = f"""
    아래 교재 내용을 참고하여 중2 과학 수준의 문제를 하나 출제해 주세요.
    문제는 교재 내용 안에서만 출제해야 하며, 간단하고 명확하게 작성하세요.

    교재 내용:
    {context}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    st.session_state["question"] = response["choices"][0]["message"]["content"]

# 문제 출력
if st.session_state["question"]:
    st.subheader("📢 AI 출제 문제:")
    st.write(st.session_state["question"])

    # 답 입력
    answer = st.text_input("✍️ 답을 입력하세요:")

    if st.button("제출") and answer:
        # 채점/피드백
        feedback_prompt = f"""
        교재 내용:
        {context}

        문제: {st.session_state['question']}
        학생 답: {answer}

        위 답이 맞는지 교재 내용 근거로 채점하고, 간단히 설명을 추가하세요.
        """
        feedback_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": feedback_prompt}]
        )
        feedback = feedback_response["choices"][0]["message"]["content"]

        # 기록 저장
        st.session_state["history"].append({
            "question": st.session_state["question"],
            "answer": answer,
            "feedback": feedback
        })

        # 다음 문제 위해 초기화
        st.session_state["question"] = None

# 이전 기록 출력
if st.session_state["history"]:
    st.subheader("📜 문제 기록")
    for i, item in enumerate(st.session_state["history"], 1):
        st.markdown(f"**문제 {i}:** {item['question']}")
        st.markdown(f"✍️ 답: {item['answer']}")
        st.markdown(f"✅ AI 피드백: {item['feedback']}")
        st.markdown("---")
