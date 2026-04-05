from arxiv_fetch import search_arxiv
from ranker import rank_papers
from summarizer import summarize_papers

query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'
papers = search_arxiv(query, max_results=30)

ranked = rank_papers(papers)

#print(papers[0])

top_ids = {paper["arxiv_id"] for paper in ranked[:3]}
top_papers = [paper for paper in papers if paper["arxiv_id"] in top_ids]

summaries = summarize_papers(top_papers)

print("\nTOP RANKED PAPERS:\n")
for paper in ranked[:3]:
    print(paper["title"])
    print("Score:", paper["relevance_score"])
    print("Why selected:", paper["reason_selected"])
    print()

print("\nSUMMARIES:\n")
for summary in summaries:
    print(summary["title"])
    print("Summary:", summary["short_summary"])
    print("Main contribution:", summary["main_contribution"])
    print("Why it matters:", summary["why_it_matters"])
    print("\n---\n")