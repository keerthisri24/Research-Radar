from arxiv_fetch import search_arxiv
from ranker import rank_papers
from summarizer import summarize_papers
from db import create_table, paper_already_saved, save_paper_result

create_table()

query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'

papers = search_arxiv(query, max_results=30)

papers = [paper for paper in papers if not paper_already_saved(paper["arxiv_id"])]

if not papers:
    print("No new papers to process.")
    exit()

#print(papers[0])

ranked = rank_papers(papers)

top_ids = {paper["arxiv_id"] for paper in ranked[:3]}
top_papers = [paper for paper in papers if paper["arxiv_id"] in top_ids]

summaries = summarize_papers(top_papers)

ranked_map = {paper["arxiv_id"]: paper for paper in ranked}
summary_map = {paper["arxiv_id"]: paper for paper in summaries}

print("\nTODAY'S PAPER DIGEST:\n")

for paper in top_papers:
    arxiv_id = paper["arxiv_id"]
    ranked_info = ranked_map[arxiv_id]
    summary_info = summary_map[arxiv_id]

    print(f"📄 {summary_info['title']}")
    print(f"\nSummary:\n{summary_info['short_summary']}")
    print(f"\nKey idea: {summary_info['main_contribution']}")
    print(f"\nWhy it matters: {summary_info['why_it_matters']}")
    print("\n" + "=" * 60 + "\n")

    save_paper_result(paper, ranked_info, summary_info)