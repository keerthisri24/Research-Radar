# Research Radar

Research Radar is an end to end AI powered research and news update pipeline that automatically collects, ranks, summarizes, stores, and sends current tech research and news updates.

The system ingests recent arXiv papers and AI related Hacker News posts, applies LLM ranking and summarization, stores processed results in PostgreSQL with Docker, and delivers a curated digest through Telegram on a scheduled basis.

<img width="200" height="300" alt="IMG_4988" src="https://github.com/user-attachments/assets/fa25465f-ab70-4c5b-9b5f-695aaae5635a" /> <img width="200" height="300" alt="IMG_4989" src="https://github.com/user-attachments/assets/35f372f2-2971-4e8a-a52b-3a609763e79c" />

---

# Features

* Fetches recent AI papers from the arXiv API
* Fetches AI related news from Hacker News
* Uses LLMs for:

  * relevance ranking
  * digest generation
  * concise summarization
* Stores processed papers/news in PostgreSQL
* Prevents duplicate processing using database tracking
* Sends automated Telegram digests
* Runs automatically on AWS EC2 using cron scheduling
* Handles API failures with retry and backoff logic

---

# Tech Stack

## Languages

* Python

## APIs

* OpenAI API
* arXiv API
* Hacker News API
* Telegram Bot API

## Infrastructure

* AWS EC2
* Docker
* PostgreSQL
* Cron

## Python Libraries

* requests
* psycopg2
* python-dotenv
* openai

---

# System Architecture

```text
arXiv API ─────┐
               ├──> Ranking ───> Summarization ───┐
Hacker News ───┘                                  │
                                                   ├──> PostgreSQL
                                                   │
                                                   └──> Telegram Digest

AWS EC2 + Cron → Scheduled Daily Execution
```

---

# Project Structure

```text
Research-Radar/
│
├── arxiv_fetch.py          # Fetches papers from arXiv
├── ranker.py               # Ranks papers with LLM
├── summarizer.py           # Summarizes papers
│
├── news_fetch.py           # Fetches AI news from Hacker News
├── news_ranker.py          # Ranks news stories
├── news_summarizer.py      # Summarizes news
│
├── telegram_sender.py      # Sends Telegram messages
├── db.py                   # PostgreSQL connection + persistence
├── main.py                 # End-to-end pipeline entrypoint
│
├── requirements.txt
├── .env
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Research-Radar.git
cd Research-Radar
```

---

## 2. Create Virtual Environment (Optional)

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```text
OPENAI_API_KEY=your_openai_key

POSTGRES_DB=research_radar
POSTGRES_USER=radar_user
POSTGRES_PASSWORD=radar_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

# PostgreSQL Setup

## Run PostgreSQL with Docker

```bash
docker run --name research-postgres \
  -e POSTGRES_DB=research_radar \
  -e POSTGRES_USER=radar_user \
  -e POSTGRES_PASSWORD=radar_password \
  -p 5432:5432 \
  -d postgres:17
```

Verify container:

```bash
docker ps
```

---

# Running the Pipeline

Run manually:

```bash
python main.py
```

The pipeline will:

1. Fetch papers and news
2. Rank content using LLMs
3. Generate summaries
4. Store results in PostgreSQL
5. Send a Telegram digest

---

# Telegram Setup

## Create Bot

1. Open Telegram
2. Search for BotFather
3. Run:

```text
/newbot
```

4. Copy the generated bot token

---

## Get Chat ID

Message your bot once.

Then open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Find:

```json
"chat": {
  "id": 123456789
}
```

Use that value as `TELEGRAM_CHAT_ID`.

---

# AWS EC2 Deployment

## Launch EC2

Recommended configuration:

* Amazon Linux 2023
* t2.micro
* SSH enabled

---

## Install Dependencies on EC2

```bash
sudo dnf install python3-pip git docker cronie -y
```

Enable services:

```bash
sudo systemctl enable docker
sudo systemctl start docker

sudo systemctl enable crond
sudo systemctl start crond
```

---

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Research-Radar.git
cd Research-Radar
```

---

## Install Python Packages

```bash
python3 -m pip install --user -r requirements.txt
```

---

# Cron Scheduling

Open crontab:

```bash
crontab -e
```

Example: Run daily at 9 AM ET

```bash
0 13 * * * cd /home/ec2-user/Research-Radar && /usr/bin/python3 main.py >> output.log 2>&1
```

Verify cron jobs:

```bash
crontab -l
```

---

# Reliability Features

## Retry + Backoff Logic

The pipeline implements retry logic for:

* arXiv rate limits (429)
* temporary API outages (503)
* network timeouts
* transient connection failures

This improves reliability during automated scheduled execution.

---

## Duplicate Prevention

Processed papers/news are stored in PostgreSQL.

Before processing new items, the pipeline checks whether an item has already been summarized and delivered.





