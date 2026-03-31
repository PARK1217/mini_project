import os


class DocumentLoader:
    @staticmethod
    def load_documents(directory, extensions):
        """지정된 확장자만 필터링하여 읽기"""
        docs = []
        if not os.path.exists(directory):
            return docs

        for filename in os.listdir(directory):
            # 사용자가 선택한 확장자 중 하나로 끝나는지 확인
            if any(filename.lower().endswith(ext.strip().lower()) for ext in extensions):
                try:
                    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                        docs.append({"name": filename, "content": f.read()})
                except Exception:
                    continue  # 읽기 권한 등 예외 발생 시 스킵
        return docs

    @staticmethod
    def search_with_context(docs, keyword, context_lines):
        """키워드 검색 및 앞뒤 n줄 추출"""
        results = []
        for doc in docs:
            lines = doc['content'].split('\n')
            for i, line in enumerate(lines):
                if keyword.lower() in line.lower():
                    # 리스트 슬라이싱을 이용한 앞뒤 줄 추출
                    start = max(0, i - context_lines)
                    end = i + context_lines + 1
                    snippet = "\n".join(lines[start:end])

                    results.append({
                        "file": doc['name'],
                        "line": i + 1,
                        "text": snippet
                    })
        return results