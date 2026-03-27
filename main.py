import streamlit as st
import pandas as pd
import plotly.express as px  # 🔥 도넛 차트를 위해 추가

# 1. 페이지 설정
st.set_page_config(page_title="Python WorkSpace", page_icon="icon_test.png", layout="wide")
st.title("🏠 Python 실습 통합 대시보드")

# 2. 모든 세션 변수 초기화 (Prefix 구분)
if 'check_count' not in st.session_state:
    st.session_state.check_count = 0
    st.session_state.success_count = 0
    st.session_state.fail_count = 0

if 'uc_total' not in st.session_state:
    st.session_state.uc_total = 0
    st.session_state.uc_success = 0
    st.session_state.uc_fail = 0
    st.session_state.uc_history = {}  # {"길이": 5, "무게": 2} 형태

# 3. 리포트 레이아웃 구성
col_left, col_right = st.columns(2)

# [왼쪽: 패스워드 리포트] (기본 유지)
with col_left:
    with st.container(border=True):
        st.write("### 🔒 패스워드 체크 리포트")
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("성공", f"{st.session_state.success_count}회")
        c2.metric("실패", f"{st.session_state.fail_count}회")
        st.metric("총 검사 횟수", f"{st.session_state.check_count}회")

# [오른쪽: 단위 변환 리포트] (도넛 차트 적용)
with col_right:
    with st.container(border=True):
        st.write("### 🌡️ 단위 변환 리포트")
        st.divider()
        c3, c4, c5 = st.columns(3)
        c3.metric("성공", f"{st.session_state.uc_success}회")
        c4.metric("실패", f"{st.session_state.uc_fail}회")
        c5.metric("총 시도", f"{st.session_state.uc_total}회")

        st.divider()
        st.write("🍩 **카테고리별 이용 비중**")

        if st.session_state.uc_history:
            # 1. 데이터프레임 생성
            df = pd.DataFrame(
                list(st.session_state.uc_history.items()),
                columns=['Category', 'Count']
            )

            # 2. Plotly 도넛 차트 생성
            fig = px.pie(df, values='Count', names='Category', hole=0.5,
                         color_discrete_sequence=px.colors.sequential.RdBu)

            # 3. 차트 레이아웃 조정 (여백 및 범례 위치)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)

            # 4. 차트 출력
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("변환 기록이 아직 없습니다.")