import os
import json
import urllib.parse
import requests
import time
import random

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

def fetch_data(base_url, ops, key_name):
    # 안정성이 검증된 프록시 서버 순차 적용
    proxies = [
        "https://api.allorigins.win/raw?url=",
        "https://api.codetabs.com/v1/proxy?quest=",
        "https://corsproxy.io/?"
    ]
    
    for proxy in proxies:
        for op in ops:
            for json_type in ["type", "returnType"]:
                # 회원님 말씀대로 가장 안정적인 500건으로 타협!
                target_url = f"{base_url}/{op}?serviceKey={ENCODED_KEY}&pageNo=1&numOfRows=500&{json_type}=json"
                encoded_url = urllib.parse.quote(target_url)
                
                # 캐시 무력화 난수 추가
                if "allorigins" in proxy:
                    proxy_url = f"{proxy}{encoded_url}&disableCache=true&_={random.randint(1,99999)}"
                else:
                    proxy_url = f"{proxy}{encoded_url}"
                    
                try:
                    print(f"[{key_name}] {proxy.split('//')[1].split('/')[0]} 서버로 500건 수집 요청 중...")
                    res = requests.get(proxy_url, timeout=30)
                    
                    if res.status_code == 200:
                        data = res.json()
                        body = data.get("response", {}).get("body", {}) or data.get("body", {})
                        items = body.get("items", [])
                        
                        if isinstance(items, dict) and "item" in items:
                            items = items["item"]
                            
                        # 정상 수집 시 즉시 종료
                        if items and isinstance(items, list) and len(items) > 0:
                            print(f"✅ [{key_name}] 총 {len(items)}건 수집 대성공!")
                            return items
                except Exception:
                    pass # 에러 발생 시 조용히 다음 조합으로 넘어감
                    
    print(f"❌ [{key_name}] 모든 우회 경로 및 조합 시도 실패")
    return []

def main():
    print("🚀 [500건 최적화 + 고안정성 프록시 모드] 식약처 API 수집 시작...")
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
