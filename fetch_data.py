import os
import json
import urllib.parse
import requests

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"
API_KEY = urllib.parse.unquote(ENCODED_KEY)

def fetch_data(base_url, ops, key_name):
    for op in ops:
        url = f"{base_url}/{op}"
        for json_param in [{"type": "json"}, {"returnType": "json"}]:
            params = {
                "serviceKey": API_KEY,
                "pageNo": "1",
                "numOfRows": "1000" # 300건에서 1,000건으로 수집량 대폭 확장
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
                        print(f"✅ [{key_name}] {op} 주소에서 {len(items)}건 수집 대성공!")
                        return items
            except Exception:
                pass
                
    print(f"❌ [{key_name}] 모든 주소 시도 실패")
    return []

def main():
    print("🚀 [최종 최적화 모드] 식약처 API 수집 시작...")
    os.makedirs("data", exist_ok=True)
    
    sanctions_base = "https://apis.data.go.kr/1471000/MdcinExaathrService04"
    sanctions_ops = ["getMdcinExaathrList04", "getMdcinExaathrList03", "getMdcinExaathrList02", "getMdcinExaathrList01", "getMdcinExaathrList"]
    sanctions = fetch_data(sanctions_base, sanctions_ops, "행정처분")
    with open("data/sanctions.json", "w", encoding="utf-8") as f:
        json.dump(sanctions, f, ensure_ascii=False, indent=2)

    letters_base = "https://apis.data.go.kr/1471000/DrugSafeLetterService02"
    letters_ops = ["getDrugSafeLetterList02", "getDrugSafeLetterList01", "getDrugSafeLetterList"]
    letters = fetch_data(letters_base, letters_ops, "안전성서한")
    with open("data/safe_letters.json", "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
