import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ✅ 한글 안 깨지게 기본 matplotlib 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'  # 웹 호환성 좋고 한글도 잘 보임
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 깨짐 방지

# ✅ Streamlit 앱 제목
st.title("📈 켈리 공식 자본 투입률 시뮬레이터")

# ✅ 사용자 입력
gain = st.number_input("📈 Gain per win (%)", value=200.0)
loss = st.number_input("📉 Loss per loss (%)", value=-100.0)
p_input = st.slider("🎯 Win rate (%)", 0.0, 100.0, 50.0, step=1.0)

# ✅ 켈리 공식 계산
b = gain / 100
l = abs(loss) / 100
p = np.linspace(0.001, 0.999, 500)
f = (b * p - (1 - p)) / b

# ✅ 현재 승률 기준의 자본 투입률 계산
current_f = ((b * (p_input / 100) - (1 - (p_input / 100))) / b) * 100

# ✅ 그래프 그리기
fig, ax = plt.subplots()
ax.plot(p * 100, f * 100, label="Kelly allocation (%)")
ax.axvline(p_input, color='red', linestyle='--', label=f"Current win rate: {p_input:.0f}%")
ax.axhline(current_f, color='gray', linestyle='--', label=f"Recommended bet size: {current_f:.0f}%")
ax.set_xlabel("Win rate (%)")
ax.set_ylabel("Capital allocation (%)")
ax.set_title("📊 Kelly Optimal Capital Allocation by Win Rate")
ax.grid(True)
ax.legend()

# ✅ Streamlit에 그래프 출력
st.pyplot(fig)
