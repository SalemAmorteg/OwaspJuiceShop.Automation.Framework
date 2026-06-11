from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

JUICE_SHOP_URL = "http://localhost:3000"

DATABASE_PATH = (
    PROJECT_ROOT
    / "juice-shop"
    / "data"
    / "juiceshop.sqlite"
)

REQUEST_TIMEOUT = 10

DATABASE_TIMEOUT = 30
