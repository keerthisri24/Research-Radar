from arxiv_fetch import search_arxiv
from ranker import rank_papers

query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'
papers = search_arxiv(query, max_results=30)

ranked = rank_papers(papers)

for paper in ranked:
    print(paper["title"])
    print(paper["relevance_score"])
    print(paper["reason_selected"])
    print()