import streamlit as st
from logic_converter import UnitConverter

st.title("🌡️ 만능 단위 변환기")

MAIN_FACTORS = {}
category = st.selectbox("어떤 단위를 변환할까요?", ["길이", "무게", "온도", "데이터 크기", "부동산 넓이", "시간"])

# match-case 사용
match category:
    case "길이":
        st.subheader("📐 길이 단위 변환기")
        # 입력 영역
        with st.container(border=True):  # 테두리가 생기면서 하나의 그룹으로 보입니다.
            st.write("📥 **입력**")
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
            with col1:
                val = st.number_input("값", value=1.0)
            with col2:
                u_from = st.selectbox("단위", ["mm", "cm", "m", "km", "inch", "ft", "yd", "mile", "자"], key="from")

        st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

        # 출력 영역
        with st.container(border=True):
            u_to = st.selectbox("변환할 단위", ["mm", "cm", "m", "km", "inch", "ft", "yd", "mile", "자"], key="to")

            st.write("☑️ **출력**")
            # 실제 계산 호출 (static 또는 class method 호출 방식)
            result = UnitConverter.convert(category, val, u_from, u_to)
            # 2. 결과값을 화면에 뿌려줍니다.
            st.info(f"### 계산 결과: {result} {u_to}")

    case "무게":
        st.subheader("⚖️ 무게 단위 변환기")
        # 입력영역
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
            with col1:
                val = st.number_input("값", value=1.0)
            with col2:
                u_from = st.selectbox("단위", ["mg", "g", "kg", "t", "oz", "lb", "돈", "근", "관"], key="from")

        st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

        # 출력 영역
        with st.container(border=True):
            u_to = st.selectbox("변환할 단위", ["mg", "g", "kg", "t", "oz", "lb", "돈", "근", "관"], key="to")

            st.write("☑️ **출력**")
            # 실제 계산 호출 (static 또는 class method 호출 방식)
            result = UnitConverter.convert(category, val, u_from, u_to)
            # 2. 결과값을 화면에 뿌려줍니다.
            st.info(f"### 계산 결과: {result} {u_to}")

    case "온도":
        st.subheader("🌡️ 온도 단위 변환기")
        # 입력영역
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
            with col1:
                val = st.number_input("값", value=1.0)
            with col2:
                u_from = st.selectbox("단위", ["°C (섭씨)", "°F (화씨)", "K (켈빈)"], key="from")

            st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

            # 출력 영역
            with st.container(border=True):
                u_to = st.selectbox("단위", ["°C (섭씨)", "°F (화씨)", "K (켈빈)"], key="to")

                st.write("☑️ **출력**")
                # 실제 계산 호출 (static 또는 class method 호출 방식)
                result = UnitConverter.convert(category, val, u_from, u_to)
                # 2. 결과값을 화면에 뿌려줍니다.
                st.info(f"### 계산 결과: {result} {u_to}")

    case "데이터 크기":
        st.subheader("💾 데이터 단위 변환기")
        # 입력영역
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            val = st.number_input("값", value=1.0)
        with col2:
            u_from = st.selectbox("단위", ["bit", "B", "KB", "MB", "GB", "TB", "PB"], key="from")

        st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

        # 출력 영역
        with st.container(border=True):
            u_to = st.selectbox("단위", ["bit", "B", "KB", "MB", "GB", "TB", "PB"], key="to")

            st.write("☑️ **출력**")
            # 실제 계산 호출 (static 또는 class method 호출 방식)
            result = UnitConverter.convert(category, val, u_from, u_to)
            # 2. 결과값을 화면에 뿌려줍니다.
            st.info(f"### 계산 결과: {result} {u_to}")

    case "부동산 넓이":
        st.subheader("🏘️ 부동산 넓이 단위 변환기")
        # 입력영역
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            val = st.number_input("값", value=1.0)
        with col2:
            u_from = st.selectbox("단위", ["m2", "py", "ac", "ha", "sq_ft"], key="from")

        st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

        # 출력 영역
        with st.container(border=True):
            u_to = st.selectbox("단위", ["m2", "py", "ac", "ha", "sq_ft"], key="to")

            st.write("☑️ **출력**")
            # 실제 계산 호출 (static 또는 class method 호출 방식)
            result = UnitConverter.convert(category, val, u_from, u_to)
            # 2. 결과값을 화면에 뿌려줍니다.
            st.info(f"### 계산 결과: {result} {u_to}")

    case "시간":
        st.subheader("⏰ 시간 단위 변환기")
        # 입력영역
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            val = st.number_input("값", value=1.0)
        with col2:
            u_from = st.selectbox("단위", ["ms", "s", "min", "h", "d", "week"], key="from")

        st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

        # 출력 영역
        with st.container(border=True):
            u_to = st.selectbox("단위", ["ms", "s", "min", "h", "d", "week"], key="to")

            st.write("☑️ **출력**")
            # 실제 계산 호출 (static 또는 class method 호출 방식)
            result = UnitConverter.convert(category, val, u_from, u_to)
            # 2. 결과값을 화면에 뿌려줍니다.
            st.info(f"### 계산 결과: {result} {u_to}")