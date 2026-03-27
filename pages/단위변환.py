import streamlit as st
from logic_converter import UnitConverter

st.title("🌡️ 만능 단위 변환기")

# 1. 카테고리 선택 (백엔드에서 정의한 키 리스트를 그대로 가져옴)
# uc.UNITS.keys() 등을 활용하면 백엔드 수정 시 프론트는 자동 반영됨.
categories = ["길이", "무게", "온도", "데이터 크기", "부동산 넓이", "시간"]
category = st.selectbox("어떤 단위를 변환할까요?", categories)

# 2. 카테고리에 맞는 단위 리스트 가져오기
# 실제로는 UnitConverter.get_units(category) 같은 메서드를 호출하는 것이 가장 보기 좋음.
units_map = {
    "길이": ["mm", "cm", "m", "km", "inch", "ft", "yd", "mile", "자"],
    "무게": ["mg", "g", "kg", "t", "oz", "lb", "돈", "근", "관"],
    "온도": ["°C (섭씨)", "°F (화씨)", "K (켈빈)"],
    "데이터 크기": ["bit", "B", "KB", "MB", "GB", "TB", "PB"],
    "부동산 넓이": ["m2", "py", "ac", "ha", "sq_ft"],
    "시간": ["ms", "s", "min", "h", "d", "week"]
}
current_units = units_map[category]

# 3. 공통 UI 레이아웃 (반복 없이 딱 한 번만 작성!)
st.subheader(f"✨ {category} 단위 변환기")

with st.container(border=True):
    st.write("📥 **입력**")
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        val = st.number_input("값", value=1.0)
    with col2:
        u_from = st.selectbox("시작 단위", current_units, key="from")

st.markdown("<h3 style='text-align: center;'>🔽</h3>", unsafe_allow_html=True)

with st.container(border=True):
    u_to = st.selectbox("변환할 단위", current_units, key="to")
    st.write("☑️ **출력**")

    # 4. 백엔드 호출 (카테고리만 던지면 백엔드가 알아서 계산)
    result = UnitConverter.convert(category, val, u_from, u_to)
    st.info(f"### 계산 결과: {result} {u_to}")