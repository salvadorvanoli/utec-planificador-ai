try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv():
        return None

import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

if not OPENAI_KEY:
    # No lanzar error en import; se validará al inicializar el agente.
    OPENAI_KEY = None

