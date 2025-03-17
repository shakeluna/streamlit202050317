import streamlit as st
import pandas as pd
import requests
import json
from urllib.parse import quote
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="스팀 게임 가격 비교 - 싸다게임",
    page_icon="🎮",
    layout="wide"
)

# 스타일 적용
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .price-highlight {
        color: #FF9900;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .store-name {
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("<h1 class='main-header'>스팀 게임 최저가 비교</h1>", unsafe_allow_html=True)

# Supabase API 정보
SUPABASE_URL = "https://zsslzoptwfunhkrplsbv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpzc2x6b3B0d2Z1bmhrcnBsc2J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQyODU3NDQsImV4cCI6MjAyOTg2MTc0NH0.6-QnGWhnY2ZshI6B2TPXReZNKyVLWJhyC0W9BwbviAM"

# 테이블 이름 가져오기 함수
def get_table_name(appid):
    ranges = [
        [1, 150000, "steamappid1"],
        [150001, 300000, "steamappid2"],
        [300001, 450000, "steamappid3"],
        [450001, 600000, "steamappid4"],
        [600001, 750000, "steamappid5"],
        [750001, 900000, "steamappid6"],
        [900001, 1050000, "steamappid7"],
        [1050001, 1200000, "steamappid8"],
        [1200001, 1350000, "steamappid9"],
        [1350001, 1500000, "steamappid10"],
        [1500001, 1650000, "steamappid11"],
        [1650001, 1800000, "steamappid12"],
        [1800001, 1950000, "steamappid13"],
        [1950001, 2100000, "steamappid14"],
        [2100001, 2250000, "steamappid15"],
        [2250001, 2400000, "steamappid16"],
        [2400001, 2550000, "steamappid17"],
        [2550001, 2700000, "steamappid18"],
        [2700001, 2850000, "steamappid19"],
        [2850001, 3000000, "steamappid20"]
    ]
    
    for min_val, max_val, table_name in ranges:
        if min_val <= appid <= max_val:
            return table_name
    return None

# 가격 데이터 가져오기 함수
def fetch_price_data(appid):
    table_name = get_table_name(appid)
    if not table_name:
        return None
    
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=id,store,game,steamappid,price,link&steamappid=eq.{appid}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            st.error(f"API 오류: {response.status_code}")
            return None
        
        data = response.json()
        if data:
            # 가격 기준으로 정렬
            return sorted(data, key=lambda x: x.get('price', float('inf')))
        return []
    
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        return None

# 스팀 게임 검색 함수
def search_steam_games(query):
    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={quote(query)}&l=korean&cc=kr"
        response = requests.get(url)
        
        if response.status_code != 200:
            st.error(f"스팀 API 오류: {response.status_code}")
            return []
        
        data = response.json()
        return data.get('items', [])
    
    except Exception as e:
        st.error(f"검색 오류: {str(e)}")
        return []

# 사이드바 - 게임 검색
with st.sidebar:
    st.header("게임 검색")
    search_query = st.text_input("게임 이름 입력")
    search_button = st.button("검색")
    
    st.markdown("---")
    st.header("또는 스팀 AppID 직접 입력")
    direct_appid = st.text_input("스팀 AppID")
    direct_button = st.button("가격 확인")
    
    st.markdown("---")
    st.markdown("### 인기 게임")
    popular_games = {
        "엘든 링": 1245620,
        "GTA 5": 271590,
        "스타듀 밸리": 413150,
        "사이버펑크 2077": 1091500,
        "발로란트": 2803680
    }
    
    for game_name, game_appid in popular_games.items():
        if st.button(game_name):
            direct_appid = game_appid
            direct_button = True

# 검색 결과 표시
if search_button and search_query:
    st.subheader(f"'{search_query}' 검색 결과")
    
    search_results = search_steam_games(search_query)
    if search_results:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.write("게임 이미지")
        with col2:
            st.write("게임 정보")
        with col3:
            st.write("액션")
        
        for result in search_results[:10]:  # 상위 10개 결과만 표시
            appid = result.get('id')
            name = result.get('name')
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if 'tiny_image' in result:
                    st.image(result['tiny_image'], width=120)
                else:
                    st.write("이미지 없음")
            
            with col2:
                st.write(f"**{name}**")
                if 'price' in result:
                    price_info = result['price']
                    if 'final' in price_info:
                        price = price_info['final'] / 100
                        st.write(f"스팀 가격: {price:,}원")
                
            with col3:
                if st.button(f"가격 비교", key=f"compare_{appid}"):
                    direct_appid = appid
                    direct_button = True
    else:
        st.info("검색 결과가 없습니다.")

# 가격 비교 결과 표시
if direct_button and direct_appid:
    try:
        appid = int(direct_appid)
        price_data = fetch_price_data(appid)
        
        if price_data:
            # 기본 게임 정보 표시
            game_name = price_data[0]['game']
            st.header(f"{game_name} 가격 비교")
            
            # 스팀 페이지 링크
            steam_url = f"https://store.steampowered.com/app/{appid}"
            st.markdown(f"[스팀 페이지에서 보기]({steam_url})")
            
            # 탭 생성
            tab1, tab2 = st.tabs(["가격 목록", "가격 차트"])
            
            with tab1:
                # 데이터 테이블 생성
                df = pd.DataFrame(price_data)
                
                # 가격 포맷팅
                df['formatted_price'] = df['price'].apply(lambda x: f"{x:,}원")
                
                # 테이블 표시
                st.dataframe(
                    df[['store', 'game', 'formatted_price', 'link']].rename(
                        columns={
                            'store': '스토어',
                            'game': '상품명',
                            'formatted_price': '가격',
                            'link': '링크'
                        }
                    ),
                    column_config={
                        "링크": st.column_config.LinkColumn("바로가기")
                    },
                    use_container_width=True
                )
                
                # 최저가 정보 하이라이트
                if len(price_data) > 0:
                    lowest_price = price_data[0]
                    st.markdown(f"""
                    <div class="card">
                        <h3>최저가 정보</h3>
                        <p>스토어: <span class="store-name">{lowest_price['store']}</span></p>
                        <p>상품명: {lowest_price['game']}</p>
                        <p>가격: <span class="price-highlight">{lowest_price['price']:,}원</span></p>
                        <a href="{lowest_price['link']}" target="_blank">
                            <button style="background-color: #FF9900; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">
                                최저가 스토어 이동
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                if price_data:
                    chart_df = pd.DataFrame([(item['store'], item['price']) for item in price_data], 
                                           columns=['스토어', '가격'])
                    fig = px.bar(
                        chart_df, 
                        x='스토어', 
                        y='가격',
                        title=f"{game_name} 스토어별 가격 비교",
                        color='스토어',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_layout(xaxis_title="스토어", yaxis_title="가격 (원)")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("차트를 표시할 데이터가 없습니다.")
        else:
            st.warning("이 게임의 가격 정보를 찾을 수 없습니다.")
    
    except ValueError:
        st.error("유효한 AppID를 입력해주세요.")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("© 2025 싸다게임 - 스팀 게임 최저가 비교 서비스")