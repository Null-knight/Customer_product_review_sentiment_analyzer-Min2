from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.database import DB_PATH


if __name__ == "__main__":
    if DB_PATH.exists():
        backup = DB_PATH.with_name(f"review_analyzer_{datetime.now():%Y%m%d_%H%M%S}.db")
        shutil.copy2(DB_PATH, backup)
        print(f"Backup written: {backup}")
    else:
        print("No database found to back up.")
