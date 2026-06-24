import requests

def fetch_rakuten_products(keyword: str, app_id: str, access_key: str) -> list:
    """楽天最新APIから商品データを取得する（リファラ制限対応版）"""
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    
    params = {
        "format": "json",
        "keyword": keyword,
        "genreId": "0",  # 新API必須パラメータ
        "applicationId": app_id,
        "accessKey": access_key,
        "hits": 30
    }
    
    # 楽天のドメインチェックを通過するため、登録したStreamlitのURLをヘッダーに仕込む
    headers = {
        "Referer": "https://rakuten-api.streamlit.app/",
        "Origin": "https://rakuten-api.streamlit.app",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # headers=headers を通信に追加
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"楽天APIエラー ({response.status_code}): {response.text}")
        
    data = response.json()
    return data.get("Items", [])
