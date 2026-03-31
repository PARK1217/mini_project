import streamlit as st
import os   # 폴더 존재 여부 확인 및 파일 탐색을 위해 추가
from logic_loader import DocumentLoader as loader

# 1. 페이지 설정 (반드시 최상단)
st.set_page_config(page_title="스마트 로컬 문서 검색기", page_icon="📄", layout="wide")

st.title("📄 스마트 로컬 문서 검색기")

# 2. 세션 히스토리 초기화
if 'path_history' not in st.session_state:
    st.session_state.path_history = ["./data"]

# 3. 사이드바 설정 영역
with st.sidebar:
    st.header("📂 탐색 설정")

    # 최근 경로 선택
    selected_path = st.selectbox(
        "탐색 폴더 선택",
        options=st.session_state.path_history,
        help="이전에 검색했던 경로들이 표시됩니다."
    )

    # 새로운 경로 등록
    with st.expander("➕ 새 경로 추가 및 등록"):
        new_path = st.text_input("폴더 경로 직접 입력", placeholder="C:/logs/project")
        if st.button("히스토리에 등록", use_container_width=True):
            if new_path and new_path not in st.session_state.path_history:
                if os.path.isdir(new_path):
                    st.session_state.path_history.insert(0, new_path)
                    st.success("등록 완료!")
                    st.rerun()
                else:
                    st.error("존재하지 않는 폴더입니다.")

    # 사이드바에 키워드 입력과 버튼 배치
    keyword = st.text_input("🔍 검색 키워드", placeholder="검색어를 입력하세요")
    search_clicked = st.button("🚀 검색 실행", use_container_width=True)

    # 확장자 필터 및 문맥 설정
    ext_options = ['.txt', '.log', '.java', '.py', '.xml', '.yml']
    selected_exts = st.multiselect("필터링 확장자", options=ext_options, default=['.txt', '.log'])
    context_val = st.slider("앞뒤 문맥 범위 (줄)", 0, 30, 2)

    

# 4. 메인 콘텐츠 영역: 검색 로직 실행
if search_clicked: # 버튼이 클릭되었을 때만 실행
    if keyword and selected_exts:
        with st.spinner("파일 분석 중..."):
            # 로직 호출
            all_docs = loader.load_documents(selected_path, selected_exts)
            results = loader.search_with_context(all_docs, keyword, context_val)

            if results:
                st.subheader(f"🎯 검색 결과 ({len(results)}건)")
                for res in results:
                    with st.container(border=True):
                        st.caption(f"📂 {res['file']} (Line: {res['line']})")
                        st.code(res['text'], language="text")
            else:
                st.warning(f"'{keyword}'에 대한 결과가 없습니다.")
    else:
        st.error("사이드바에서 키워드와 확장자를 모두 확인해 주세요.")
else:
    # 검색 전 초기 화면 안내
    st.info("👈 왼쪽 사이드바에서 경로를 선택하고 키워드를 입력한 뒤 [검색 실행] 버튼을 눌러주세요.")