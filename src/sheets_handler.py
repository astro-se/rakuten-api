from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsClient:
    def __init__(self, secrets_dict: dict, spreadsheet_id: str):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        # StreamlitのSecrets辞書から直接認証
        creds = Credentials.from_service_account_info(secrets_dict, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.workbook = self.gc.open_by_key(spreadsheet_id)
        self.sheet = self.workbook.get_worksheet(0)

    def append_macro_data(self, items: list):
        """取得したアイテム群をスプレッドシートへ追記"""
        if not items:
            return
            
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = []
        
        for item_data in items:
            item = item_data.get("Item", {})
            rows.append([
                now_str,
                item.get("itemName"),
                item.get("itemPrice"),
                item.get("reviewCount"),
                item.get("shopName"),
                item.get("itemUrl")
            ])
            
        # ヘッダーが空なら作成
        if len(self.sheet.get_all_values()) == 0:
            self.sheet.append_row(['取得日時', '商品名', '価格(円)', 'レビュー件数', '店舗名', '商品URL'])
            
        self.sheet.append_rows(rows)
