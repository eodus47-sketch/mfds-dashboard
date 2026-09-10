import os
import json
import urllib.parse
import requests

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"
API_KEY = urllib.parse.unquote(ENCODED_KEY)

# 최신 식약처 API 엔드포인트명 적용
SANCTION_URL = "https://apis.data.go.kr/1471000/MdcinExaathrService04/getMdcinExaathrList04"
SAFE_LETTER_URL = "https://apis.data.go.kr/1471000/DrugSafeLetterService02/getDrugSafeLetterList02"

os.makedirs("data", exist_ok=True)

def fetch_data(url, key_name):
    params = {
        "serviceKey": API_KEY,
        "type": "json",
        "pageNo": "1",
        "numOfRows": "100"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 공공데이터포털 JSON 표준 구조 완벽 대응
        body = data.get("response", {}).get("body", {}) or data.get("body", {})
        items = body.get("items", [])
        
        # 가끔 items 안에 item 이라는 딕셔너리가 한 번 더 있는 경우를 처리
        if isinstance(items, dict) and "item" in items:
            items = items["item"]
            
        print(f"[{key_name}] {len(items)}건 수집 완료")
        return items
    except Exception as e:
        print(f"[{key_name}] API 수집 중 오류 발생: {e}")
        return []

def main():
    print("🚀 식약처 API 데이터 수집 시작...")
    
    sanctions = fetch_data(SANCTION_URL, "행정처분")
    with open("data/sanctions.json", "w", encoding="utf-8") as f:
        json.dump(sanctions, f, ensure_ascii=False, indent=2)

    safe_letters = fetch_data(SAFE_LETTER_URL, "안전성서한")
    with open("data/safe_letters.json", "w", encoding="utf-8") as f:
        json.dump(safe_letters, f, ensure_ascii=False, indent=2)
        
    print("✅ 모든 데이터 갱신이 완료되었습니다.")

if __name__ == "__main__":
    main()
