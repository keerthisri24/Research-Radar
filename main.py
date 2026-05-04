from arxiv_fetch import search_arxiv
from ranker import rank_papers
from summarizer import summarize_papers

from news_fetch import fetch_ai_news
from news_ranker import rank_news
from news_summarizer import summarize_news


def run_digest():
    query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'

    papers = search_arxiv(query, max_results=30)
    ranked_papers = rank_papers(papers)

    top_paper_ids = {str(p["arxiv_id"]) for p in ranked_papers[:3]}
    top_papers = [p for p in papers if str(p["arxiv_id"]) in top_paper_ids]
    paper_summaries = summarize_papers(top_papers)

    news_items = fetch_ai_news(max_candidates=30)
    ranked_news = rank_news(news_items)

    top_news_ids = {str(n["news_id"]) for n in ranked_news[:3]}
    top_news = [n for n in news_items if str(n["news_id"]) in top_news_ids]
    news_summaries = summarize_news(top_news)

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


if __name__ == "__main__":
    run_digest()