
import html
import time
import requests

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"


AI_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "llm",
    "large language model",
    "gpt",
    "openai",
    "anthropic",
    "claude",
    "gemini",
    "rag",
    "retrieval augmented generation",
    "agent",
    "multi-agent",
    "multimodal",
    "vision-language",
    "reasoning model",
    "inference",
    "fine-tuning",
    "eval",
    "evaluation",
    "alignment",
    "safety",
    "ethics",
    "deep learning",
    "neural network",
]


# Get top story IDs from Hacker News.
def get_top_story_ids(limit=60):
    url = f"{HN_BASE_URL}/topstories.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    story_ids = response.json()
    return story_ids[:limit]

# Get a single Hacker News item by ID.
def get_item(item_id):
    url = f"{HN_BASE_URL}/item/{item_id}.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def is_ai_related(story):
    title = (story.get("title") or "").lower()
    url = (story.get("url") or "").lower()
    text_blob = f"{title} {url}"

    return any(keyword in text_blob for keyword in AI_KEYWORDS)


def clean_text(text):
    if not text:
        return ""
    return html.unescape(text).strip()


def fetch_ai_news(max_candidates=30, top_story_pool=80, sleep_seconds=0.1):
    story_ids = get_top_story_ids(limit=top_story_pool)
    candidates = []

    for story_id in story_ids:
        item = get_item(story_id)

        if not item:
            continue

        if item.get("type") != "story":
            continue

        if item.get("deleted") or item.get("dead"):
            continue

        if not item.get("title"):
            continue

        if not is_ai_related(item):
            continue

        candidates.append(
            {
                "news_id": str(item.get("id")),
                "title": clean_text(item.get("title")),
                "url": item.get("url", ""),
                "score": item.get("score", 0),
                "by": item.get("by", ""),
                "time": item.get("time"),
                "descendants": item.get("descendants", 0),
                "type": item.get("type", ""),
                "source": "hacker_news",
            }
        )

        if len(candidates) >= max_candidates:
            break

        time.sleep(sleep_seconds)

    return candidates


if __name__ == "__main__":
    news_items = fetch_ai_news(max_candidates=10)

    for item in news_items:
        print("\n---")
        print("ID:", item["news_id"])
        print("Title:", item["title"])
        print("Score:", item["score"])
        print("Comments:", item["descendants"])
        print("URL:", item["url"])