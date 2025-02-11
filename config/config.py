import os
from dotenv import load_dotenv
import torch

# ✅ Ielādē .env failu no config/ direktorijas
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print("⚠️  Brīdinājums: .env fails netika atrasts config/ direktorijā!")

# ✅ API Atslēgas un Telegram konfigurācija
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("API_KEY")

# ✅ DeepSeek AI Modelis
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/deepseek-v3-base")  # Noklusējuma modelis
USE_GPU = os.getenv("USE_GPU", "true").lower() == "true"

# ✅ Pārbauda, vai GPU ir pieejams un konfigurē ierīci
DEVICE = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"

# ✅ Debug Logs
if not TELEGRAM_BOT_TOKEN:
    print("❌ Kļūda: TELEGRAM_BOT_TOKEN nav iestatīts .env failā!")
if not TELEGRAM_CHAT_ID:
    print("❌ Kļūda: TELEGRAM_CHAT_ID nav iestatīts .env failā!")
if not API_KEY:
    print("❌ Kļūda: API_KEY nav iestatīts .env failā!")

print(f"✅ DeepSeek AI Modelis: {MODEL_NAME}")
print(f"✅ Ierīce: {DEVICE} (GPU aktīvs: {torch.cuda.is_available()})")
