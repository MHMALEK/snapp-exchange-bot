# Exchange money bot

A **personal**, **non‑commercial** Telegram bot. The goal is modest: make it a bit simpler for **people in Iran** to find each other for **ریال ↔ euro / US dollar** deals—posting offers, browsing a small catalog, and seeing rough **ریالی equivalents** from public rate snapshots.

It does **not** move money, hold funds, or vet counterparties. You’re always responsible for who you trust and how you settle.

---

### What it does (high level)

- **Sign‑up / consent** flow in Persian  
- **Sell flow**: post an amount in EUR or USD; optional publish to a **listings channel** (bot must be admin there)  
- **Buy / browse** helpers and **channel membership** gate when configured  
- Small **FastAPI** app alongside the bot (e.g. for integrations); **SQLite** or **Postgres** via `DATABASE_URL`

---

### Run locally

Requires **Python 3.9+**.

```bash
cp .env.example .env   # fill in TELEGRAM_BOT_TOKEN and the rest
pip install -e ".[dev]"
python run_bot.py      # Telegram bot
# optional: python run_api.py   # FastAPI on :8000
```

Docker starts **both** the API and the bot (see `scripts/docker-entrypoint.sh`).

Tests: `pytest`

---

### Deploy

The repo includes a **Dockerfile** and a **GitHub Actions** workflow that builds, pushes to **GHCR**, and can **SSH‑deploy** to a small VPS. Secrets and env vars live in GitHub; see `.github/workflows/deploy.yml` for the list.

---

### Disclaimer

**Not** financial, legal, or tax advice. Rates shown are indicative only. This project is a hobby; use it at your own risk.
