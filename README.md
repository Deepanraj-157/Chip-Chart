# chip chart

## Problem
Engineers pick between several Wi-Fi/Bluetooth chips and must read 700-page reference manuals and long datasheet tables to estimate current draw, battery life and pin limits. LLM chatbots often misread table values or do the arithmetic wrong, which leads to wrong battery sizing.

## Who it is for
OneHardware design engineer at a Coimbatore IoT product design house  or two real user types, for example "compliance officer at a gold-loan NBFC in Coimbatore

## Signature feature
Battery-life calculator: enter a duty cycle and get average current and days of battery, with each number linked to its datasheet table and page.

## Hardest problem (my interview story)
Tables to numbers computed with code. Electrical-characteristics tables are extracted into typed rows (parameter, condition, min/typ/max, unit), and a Python calculator computes battery life or total current. The LLM only picks rows and explains; measured numeric accuracy is reported on 60 hand-checked calculations.
## Dataset


## 10 real questions
See [docs/QUESTIONS.md](docs/QUESTIONS.md).

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link

