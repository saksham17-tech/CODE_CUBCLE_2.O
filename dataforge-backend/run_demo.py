#!/usr/bin/env python3
"""
DataForge AI — Hackathon MVP Demo Runner
Starts the API + UI on http://127.0.0.1:8765
"""
import os
import sys
from pathlib import Path

# Ensure package path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

def main():
    import uvicorn
    from app.main import app
    print("=" * 60)
    print("  DataForge AI  —  Autonomous Data Intelligence Platform")
    print("  Hackathon MVP  |  http://127.0.0.1:8765")
    print("  API docs       |  http://127.0.0.1:8765/docs")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")

if __name__ == "__main__":
    main()
