import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.font_manager as fm
#import platform

# ✅ 한글 폰트 설정
#if platform.system() == 'Windows':
#    font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우용
#elif platform.system() == 'Darwin':
#    font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'  # 맥OS용
#else:
#    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 리눅스용 (Nanum Gothic 설치 필요)

#font_name = fm.FontProperties(fname=font_path).get_name()
#plt.rc('font', family=font_name)
#plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# ✅ Streamlit 앱 본문
st.title("📈 켈리 공식 자본 투입률 시뮬레이터")

gain = st.number_input("📈 이익률 (%)", value=300.0)
loss = st.number_input("📉 손실률 (%)", value=-100.0)
p_input = st.slider("🎯 현재 승률 (%)", 0.0, 100.0, 40.0)

b = gain / 100
l = abs(loss) / 100
p = np.linspace(0.001, 0.999, 500)
f = (b * p - (1 - p)) / b

fig, ax = plt.subplots()
ax.plot(p * 100, f * 100, label="켈리 자본 투입률 (%)")
ax.axvline(p_input, color='red', linestyle='--', label=f"현재 승률: {p_input:.2f}%")
current_f = ((b * (p_input/100) - (1 - (p_input/100))) / b) * 100
ax.axhline(current_f, color='gray', linestyle='--', label=f"투입률: {current_f:.2f}%")
ax.set_xlabel("승률 (%)")
ax.set_ylabel("자본 투입률 (%)")
ax.set_title("📊 승률에 따른 켈리 공식 자본 투입률")
ax.grid(True)
ax.legend()

st.pyplot(fig)
