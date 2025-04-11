import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ✅ 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.title("📈 켈리 공식 자본 투입률 시뮬레이터")

# ✅ 진입가, 익절가, 손절가 입력
st.subheader("💰 가격 기반 손익비 자동 계산")
entry_price = st.number_input("진입가", value=10000.0)
tp_price = st.number_input("익절가", value=12000.0)
sl_price = st.number_input("손절가", value=9000.0)

# ✅ 손익비 기반 수익률/손실률 계산
profit_pct = ((tp_price - entry_price) / entry_price) * 100
loss_pct = ((sl_price - entry_price) / entry_price) * 100

# ✅ 수익률은 0보다 작으면 0, 손실률은 0보다 크면 0
gain = max(profit_pct, 0)
loss = min(loss_pct, 0)

# ✅ 계산된 손익비 출력
st.markdown(f"📊 손익비 = `{abs(gain / loss):.2f} : 1`")
st.markdown(f"📈 수익률 = `{gain:.2f}%`, 📉 손실률 = `{loss:.2f}%`")

# ✅ 승률 입력 (정수 단위)
p_input = st.slider("🎯 승률 (%)", 0.0, 100.0, 50.0, step=1.0)

# ✅ 켈리 공식 계산
b = gain / 100
l = abs(loss) / 100
p = np.linspace(0.001, 0.999, 500)
f = (b * p - (1 - p)) / b
current_f = ((b * (p_input / 100) - (1 - (p_input / 100))) / b) * 100

# ✅ 그래프
fig, ax = plt.subplots()
ax.plot(p * 100, f * 100, label="Kelly allocation (%)")
ax.axvline(p_input, color='red', linestyle='--', label=f"Current win rate: {p_input:.0f}%")
ax.axhline(current_f, color='gray', linestyle='--', label=f"Recommended bet size: {current_f:.0f}%")
ax.set_xlabel("Win rate (%)")
ax.set_ylabel("Capital allocation (%)")
ax.set_title("📊 Kelly Optimal Capital Allocation by Win Rate")
ax.grid(True)
ax.legend()

st.pyplot(fig)
