from arxiv_fetch import search_arxiv
from ranker import rank_papers
from summarizer import summarize_papers

from news_fetch import fetch_ai_news
from news_ranker import rank_news
from news_summarizer import summarize_news

from db import create_table, create_news_table, paper_already_saved, news_already_saved, save_paper_result, save_news_result
from telegram_sender import send_telegram_message

def run_digest():
    query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'

    create_table()
    create_news_table()

    papers = search_arxiv(query, max_results=30) # change back to 30
    papers = [p for p in papers if not paper_already_saved(p["arxiv_id"])]

    paper_summaries = []

    if papers:

        ranked_papers = rank_papers(papers)

        top_paper_ids = {str(p["arxiv_id"]) for p in ranked_papers[:3]}
        top_papers = [p for p in papers if str(p["arxiv_id"]) in top_paper_ids]
        paper_summaries = summarize_papers(top_papers)

        ranked_paper_map = {str(p["arxiv_id"]): p for p in ranked_papers}
        summary_paper_map = {str(p["arxiv_id"]): p for p in paper_summaries}

        for paper in top_papers:
            arxiv_id = str(paper["arxiv_id"])
            save_paper_result(
                paper,
                ranked_paper_map[arxiv_id],
                summary_paper_map[arxiv_id],)


    news_items = fetch_ai_news(max_candidates=30)
    news_items = [n for n in news_items if not news_already_saved(n["news_id"])]
    news_summaries = []

    if news_items:

        ranked_news = rank_news(news_items)

        top_news_ids = {str(n["news_id"]) for n in ranked_news[:3]}
        top_news = [n for n in news_items if str(n["news_id"]) in top_news_ids]
        news_summaries = summarize_news(top_news)

        ranked_news_map = {str(n["news_id"]): n for n in ranked_news}
        summary_news_map = {str(n["news_id"]): n for n in news_summaries}

        for news_item in top_news:
            news_id = str(news_item["news_id"])
            save_news_result(
                news_item,
                ranked_news_map[news_id],
                summary_news_map[news_id],)

    print("\nAI RESEARCH RADAR\n")
    print("PAPERS\n")

    for paper in paper_summaries:
        print(f"📄 {paper['title']}")
        print(f"Summary: {paper['short_summary']}")
        print(f"Key idea: {paper['main_contribution']}")
        print(f"Why it matters: {paper['why_it_matters']}")
        print()

    print("\nAI NEWS\n")

    for news in news_summaries:
        print(f"📰 {news['title']}")
        print(f"Summary: {news['summary']}")
        print(f"Why it matters: {news['why_it_matters']}")
        print(f"Who should care: {news['who_should_care']}")
        print()

    message = format_digest(paper_summaries, news_summaries)
    send_telegram_message(message)

def format_digest(paper_summaries, news_summaries):
    lines = []

    lines.append("🧠 <b>AI Research Radar</b>\n")

    lines.append("📄 <b>Papers</b>\n")
    if paper_summaries:
        for paper in paper_summaries:
            lines.append(f"<b>{paper['title']}</b>")
            lines.append(f"Summary: {paper['short_summary']}")
            lines.append(f"Key idea: {paper['main_contribution']}")
            lines.append(f"Why it matters: {paper['why_it_matters']}\n")
    else:
        lines.append("No new papers today.\n")

    lines.append("📰 <b>AI News</b>\n")
    if news_summaries:
        for news in news_summaries:
            lines.append(f"<b>{news['title']}</b>")
            lines.append(f"Summary: {news['summary']}")
            lines.append(f"Why it matters: {news['why_it_matters']}")
            lines.append(f"Who should care: {news['who_should_care']}\n")
    else:
        lines.append("No new AI news today.\n")

    return "\n".join(lines)

if __name__ == "__main__":
    run_digest()
    