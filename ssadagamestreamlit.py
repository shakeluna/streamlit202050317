import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# 간단한 홈페이지로 시작
st.title("스팀 게임 최저가 검색기 - 싸다게임")

# 기본 테스트 페이지
st.write("앱이 성공적으로 로드되었습니다!")
st.write("게임 검색을 시작하려면 사이드바를 사용하세요.")

# 간단한 예제 표시
st.subheader("인기 게임")
games = {
    "엘든 링": 1245620,
    "GTA 5": 271590,
    "스타듀 밸리": 413150
}

for name, appid in games.items():
    st.write(f"{name} - AppID: {appid}")
