import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ✅ 기본 폰트 설정 (웹 호환성 + 영어만 사용)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# ✅ Streamlit 앱 제목
st.title("📈 Kelly Criterion Capital Allocation Simulator")

# ✅ 사용자 입력
gain = st.number_input("📈 Gain per win (%)", value=200.0)
loss = st.number_input("📉 Loss per loss (%)", value=-100.0)
p_input = st.slider("🎯 Win rate (%)", 0.0, 100.0, 50.0)

# ✅ 켈리 공식 계산 (손익비 기준)
b = abs(gain / loss)  # 손익비 = 이익 / 손실
p = np.linspace(0.001, 0.999, 500)
q = 1 - p
f = (b * p - q) / b

# ✅ 현재 승률에 해당하는 f 계산
p_cur = p_input / 100
q_cur = 1 - p_cur
current_f = (b * p_cur - q_cur) / b * 100  # 퍼센트로 변환

# ✅ 그래프 그리기
fig, ax = plt.subplots()
ax.plot(p * 100, f * 100, label="Kelly allocation (%)")  # 퍼센트로 변환
ax.axvline(p_input, color='red', linestyle='--', label=f"Current win rate: {p_input:.2f}%")
ax.axhline(current_f, color='gray', linestyle='--', label=f"Recommended bet size: {current_f:.2f}%")
ax.set_xlabel("Win rate (%)")
ax.set_ylabel("Capital allocation (%)")
ax.set_title("📊 Kelly Optimal Capital Allocation by Win Rate")
ax.grid(True)
ax.legend()

# ✅ Streamlit에 그래프 출력
st.pyplot(fig)

