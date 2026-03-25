import streamlit as st

from logic_password import check_pw_security

st.set_page_config(page_title= "Python WorkSpace", page_icon= "icon_test.png", layout="centered")
if "check_count" not in st.session_state:
    st.session_state.check_count = 0
    st.session_state.success_count = 0
    st.session_state.fail_count = 0

st.title("Password Check")
pw = st.text_input("체크할 비밀번호 입력", type="password")

if st.button("검사하기") :
    #logic_password 호출
    res = check_pw_security(pw)
    st.session_state.check_count += 1

    # [1단계] 금지된 문자가 섞였는지 (보안 위협)
    if res["forbidden"]:
        st.session_state.fail_count += 1
        st.error("⛔ 허용되지 않은 문자(공백, 한글 등)가 포함되어 있습니다.")

    # [2단계] 금지된 건 없지만, 조건이 하나라도 누락되었는지 (dkssud 케이스)
    elif res["score"] < 100:
        st.session_state.fail_count += 1
        st.warning("⚠️ 보안 등급이 낮습니다. 다음 조건을 충족해주세요.")

        # 상세 미충족 조건 나열
        if not res["length"]:
            st.info("📏 최소 10자 이상 (현재: {}자)".format(len(pw)))
        if not res["upper"]:
            st.info("🔠 대문자 1개 이상 포함 필요")
        if not res["special"]:
            st.info("🔑 특수문자(!@#$%^*()_+-=) 1개 이상 포함 필요")

    # [3단계] 모든 조건 만족
    else:
        st.session_state.success_count += 1
        st.success("✅ 안전한 비밀번호입니다! (100점)")

# 논리적 모순이 있어 로직 재구성필요( dkssud의 경우 길이,대문자,특수문자 누락이지만 쓰지도 않은 특수문자가 이미 포함되어있다고 나오면 오해요지가 있어보임
    # if res["score"] == 100:
    #     st.success("👍 완벽한 비밀번호입니다.!")
    # else:
    #     st.error("보안등급이 낮습니다.")
    #
    #     #상세사유
    #     with st.expander("상세 미충족 조건 확인"):
    #         if not res["length"] :
    #             st.warning("⚠️ 최소 10자 이상이어야 합니다.")
    #         if not res["upper"] :
    #             st.warning("️️⚠️ 대문자가 최소 1개 이상 포함되어야 합니다.")
    #         if not res["special"] :
    #             st.warning("⚠️ 허용된 특수문자는 !@#$%^*()_+-= 입니다.")
    #         if not res["forbidden"] :
    #             st.error("⛔ 허용되지 않은 특수문자가 포함되어 있습니다.")
