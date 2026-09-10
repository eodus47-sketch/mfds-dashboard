import os
import json
import urllib.parse
import requests

# 1. 회원님이 검증 요청하신 정보 (팩트 반영)
BASE_URL = "https://apis.data.go.kr/1471000/MdcinExaathrService04"
ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

# 2. 이중 인코딩(Double-Encoding) 방지를 위한 디코딩 필수 적용
DECODED_KEY = urllib.parse.unquote(ENCODED_KEY)

def fetch_sanctions():
    # 기본 서비스 URL 뒤에 세부 호출 명칭(Operation) 추가
    ops = ["getMdcinExaathrList04", "getMdcinExaathrList"]
    
    for op in ops:
        url = f"{BASE_URL}/{op}"
        # 식약처 API 응답 포맷(type, returnType) 혼용 대응
        for json_param in [{"type": "json"}, {"returnType": "json"}]:
            params = {
                "serviceKey": DECODED_KEY,
                "pageNo": "1",
                "numOfRows": "300"
            }
            params.update(json_param)
            
            try:
                res = requests.get(url, params=params, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    body = data.get("response", {}).get("body", {}) or data.get("body", {})
                    items = body.get("items", [])
                    
                    if isinstance(items, dict) and "item" in items:
                        items = items["item"]
                        
                    if items and isinstance(items, list) and len(items) > 0:
                        print(f"✅ [행정처분] {len(items)}건 정상 수집 완료 (엔드포인트: {url})")
                        return items
            except Exception as e:
                pass
                
    print("❌ [행정처분] 수집 실패: 제공된 엔드포인트 및 파라미터 조합으로 데이터 반환 없음")
    return []

def fetch_letters():
    # 안전성 서한 (이전 로그에서 이미 300건 수집 성공이 확인된 코드)
    ops = ["getDrugSafeLetterList02", "getDrugSafeLetterList01"]
    for op in ops:
        url = f"https://apis.data.go.kr/1471000/DrugSafeLetterService02/{op}"
        for json_param in [{"type": "json"}, {"returnType": "json"}]:
            params = {
                "serviceKey": DECODED_KEY,
                "pageNo": "1",
                "numOfRows": "300"
            }
            params.update(json_param)
            try:
                res = requests.get(url, params=params, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    body = data.get("response", {}).get("body", {}) or data.get("body", {})
                    items = body.get("items", [])
                    if isinstance(items, dict) and "item" in items:
                        items = items["item"]
                    if items and isinstance(items, list) and len(items) > 0:
                        print(f"✅ [안전성서한] {len(items)}건 정상 수집 완료")
                        return items
            except:
                pass
    return []

def main():
    print("🚀 식약처 제공 공식 API 엔드포인트 기반 데이터 수집 가동...")
    os.makedirs("data", exist_ok=True)
    
    sanctions = fetch_sanctions()
    with open("data/sanctions.json", "w", encoding="utf-8") as f:
        json.dump(sanctions, f, ensure_ascii=False, indent=2)

    letters = fetch_letters()
    with open("data/safe_letters.json", "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
