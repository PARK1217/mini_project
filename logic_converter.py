class UnitConverter:
    # 1. 각 카테고리별 환산 계수 (기준 단위: m, kg, B, m2, s)
    _FACTORS = {
        "길이": {
            'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
            'inch': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mile': 1609.34, '자': 0.303
        },
        "무게": {
            'mg': 0.000001, 'g': 0.001, 'kg': 1.0, 't': 1000.0,
            'oz': 0.02835, 'lb': 0.45359, '돈': 0.00375, '근': 0.6, '관': 3.75
        },
        "데이터 크기": {
            'bit': 0.125, 'B': 1.0, 'KB': 1024.0, 'MB': 1024.0 ** 2,
            'GB': 1024.0 ** 3, 'TB': 1024.0 ** 4, 'PB': 1024.0 ** 5
        },
        "부동산 넓이": {
            'm2': 1.0, 'py': 3.305785, 'ac': 4046.856, 'ha': 10000.0, 'sq_ft': 0.092903
        },
        "시간": {
            'ms': 0.001, 's': 1.0, 'min': 60.0, 'h': 3600.0, 'd': 86400.0, 'week': 604800.0
        }
    }

    @classmethod
    def get_categories(cls):
        """프론트엔드 셀렉트박스용 카테고리 목록 반환"""
        return list(cls._FACTORS.keys()) + ["온도"]

    @classmethod
    def get_units(cls, category):
        """선택된 카테고리에 맞는 단위 리스트 반환"""
        if category == "온도":
            return ["°C (섭씨)", "°F (화씨)", "K (켈빈)"]
        return list(cls._FACTORS.get(category, {}).keys())

    @classmethod
    def convert(cls, category, value, from_unit, to_unit):
        """통합 변환 메서드 (전략 패턴 적용)"""
        try:
            # 1. 온도 예외 처리 (공식이 다르므로 별도 로직 실행)
            if category == "온도":
                return cls._convert_temperature(value, from_unit, to_unit)

            # 2. 일반 단위 처리 (Strategy lookup)
            factors = cls._FACTORS.get(category)
            if not factors:
                return value

            # 공통 변환 공식: (입력값 * 시작계수) / 목표계수
            base_value = value * factors[from_unit]
            result = base_value / factors[to_unit]
            return round(result, 4)

        except (KeyError, ZeroDivisionError, TypeError):
            return None # 0.0 대신 None 을 반환

    @classmethod
    def _convert_temperature(cls, value, from_unit, to_unit):
        """내부용 온도 변환 로직 (Private-like method)"""
        # 단위명에서 기호만 추출 (예: "°C (섭씨)" -> "°C")
        f = from_unit.split()[0]
        t = to_unit.split()[0]

        if f == t: return value

        # 1. 기준(섭씨)으로 변환
        c = value
        if f == "°F":
            c = (value - 32) * 5 / 9
        elif f == "K":
            c = value - 273.15

        # 2. 섭씨에서 목표 단위로 변환
        res = c
        if t == "°F":
            res = (c * 9 / 5) + 32
        elif t == "K":
            res = c + 273.15

        return round(res, 2)