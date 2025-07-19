from pydantic_settings import BaseSettings
from pydantic import AnyUrl
import base64, json, os, tempfile


class Settings(BaseSettings):
    # ========= Required back‑end services =========
    SUPABASE_DB_URL: AnyUrl                       # keep your Postgres integration

    # ========= Shopify creds (4 env vars) =========
    IRRANOVA_API_KEY: str
    IRRANOVA_PASSWORD: str
    IRRAKIDS_API_KEY: str
    IRRAKIDS_PASSWORD: str

    # Domains rarely change, but keep overridable
    IRRANOVA_DOMAIN: str = "fdd92b-2e.myshopify.com"
    IRRAKIDS_DOMAIN: str = "nouralibas.myshopify.com"

    # ========= Optional Google‑Sheets output ======
    GOOGLE_SHEET_ID: str | None = ""
    GOOGLE_SERVICE_ACCOUNT_JSON: str | None = ""

    # ========= Scanner tunables ===================
    MAX_DIGITS: int = 6
    ORDER_CUTOFF_DAYS: int = 50
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 1_000    # ms
    BATCH_SIZE: int = 100

    class Config:
        env_file = ".env", ".env.local", ".env.prod"

    # ---------- computed properties ---------------
    @property
    def shopify_stores(self) -> list[dict]:
        """Return the list structure expected by shopify.py."""
        return [
            {
                "name": "irranova",
                "api_key": self.IRRANOVA_API_KEY,
                "password": self.IRRANOVA_PASSWORD,
                "domain": self.IRRANOVA_DOMAIN,
            },
            {
                "name": "irrakids",
                "api_key": self.IRRAKIDS_API_KEY,
                "password": self.IRRAKIDS_PASSWORD,
                "domain": self.IRRAKIDS_DOMAIN,
            },
        ]

    # ---------- helpers ---------------------------
    def _write_sa_key(self) -> None:
        """If GOOGLE_SERVICE_ACCOUNT_JSON is set (base64), write it to disk
        so gspread/google‑apis can load it."""
        if not self.GOOGLE_SERVICE_ACCOUNT_JSON:
            return
        data = base64.b64decode(self.GOOGLE_SERVICE_ACCOUNT_JSON)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        fp.write(data)
        fp.close()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = fp.name


# instantiate once at import
settings = Settings()
settings._write_sa_key()
