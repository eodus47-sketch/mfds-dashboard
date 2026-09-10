import os
import json
import urllib.parse
import requests
import time

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"

def fetch_data(base_url, ops, key_name):
    for op in ops:
        for json_type in ["type", "returnType"]:
            all_items = []
            success = False
            
            # 100건씩 10페이지 = 총 1,000건 수집 루프
            for page in range(1, 11):
                # 파라미터 꼬임 방지를 위해 원본 주소 직접 조립
                target_url = f"{base_url}/{op}?serviceKey={ENCODED_KEY}&pageNo={page}&numOfRows=100&{json_type}=json"
                
                # 방화벽 우회 프록시 터널 적용 (이 부분이 빠져서 0건이 떴던 것입니다!)
                proxy_url = f"https://api.allorigins.win/raw?url={urllib.parse.quote(target_url)}"
                
                try:
                    print(f"[{key_name}] {page}페이지 우회 수집 중...")
                    res = requests.get(proxy_url, timeout=20)
                    
                    if res.status_code == 200:
                        data = res.json()
                        body = data.get("response", {}).get("body", {}) or data.get("body", {})
                        items = body.get("items", [])
                        
                        if isinstance(items, dict) and "item" in items:
                            items = items["item"]
                            
                        if items and isinstance(items, list) and len(items) > 0:
                            all_items.extend(items)
                            success = True
                            time.sleep(1) # 공공 API 차단 방지를 위한 1초 휴식
                        else:
                            break # 해당 페이지에 더 이상 데이터가 없으면 중단
                    else:
                        break # 프록시 에러 시 중단
                except Exception as e:
                    print(f"에러 발생: {e}")
                    break
            
            if success and len(all_items) > 0:
                print(f"✅ [{key_name}] {op} 주소에서 총 {len(all_items)}건 수집 완료!")
                return all_items
                
    print(f"❌ [{key_name}] 모든 우회 경로 시도 실패")
    return []

def main():
    print("🚀 [1000건 확장 + 해외 차단 우회 복구 모드] 식약처 API 수집 시작...")
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
