import streamlit as st
from logic_converter import UnitConverter as uc

# 1. 세션 상태 방어 코드
if 'uc_total' not in st.session_state:
    st.session_state.uc_total = 0
    st.session_state.uc_success = 0
    st.session_state.uc_fail = 0
    st.session_state.uc_history = {}

st.title("🌡️ 만능 단위 변환기")

categories = uc.get_categories()
category = st.selectbox("어떤 단위를 변환할까요?", categories)
current_units = uc.get_units(category)

st.subheader(f"✨ {category} 단위 변환기")

# 입력 영역
with st.container(border=True):
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        val = st.number_input("값 입력", value=1.0)
    with col2:
        u_from = st.selectbox("시작 단위", current_units, key="from_u")

st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

# 출력 및 실행 영역
with st.container(border=True):
    u_to = st.selectbox("변환할 단위", current_units, key="to_u")

    # 🔥 [수정] 버튼을 눌렀을 때만 로직 실행
    if st.button("변환하기", use_container_width=True):
        result = uc.convert(category, val, u_from, u_to)

        # 세션 카운트 업데이트 (버튼 클릭 시에만 실행됨)
        st.session_state.uc_total += 1

        if result is not None:
            st.session_state.uc_success += 1
            st.session_state.uc_history[category] = st.session_state.uc_history.get(category, 0) + 1
            st.success(f"### 결과: {result} {u_to}")
        else:
            st.session_state.uc_fail += 1
            st.error("⚠️ 변환 실패: 지원하지 않는 조합입니다.")
    else:
        st.info("변환할 값을 입력하고 버튼을 눌러주세요.")