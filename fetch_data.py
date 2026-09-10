import os
import json
import urllib.parse
import requests
import time
import random

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

def fetch_data(base_url, ops, key_name):
    # 안정성이 훨씬 높은 우회 프록시 서버 3종으로 교체 및 확장
    proxies = [
        "https://api.codetabs.com/v1/proxy?quest=",
        "https://api.allorigins.win/raw?url=",
        "https://corsproxy.io/?"
    ]
    
    for proxy in proxies:
        for op in ops:
            for json_type in ["type", "returnType"]:
                # 여러 페이지로 쪼개지 않고, 한 번의 요청으로 1000건을 요구하여 프록시 차단 방지
                target_url = f"{base_url}/{op}?serviceKey={ENCODED_KEY}&pageNo=1&numOfRows=1000&{json_type}=json"
                encoded_url = urllib.parse.quote(target_url)
                
                # allorigins 서버의 악명 높은 캐시 고착화 문제 해결용 난수(Random) 추가
                if "allorigins" in proxy:
                    proxy_url = f"{proxy}{encoded_url}&disableCache=true&_={random.randint(1,99999)}"
                else:
                    proxy_url = f"{proxy}{encoded_url}"
                    
                try:
                    print(f"[{key_name}] {proxy.split('//')[1].split('/')[0]} 서버로 1000건 단건 수집 요청 중...")
                    res = requests.get(proxy_url, timeout=30)
                    
                    if res.status_code == 200:
                        data = res.json()
                        body = data.get("response", {}).get("body", {}) or data.get("body", {})
                        items = body.get("items", [])
                        
                        if isinstance(items, dict) and "item" in items:
                            items = items["item"]
                            
                        # 단건 요청으로 정상적으로 데이터를 받았다면 즉시 종료
                        if items and isinstance(items, list) and len(items) > 0:
                            print(f"✅ [{key_name}] 총 {len(items)}건 수집 대성공!")
                            return items
                        else:
                            print("  -> 응답은 성공했으나 데이터가 비어있습니다.")
                    else:
                        print(f"  -> 상태코드 에러: {res.status_code}")
                except Exception as e:
                    print(f"  -> 통신 에러 발생: {e}")
                    time.sleep(1) # 에러 발생 시 방화벽 자극을 피하기 위해 1초 대기
                    
    print(f"❌ [{key_name}] 모든 우회 경로 및 조합 시도 실패")
    return []

def main():
    print("🚀 [1000건 단건 수집 + 고안정성 프록시 모드] 식약처 API 수집 시작...")
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
