#!/bin/bash
python3 -m pytest ./src/tests -vv
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload