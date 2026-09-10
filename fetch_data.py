import os
import json
import urllib.parse
import requests

ENCODED_KEY = "UeUGCJBDne0mX4NRwLK6TCdYTL99EzScvgxb0ai3l5d0M5YIO3YriZo%2FMiH1Amq9vL13f%2F9TtMyVcInZQf%2FsfQ%3D%3D"
API_KEY = urllib.parse.unquote(ENCODED_KEY)

def smart_fetch(base_url, ops, key_name):
    # 식약처 API의 고질적인 파라미터 불일치 문제 해결을 위해 여러 경우의 수 자동 탐색
    for op in ops:
        url = f"{base_url}/{op}"
        # type=json과 returnType=json 두 가지 방식을 모두 시도
        for json_param in [{"type": "json"}, {"returnType": "json"}]:
            params = {
                "serviceKey": API_KEY,
                "pageNo": "1",
                "numOfRows": "1000" # 풍부한 차트 구성을 위해 최근 300건 수집
            }
            params.update(json_param)
            
            try:
                res = requests.get(url, params=params, timeout=15)
                res.raise_for_status()
                
                # XML 에러 응답이 오면 json 변환 시 실패하여 아래 except로 넘어감
                data = res.json()
                
                body = data.get("response", {}).get("body", {}) or data.get("body", {})
                items = body.get("items", [])
                
                # 간혹 item 배열이 딕셔너리 안에 한 번 더 묶인 구조 처리
                if isinstance(items, dict) and "item" in items:
                    items = items["item"]
                    
                # 정상적으로 리스트 형태의 데이터가 들어왔을 때만 성공 처리
                if items and isinstance(items, list) and len(items) > 0:
                    print(f"✅ [{key_name}] 수집 성공! ({len(items)}건)")
                    return items
            except Exception:
                pass # 에러가 나면 조용히 다음 조합 시도

    print(f"❌ [{key_name}] 모든 주소 및 파라미터 조합 시도 실패")
    return []

def main():
    print("🚀 식약처 API 스마트 수집 로봇 시작...")
    os.makedirs("data", exist_ok=True)
    
    # 1. 행정처분 자동 탐색
    sanctions_base = "https://apis.data.go.kr/1471000/MdcinExaathrService04"
    sanctions_ops = ["getMdcinExaathrList04", "getMdcinExaathrList03", "getMdcinExaathrList02", "getMdcinExaathrList01", "getMdcinExaathrList"]
    sanctions = smart_fetch(sanctions_base, sanctions_ops, "행정처분")
    with open("data/sanctions.json", "w", encoding="utf-8") as f:
        json.dump(sanctions, f, ensure_ascii=False, indent=2)

    # 2. 안전성서한 자동 탐색 (데이터만 백그라운드로 수집)
    letters_base = "https://apis.data.go.kr/1471000/DrugSafeLetterService02"
    letters_ops = ["getDrugSafeLetterList02", "getDrugSafeLetterList01", "getDrugSafeLetterList"]
    letters = smart_fetch(letters_base, letters_ops, "안전성서한")
    with open("data/safe_letters.json", "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)

    print("✅ 데이터 수집 및 갱신 완료!")

if __name__ == "__main__":
    main()
