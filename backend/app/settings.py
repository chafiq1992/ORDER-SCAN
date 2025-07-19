from pydantic import BaseSettings, AnyUrl
import json, base64, os, tempfile

class Settings(BaseSettings):
    SUPABASE_DB_URL: AnyUrl
    SHOPIFY_STORES_JSON: str
    GOOGLE_SHEET_ID: str | None = ""
    GOOGLE_SERVICE_ACCOUNT_JSON: str | None = ""
    MAX_DIGITS: int = 6
    ORDER_CUTOFF_DAYS: int = 50
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 1000  # ms
    BATCH_SIZE: int = 100

    class Config:
        env_file = ".env", ".env.local", ".env.prod"

    @property
    def shopify_stores(self) -> list[dict]:
        return json.loads(self.SHOPIFY_STORES_JSON)

    def _write_sa_key(self):
        if not self.GOOGLE_SERVICE_ACCOUNT_JSON:
            return
        data = base64.b64decode(self.GOOGLE_SERVICE_ACCOUNT_JSON)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        fp.write(data); fp.close()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = fp.name

settings = Settings()
settings._write_sa_key()
