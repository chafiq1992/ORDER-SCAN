import gspread
from .settings import settings

def _client():
    if not settings.GOOGLE_SHEET_ID:
        return None
    return gspread.service_account()

def append_row(values: list[str]):
    gc = _client()
    if not gc:
        return
    sh = gc.open_by_key(settings.GOOGLE_SHEET_ID)
    ws = sh.worksheet("Scans")
    ws.append_row(values, value_input_option="USER_ENTERED")
