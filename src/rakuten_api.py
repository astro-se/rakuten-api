import requests

def fetch_rakuten_products(keyword: str, app_id: str, access_key: str) -> list:
    """楽天最新APIから商品データを取得する"""
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    
    params = {
        "format": "json",
        "keyword": keyword,
        "genreId": "0",  # 新API必須パラメータ
        "applicationId": app_id,
        "accessKey": access_key,
        "hits": 30
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"楽天APIエラー ({response.status_code}): {response.text}")
        
    data = response.json()
    return data.get("Items", [])
