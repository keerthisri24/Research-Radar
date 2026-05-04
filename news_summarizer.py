import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"
PROMPT_VERSION = "hn_news_summarizer_v1"

SYSTEM_PROMPT = """
You are a news summarizer for busy technical readers.

Your job is to explain Hacker News AI stories in a way that is:
- easy to understand
- easy to digest
- not overly academic
- clear about why the story matters

Return ONLY valid JSON as a list.

Each item must contain:
- news_id
- title
- summary
- why_it_matters
- who_should_care

Writing rules:
- summary: 3-5 sentences in plain English
- explain what happened and why the story is getting attention
- avoid jargon when possible
- avoid hype
- use only the provided title, URL, score, and comment count
- if details are unclear from the metadata alone, say so plainly
"""


def build_news_summary_prompt(selected_news_items):
    blocks = []

    for i, item in enumerate(selected_news_items, start=1):
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

    return "Summarize these selected Hacker News stories:\n\n" + "\n\n".join(blocks)


def summarize_news(selected_news_items):
    prompt = build_news_summary_prompt(selected_news_items)

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
    from news_ranker import rank_news

    items = fetch_ai_news(max_candidates=20)
    ranked = rank_news(items)

    top_ids = {item["news_id"] for item in ranked[:3]}
    top_items = [item for item in items if item["news_id"] in top_ids]

    summaries = summarize_news(top_items)

    for item in summaries:
        print("\n---")
        print(item["title"])
        print("Summary:", item["summary"])
        print("Why it matters:", item["why_it_matters"])
        print("Who should care:", item["who_should_care"])