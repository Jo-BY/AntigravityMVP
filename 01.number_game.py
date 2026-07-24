import sys
import os

# AppData user site-packages 경로 자동 추가
user_site = os.path.expanduser(r"~\AppData\Roaming\Python\Python314\site-packages")
if user_site not in sys.path and os.path.exists(user_site):
    sys.path.insert(0, user_site)

import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="🎯 숫자 맞추기 게임",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS로 스타일링 강화
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .hint-box-up {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        color: #1B5E20;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    .hint-box-down {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        border-radius: 8px;
        color: #0D47A1;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    .success-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFC107;
        padding: 1.2rem;
        border-radius: 8px;
        color: #B78103;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
    }
    .history-badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-up { background-color: #C8E6C9; color: #2E7D32; }
    .badge-down { background-color: #BBDEFB; color: #1565C0; }
    .badge-correct { background-color: #FFE082; color: #E65100; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'best_score' not in st.session_state:
    st.session_state.best_score = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'history' not in st.session_state:
    st.session_state.history = []
if 'message' not in st.session_state:
    st.session_state.message = None

def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.message = None

# Header Section
st.markdown('<div class="main-title">🎯 숫자 맞추기 게임</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">1부터 100 사이의 비밀 숫자를 찾아보세요!</div>', unsafe_allow_html=True)

# Welcome Card
st.markdown("""
<div class="welcome-card">
    <h3>👋 환영합니다!</h3>
    <p>최소 시도 횟수로 성공하는 것이 목표입니다. 숫자를 입력하고 결과를 확인해보세요!</p>
</div>
""", unsafe_allow_html=True)

# Metrics Section (현재 시도 횟수 & 최고 기록)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🔢 현재 시도 횟수", value=f"{st.session_state.attempts} 회")
with col2:
    best_display = f"{st.session_state.best_score} 회" if st.session_state.best_score is not None else "없음"
    st.metric(label="🏆 최소 시도 (최고 기록)", value=best_display)

st.divider()

# Game Input & Action Form
if not st.session_state.game_over:
    with st.form(key='guess_form', clear_on_submit=True):
        guess_input = st.number_input(
            "숫자를 입력하세요 (1~100):",
            min_value=1,
            max_value=100,
            step=1,
            value=50
        )
        submit_button = st.form_submit_button(label="🎯 정답 확인", use_container_width=True)

    if submit_button:
        st.session_state.attempts += 1
        guess = int(guess_input)
        target = st.session_state.target_number

        if guess < target:
            st.session_state.message = ("UP", f"📈 UP! {guess}보다 더 큰 숫자입니다.")
            st.session_state.history.append({"guess": guess, "result": "UP", "icon": "📈"})
        elif guess > target:
            st.session_state.message = ("DOWN", f"📉 DOWN! {guess}보다 더 작은 숫자입니다.")
            st.session_state.history.append({"guess": guess, "result": "DOWN", "icon": "📉"})
        else:
            st.session_state.game_over = True
            st.session_state.message = ("CORRECT", f"🎉 정답입니다! {st.session_state.attempts}번 만에 맞추셨습니다!")
            st.session_state.history.append({"guess": guess, "result": "CORRECT", "icon": "🎉"})
            
            # 최고 기록 갱신 여부
            if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
                st.session_state.best_score = st.session_state.attempts
                st.balloons()
            st.rerun()

# Result Message Display
if st.session_state.message:
    msg_type, msg_text = st.session_state.message
    if msg_type == "UP":
        st.markdown(f'<div class="hint-box-up">{msg_text}</div>', unsafe_allow_html=True)
    elif msg_type == "DOWN":
        st.markdown(f'<div class="hint-box-down">{msg_text}</div>', unsafe_allow_html=True)
    elif msg_type == "CORRECT":
        st.markdown(f'<div class="success-box">{msg_text}</div>', unsafe_allow_html=True)
        if st.session_state.best_score == st.session_state.attempts:
            st.success(f"🌟 새로운 최고 기록 달성! ({st.session_state.best_score}회)")

# Game Over / Retry Option
if st.session_state.game_over:
    st.write("")
    st.subheader("🎮 게임이 종료되었습니다!")
    col_reset, col_space = st.columns([1, 1])
    with col_reset:
        if st.button("🔄 다시 시도하기 (새 게임)", type="primary", use_container_width=True):
            reset_game()
            st.rerun()

# History Section
if st.session_state.history:
    st.write("")
    st.markdown("### 📜 이전 시도 기록")
    badges_html = ""
    for item in st.session_state.history:
        res = item["result"]
        badge_class = "badge-up" if res == "UP" else ("badge-down" if res == "DOWN" else "badge-correct")
        badges_html += f'<span class="history-badge {badge_class}">{item["icon"]} {item["guess"]} ({res})</span>'
    st.markdown(badges_html, unsafe_allow_html=True)
