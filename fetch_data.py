import os
import json
import requests

# 사용자 API 키
ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

def main():
    print("🔍 식약처 API 원인 분석 엑스레이(X-ray) 모드 가동...")
    os.makedirs("data", exist_ok=True)
    
    # 웹사이트 뻗는 것 방지용 빈 파일 생성
    with open("data/sanctions.json", "w", encoding="utf-8") as f: json.dump([], f)
    with open("data/safe_letters.json", "w", encoding="utf-8") as f: json.dump([], f)

    # 파라미터 인코딩 충돌 방지를 위해 무식하게 한 줄로 직접 꽂아버리기
    url = f"https://apis.data.go.kr/1471000/MdcinExaathrService04/getMdcinExaathrList03?serviceKey={ENCODED_KEY}&type=json&pageNo=1&numOfRows=10"
    
    try:
        print("🌐 식약처 서버에 요청을 보냅니다...")
        res = requests.get(url, timeout=20)
        print(f"✅ 상태 코드 (200이면 통신 정상): {res.status_code}")
        print("================ 응답 원본 메시지 ================")
        print(res.text[:1000])
        print("==================================================")
    except Exception as e:
        print(f"❌ 접속 자체 실패 (방화벽 차단 의심): {e}")

if __name__ == "__main__":
    main()
