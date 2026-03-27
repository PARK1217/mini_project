class UnitConverter:
    # 1. 테이블 대신하는 환산계수 테이블(자바에서는 static Map과 같은 역할을 함)
    LENGTH_FACTORS = { # 모든 단위의 기준은 현재 m를 기준으로 작성되어있음
        'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
        'inch': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mile': 1609.34, '자': 0.303
    }

    WEIGHT_FACTORS = { # 환산 기준 kg
        'mg': 0.000001, 'g': 0.001, 'kg': 1.0, 't': 1000.0, 'oz': 0.0283495,
        'lb': 0.453592, '돈': 0.00375, '근': 0.6, '관': 3.75
    }

    @classmethod    # 클래스 변수에 접근하기 위해 classmethod 사용
    def convert(cls, category, value, from_unit, to_unit):
        """통합 변환 메서드 (Strategy Pattern 적용)"""
        # 전략패턴(Strategy Pattern) : 상황에 따라 도구를 골라서 쓰는 패턴
        try:
            # 카테고리에 맞는 팩터 딕셔너리 선택
            match category:
                case "길이" : factors = cls.LENGTH_FACTORS    # 길이라는 전략!
                case "무게" : factors = cls.WEIGHT_FACTORS
                case _: return value    # 데이터에 없는 단위면 그대로 반환

            # 계산로직: (입력값 * 시작단위계수) / 목표단위계수 (공통계산로직 - OCP 원칙)
            base_value = value * factors[from_unit] # 기준 단위인 m로 바꾼다
            result = base_value / factors[to_unit]  # 최종 목표단위로 변경

            return round(result, 4)
        except (KeyError, ZeroDivisionError):
            return 0.0
