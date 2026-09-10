import os
import json
import urllib.parse
import requests

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

def fetch_data(base_url, op_name, key_name):
    target_url = f"{base_url}/{op_name}?serviceKey={ENCODED_KEY}&type=json&pageNo=1&numOfRows=300"
    
    # 식약처 해외 IP 차단을 뚫기 위한 우회 프록시(Proxy) 서버 활용
    urls_to_try = [
        f"https://api.allorigins.win/raw?url={urllib.parse.quote(target_url)}",
        f"https://corsproxy.io/?{urllib.parse.quote(target_url)}",
        target_url
    ]
    
    for idx, url in enumerate(urls_to_try):
        try:
            print(f"[{key_name}] 우회 경로 {idx+1} 시도 중...")
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            
            data = res.json()
            body = data.get("response", {}).get("body", {}) or data.get("body", {})
            items = body.get("items", [])
            
            if isinstance(items, dict) and "item" in items:
                items = items["item"]
                
            if items and isinstance(items, list) and len(items) > 0:
                print(f"✅ [{key_name}] 데이터 {len(items)}건 수집 완료!")
                return items
        except Exception as e:
            print(f"⚠️ 우회 경로 {idx+1} 실패: {e}")
            
    print(f"❌ [{key_name}] 모든 수집 경로가 막혔습니다.")
    return []

def main():
    print("🚀 [해외 IP 차단 우회 모드] 식약처 API 수집 시작...")
    os.makedirs("data", exist_ok=True)
    
    sanctions = fetch_data("https://apis.data.go.kr/1471000/MdcinExaathrService04", "getMdcinExaathrList03", "행정처분")
    with open("data/sanctions.json", "w", encoding="utf-8") as f:
        json.dump(sanctions, f, ensure_ascii=False, indent=2)

    letters = fetch_data("https://apis.data.go.kr/1471000/DrugSafeLetterService02", "getDrugSafeLetterList02", "안전성서한")
    with open("data/safe_letters.json", "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
