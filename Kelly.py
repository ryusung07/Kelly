import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ✅ 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.title("📈 켈리 공식 자본 투입률 시뮬레이터")

# ✅ 거래 방향 선택
trade_direction = st.radio("📈 거래 방향", ["롱 (매수)", "숏 (매도)"], horizontal=True)

# ✅ 거래 방식 선택
mode = st.radio("⚙️ 거래 방식", ["교차", "격리"], horizontal=True)

# ✅ 진입가, 익절가, 손절가 입력
st.subheader("💰 매매 셋업")
entry_price = st.number_input("진입가", value=10000.0)
tp_price = st.number_input("익절가", value=12000.0)
sl_price = st.number_input("손절가", value=9000.0)

# ✅ 수익률 / 손실률 계산
if trade_direction == "롱 (매수)":
    profit_pct = ((tp_price - entry_price) / entry_price) * 100
    loss_pct = ((sl_price - entry_price) / entry_price) * 100
else:  # 숏 (매도)
    profit_pct = ((entry_price - tp_price) / entry_price) * 100
    loss_pct = ((entry_price - sl_price) / entry_price) * 100

gain = max(profit_pct, 0)
loss = min(loss_pct, 0)

# ✅ 손익비
rr_ratio = abs(gain / loss) if loss != 0 else 0
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"📈 수익률 = `{gain:.2f}%`")
with col2:
    st.markdown(f"📉 손실률 = `{loss:.2f}%`")

# ✅ 격리 모드일 경우: 청산스탑 레버리지 표시
if mode == "격리":
    if loss != 0:
        stop_lev = 100 / abs(loss)
        st.markdown(f"🧯 청산 스탑 레버리지: `{stop_lev:.2f}배`")

st.markdown(f"📊 손익비 = `{rr_ratio:.2f} : 1`")

# ✅ 승률 입력
p_input = st.slider("🎯 승률 (%)", 0.0, 100.0, 50.0, step=1.0)
p = p_input / 100
q = 1 - p

# ✅ Kelly 공식 계산
a = abs(loss / 100) if loss != 0 else 1e-6
b = gain / 100 if gain != 0 else 1e-6
kelly_f = max((p / a - q / b), 0)  # 음수일 경우 0 처리

# ✅ 기대값 EV 계산
ev = (p * b) + (q * -a)
st.markdown(f"📊 기대값 (EV): `{ev * 100:.2f}%`")

# ✅ Half Kelly 토글 (아래에 배치)
use_half_kelly = False  # 초기화 먼저 해두기 위해

if mode == "교차":
    f_display = kelly_f * 100
    st.subheader(f"💡 [교차] 자본 대비 투입률: `{f_display:.2f}%`")
else:
    liquidation_risk_pct = abs(loss / 100)
    isol_margin_ratio = kelly_f * liquidation_risk_pct * 100
    st.subheader(f"💡 [격리] 자산 대비 최적 투입률: `{isol_margin_ratio:.2f}%`")

# ✅ Half Kelly 토글 (한 줄 아래)
use_half_kelly = st.checkbox("🌓 Half Kelly", value=False)

# ✅ 하프 켈리 적용
if use_half_kelly:
    kelly_f *= 0.5
    label_suffix = " (Half Kelly ON)"
else:
    label_suffix = ""

# ✅ 그래프 데이터
p_array = np.linspace(0.001, 0.999, 500)
q_array = 1 - p_array
f_array = (p_array / a - q_array / b) * 100
f_array = np.maximum(f_array, 0)
if use_half_kelly:
    f_array *= 0.5

# ✅ 그래프 그리기
fig, ax = plt.subplots()
ax.plot(p_array * 100, f_array, label="Kelly allocation (%)")
ax.axvline(p_input, color='red', linestyle='--', label=f"Win rate: {p_input:.0f}%")

if mode == "교차":
    display_val = kelly_f * 100
else:
    display_val = kelly_f * (abs(loss / 100)) * 100

label_text = f"Bet size: {display_val:.0f}%{label_suffix}"
ax.axhline(display_val, color='gray', linestyle='--', label=label_text)

ax.set_xlabel("Win rate (%)")
ax.set_ylabel("Capital allocation (%)")
ax.set_title("Kelly Optimal Capital Allocation by Win Rate")
ax.grid(True)
ax.legend()

st.pyplot(fig)
