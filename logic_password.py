# 패스워드 검증로직
def check_pw_security(password):

    # 상태를 저장할 딕셔너리(객체?)
    results = {"length": len(password) >= 10, "upper": False, "special": False, "forbidden": False, "score": 0}

    # 1. 길이 검사 (독립적)

    # 2. 내용 순회 (독립적)
    for char in password:
        if char.isupper():
            results["upper"] = True
        elif char in "!@#$%^*()_+-=":
            results["special"] = True
        elif not char.isalnum():
            results["forbidden"] = True

    # 3. 최종 판정
    if results["length"] and results["upper"] and results["special"] and not results["forbidden"]:
        results["score"] = 100

    return results

    # 길이 10자이상, 특수문자가 1개이상이고 ! @ # $ % ^ * ( ) _ + - = 이외에는 안됨, 대문자가 1개이상
    # allowed_special = "!@#$%^*()_+-="
    # 논리적 모순이 있어 로직 재구성필요( dkssud의 경우 길이,대문자,특수문자 누락이지만 쓰지도 않은 특수문자가 이미 포함되어있다고 나오면 오해요지가 있어보임
    # # 길이 검사 10자 이상이 아니면 바로 점수 리턴
    # if not results["upper"]:
    #     results["upper"] = True
    #     return results
    # # 문자열 순회(특수문자가 있는지 찾는다. 파이썬은 list로 변환 안해도 바로 for문 가능)
    # for char in password:
    # # 대문자가 있으면 true
    #     if char.isupper():
    #         results["upper"] = True
    # # 특수문자가 있으면 true
    #     elif char in allowed_special:
    #         results["special"] = True
    # # 숫자나 영문이 아닌데 허용된 특수문자도 아니라면?
    #     elif not char.isalnum():
    #         results["forbidden"] = True
    #         break
    # # 최종점수(모든점수 충족시)
    # if results["upper"] and results["special"] and not results["forbidden"]:
    #     results["score"] += 100
    # return results