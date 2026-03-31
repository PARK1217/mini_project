import requests
from datetime import datetime, timedelta
import config  # EXCHANGE_API_KEY 저장 파일


class ExchangeLogic:
    @classmethod
    def get_rates_by_date(cls, start_date_obj):
        """사용자가 지정한 날짜부터 역추적하여 환율을 가져옵니다."""
        search_date = start_date_obj
        attempts = 0

        while attempts < 7:
            formatted_date = search_date.strftime('%Y%m%d')

            params = {
                'authkey': config.EXCHANGE_API_KEY,
                'searchdate': formatted_date,
                'data': 'AP01'
            }

            try:
                # SSL 인증서 검증 오류 방지를 위해 verify=False 추가 (필요시)
                response = requests.get(config.EXCHANGE_API_URL, params=params, verify=False)
                data = response.json()

                # 데이터가 존재하고 결과가 성공(1)인 경우
                if data and len(data) > 0 and data[0].get('result') == 1:
                    return cls._process_data(data, formatted_date)

            except Exception as e:
                print(f"API 호출 중 오류 발생 ({formatted_date}): {e}")

            # 데이터가 없으면 하루 전으로 이동
            search_date -= timedelta(days=1)
            attempts += 1

        return None

    @classmethod
    def _process_data(cls, raw_data, date_str):
        """JSON 데이터를 계산하기 쉬운 딕셔너리로 가공"""
        processed = {'date': date_str, 'rates': {}}
        for item in raw_data:
            unit = item['cur_unit']
            # 쉼표 제거 및 숫자 변환
            rate = float(item['deal_bas_r'].replace(',', ''))

            # JPY(100) 등 100단위 통화 처리
            if "(100)" in unit:
                unit = unit.replace("(100)", "")
                rate = rate / 100

            processed['rates'][unit] = {
                'rate': rate,
                'name': item['cur_nm'],
                'ttb': item['ttb'],
                'tts': item['tts']
            }
        return processed

    @classmethod
    def get_weekly_trend(cls, unit_code):
        """특정 통화의 최근 7일간 환율 데이터를 가져옴."""
        trend_data = []
        current_date = datetime.now()
        days_collected = 0

        # 최근 10일 정도를 뒤져서 영업일 기준 7일치 데이터를 확보
        while days_collected < 7:
            formatted_date = current_date.strftime('%Y%m%d')
            params = {
                'authkey': config.EXCHANGE_API_KEY,
                'searchdate': formatted_date,
                'data': 'AP01'
            }
            try:
                response = requests.get(config.EXCHANGE_API_URL, params=params, verify=False)
                data = response.json()

                if data and len(data) > 0 and data[0].get('result') == 1:
                    # 해당 통화 찾기
                    for item in data:
                        if item['cur_unit'].replace("(100)", "") == unit_code:
                            rate = float(item['deal_bas_r'].replace(',', ''))
                            if "(100)" in item['cur_unit']: rate /= 100

                            # 그래프용 데이터 (날짜, 환율) 저장
                            trend_data.append({"날짜": current_date.strftime('%m/%d'), "환율": rate})
                            days_collected += 1
                            break
            except:
                pass

            current_date -= timedelta(days=1)
            # 무한 루프 방지 (최대 14일 전까지만 탐색)
            if (datetime.now() - current_date).days > 14: break

        # 날짜 순으로 정렬 (과거 -> 현재)
        return trend_data[::-1]