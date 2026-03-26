import streamlit as st

# 1. 페이지 설정, 제목, 아이콘
st.set_page_config(page_title= "Python WorkSpace", page_icon= "icon_test.png", layout="centered")
st.title("🏠 Python 실습 메인")



# 2. 세션저장소 초기화(새로고침 전까지는 데이터, 페이지 유지가능)
if 'check_count' not in st.session_state:
    st.session_state.check_count = 0
    st.session_state.success_count = 0
    st.session_state.fail_count = 0

# col1, col2 = st.columns(2)
# with col1:
#     st.metric(
#         label="🔒비밀번호 검사 횟수",
#         value=f"{st.session_state.check_count}회"
#     )
#
# with col2:
#     # 예시: 평균 점수 같은 추가 지표
#     st.metric(label="✨ 평균 보안 점수", value="85점", delta="5점 상승")

with st.container(border=True): # 테두리가 있는 박스 생성
    st.write("### 📊 패스워드 체크 리포트")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("성공한 검사 횟수", f"{st.session_state.success_count}회")
    with col2:
        st.metric("실패한 검사 횟수", f"{st.session_state.fail_count}회")
    st.divider()
    st.metric("총 검사 횟수", f"{st.session_state.check_count}회")

