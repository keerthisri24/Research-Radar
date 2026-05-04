from news_fetch import fetch_ai_news
from news_ranker import rank_news
from news_summarizer import summarize_news

news_items = fetch_ai_news(max_candidates=30)
ranked_news = rank_news(news_items)

top_news_ids = {str(item["news_id"]) for item in ranked_news[:3]}
top_news = [item for item in news_items if item["news_id"] in top_news_ids]

news_summaries = summarize_news(top_news)

print(news_summaries)

# print("Fetched:", len(news_items))
# print("Ranked:", len(ranked_news))
# print("Top IDs:", top_news_ids)
# print("Top News:", len(top_news))