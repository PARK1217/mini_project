import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from logic_exchange import ExchangeLogic as logic

# 1. 페이지 설정 (와이드 모드 적용)
st.set_page_config(page_title="실시간 & 과거 환율 조회", page_icon="💱", layout="wide")

# 버튼 및 UI 스타일 커스텀
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white; border-radius: 12px; border: None; height: 3em;
        width: 100%; font-weight: 800; font-size: 18px;
        box-shadow: 0px 4px 15px rgba(0, 123, 255, 0.3);
    }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; }
    </style>
""", unsafe_allow_html=True)


# 캐싱 함수들
@st.cache_data(ttl=3600)
def get_cached_rates(date_obj): return logic.get_rates_by_date(date_obj)


@st.cache_data(ttl=3600)
def get_cached_weekly_trend(unit): return logic.get_weekly_trend(unit)


# ---------------------------------------------------------
# 2. 사이드바 영역: 모든 설정 컨트롤러를 이쪽으로!
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 조회 설정")

    # 날짜 선택
    target_date = st.date_input("📅 조회 날짜", value=datetime.now(), max_value=datetime.now())

    # 조회 실행 버튼
    fetch_trigger = st.button("🔍 데이터 가져오기", use_container_width=True)

    st.divider()

    # 계산기 설정 (미리 배치)
    st.subheader("🧮 계산기 옵션")
    calc_mode = st.radio("계산 방향", ["외화 ➡️ 원화", "원화 ➡️ 외화"])

    # [백엔드 팁] 데이터가 로드된 후에만 활성화될 통화 선택기
    selected_unit = "USD"  # 기본값

# ---------------------------------------------------------
# 3. 데이터 로직 처리
# ---------------------------------------------------------
if fetch_trigger:
    with st.spinner("데이터 동기화 중..."):
        data_pack = get_cached_rates(target_date)
        if data_pack:
            st.session_state.current_exchange = data_pack
            st.session_state.saved_user_date = target_date.strftime('%Y%m%d')
        else:
            st.error("데이터 로드 실패")

# ---------------------------------------------------------
# 4. 메인 렌더링 영역
# ---------------------------------------------------------
st.title("💱 글로벌 환율 대시보드")

if 'current_exchange' in st.session_state:
    ex_data = st.session_state.current_exchange
    rates = ex_data['rates']

    # 날짜 비교용 포맷 정리
    actual_date = str(ex_data['date']).replace("-", "")  # 예: 20260327
    requested_date = st.session_state.get('saved_user_date')  # 예: 20260330

    # 단, 날짜가 다를 때만 사용자에게 "왜 다른지" 살짝 알려줍니다.
    if actual_date != requested_date:
        # 주말이나 고시 전일 때만 나오는 안내
        st.info(f"ℹ️ 선택하신 날짜({requested_date})가 휴일이거나 고시 전이어서, 가장 가까운 영업일({actual_date}) 환율을 보여드립니다.")
    else:
        st.success(f"✅ **{actual_date}** 기준 환율 정보입니다.")

    # 상단 메트릭 전광판
    cols = st.columns(3)
    for i, code in enumerate(['USD', 'JPY', 'EUR']):
        info = rates.get(code)
        if info:
            cols[i].metric(f"{info['name']} ({code})", f"{info['rate']:,} KRW")

    # 메인 섹션: 계산기 & 그래프 (2컬럼 배치로 공간 활용)
    st.divider()
    left_col, right_col = st.columns([1, 1.5], gap="large")

    with left_col:
        st.subheader("🧮 환율 계산기")
        # 통화 목록 정렬 로직
        priority = ['USD', 'EUR', 'JPY']
        unit_list = priority + sorted([u for u in rates.keys() if u not in priority])

        with st.container(border=True):
            selected_unit = st.selectbox("대상 통화", unit_list, key="main_unit_selector")
            rate = rates[selected_unit]['rate']

            if calc_mode == "외화 ➡️ 원화":
                amt = st.number_input(f"{selected_unit} 금액", value=1.0, step=1.0)
                st.info(f"### {amt * rate:,.2f} KRW")
            else:
                amt = st.number_input("KRW 금액", value=10000.0, step=1000.0)
                res = amt / rate if rate > 0 else 0
                st.info(f"### {res:,.2f} {selected_unit}")

    with right_col:
        st.subheader(f"📈 {selected_unit} 주간 추이")
        weekly_data = get_cached_weekly_trend(selected_unit)
        if weekly_data:
            df = pd.DataFrame(weekly_data)
            fig = px.line(df, x='날짜', y='환율', markers=True, template="plotly_white")
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.caption("""
        ⚠️ **환율 정보 안내** * 본 서비스의 환율은 **한국수출입은행 API**를 통해 제공되는 **영업점 고시 환율**입니다.  
        * 구글이나 포털 사이트의 실시간 시장 환율(Mid-market)과는 데이터 소스 및 갱신 주기에 따라 차이가 발생할 수 있습니다.  
        * 실제 환전 및 송금 시에는 은행별 수수료가 포함된 전신환매도율(TTS) 또는 현찰매수율이 적용되므로 해당 금융기관에서 최종 확인하시기 바랍니다.
    """)

else:
    st.info("👈 왼쪽 사이드바에서 날짜를 선택하고 [데이터 가져오기]를 눌러주세요.")