import streamlit as st
from src.rakuten_api import fetch_rakuten_products
from src.sheets_handler import GoogleSheetsClient

st.set_page_config(page_title="Astro 楽天マクロデータ連携", layout="wide")
st.title("📊 楽天市場 マクロデータ・パイプライン")

# 設定情報（Secrets）の読み込み
try:
    RAKUTEN_APP_ID = st.secrets["rakuten"]["application_id"]
    RAKUTEN_ACCESS_KEY = st.secrets["rakuten"]["access_key"]
    SPREADSHEET_ID = st.secrets["spreadsheet"]["id"]
    GOOGLE_CREDS = dict(st.secrets["gserviceaccount"])
except Exception as e:
    st.error("Secretsの設定が読み込めません。.streamlit/secrets.toml を確認してください。")
    st.stop()

# 画面UIの構築
keyword = st.text_input("分析対象キーワードを入力", value="不織布")

if st.button("楽天からデータを抽出してスプシに書き込む", type="primary"):
    with st.spinner("パイプライン実行中..."):
        try:
            # 1. 楽天からデータを取得
            items = fetch_rakuten_products(keyword, RAKUTEN_APP_ID, RAKUTEN_ACCESS_KEY)
            
            if not items:
                st.warning("該当データがありませんでした。")
                st.stop()
                
            # 2. スプシに書き込み
            client = GoogleSheetsClient(GOOGLE_CREDS, SPREADSHEET_ID)
            client.append_macro_data(items)
            
            st.success(f"正常に {len(items)} 件のデータをスプレッドシートに追記しました。")
            st.balloons()
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
