import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"
PROMPT_VERSION = "hn_news_ranker_v1"

SYSTEM_PROMPT = """
You are an AI news scout for a daily digest.

Your job is to review Hacker News stories and identify the ones most relevant to a user interested in:
- AI agents
- retrieval-augmented generation (RAG)
- multimodal AI
- AI ethics
- practical AI tools, products, and platform updates

Prioritize stories that are:
- genuinely about AI
- useful or important for technical readers
- likely to matter beyond shallow hype
- not redundant with each other

Return ONLY valid JSON as a list of the top 5 stories sorted by relevance_score descending.

Each item must contain:
- news_id
- title
- relevance_score
- reason_selected

Rules:
- Use only the provided title, URL, score, and comment count
- Be concrete
- Avoid hype
- Skip weak or generic startup/news stories unless they are clearly important
"""


def build_news_ranking_prompt(news_items):
    blocks = []

    for i, item in enumerate(news_items, start=1):
        blocks.append(
            f"""
Story {i}
news_id: {item.get("news_id", "")}
title: {item.get("title", "")}
url: {item.get("url", "")}
score: {item.get("score", 0)}
comment_count: {item.get("descendants", 0)}
author: {item.get("by", "")}
""".strip()
        )

    return "Here are the candidate Hacker News stories:\n\n" + "\n\n".join(blocks)


def rank_news(news_items):
    prompt = build_news_ranking_prompt(news_items)

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()

    return json.loads(content)


if __name__ == "__main__":
    from news_fetch import fetch_ai_news

    items = fetch_ai_news(max_candidates=20)
    ranked = rank_news(items)

    for item in ranked:
        print("\n---")
        print(item["title"])
        print("Score:", item["relevance_score"])
        print("Why selected:", item["reason_selected"])