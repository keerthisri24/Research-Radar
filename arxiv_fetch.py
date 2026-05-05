
# Sources:
# arxiv api documentation: https://info.arxiv.org/help/api/user-manual.html
# xml ET docuumentation: https://docs.python.org/3/library/xml.etree.elementtree.html

import requests
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

ARXIV_URL = "http://export.arxiv.org/api/query"

# return list of relevant papers
def search_arxiv(query, max_results):
    url = f"ARXIV_URL{query}"
    encoded_query = quote_plus(query)

    url = (
        f"{ARXIV_URL}"
        f"?search_query={encoded_query}"
        f"&start=0"
        f"&max_results={max_results}"
        f"&sortBy=submittedDate"
        f"&sortOrder=descending"
    )

    time.sleep(3)
    retrieved_papers = requests.get(url, timeout=30)
    retrieved_papers.raise_for_status()

    papers_formatted = ET.fromstring(retrieved_papers.text)

    # arxiv uses atom namespace
    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    papers = []

    for entry in papers_formatted.findall("atom:entry", namespace):
        title = entry.findtext("atom:title", default="", namespaces=namespace).strip().replace("\n", " ")
        summary = entry.findtext("atom:summary", default="", namespaces=namespace).strip().replace("\n", " ")
        published = entry.findtext("atom:published", default="", namespaces=namespace)
        updated = entry.findtext("atom:updated", default="", namespaces=namespace)
        paper_id = entry.findtext("atom:id", default="", namespaces=namespace)

        authors = [
            author.findtext("atom:name", default="", namespaces=namespace)
            for author in entry.findall("atom:author", namespace)
        ]

        primary_category = None
        primary_cat_val = entry.find("arxiv:primary_category", namespace)
        if primary_cat_val is not None:
            primary_category = primary_cat_val.attrib.get("term")

        papers.append(
            {
                "arxiv_id": paper_id,
                "title": title,
                "summary": summary,
                "published": published,
                "updated": updated,
                "authors": authors,
                "primary_category": primary_category,
            }
        )


    return papers


if __name__ == "__main__":
    query = '(cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND ' \
    '(all:agent OR all:"retrieval augmented generation" OR all:RAG OR all:multimodal OR all:"multi modal" OR all:"ai ethics" OR all:ethics)'
    papers = search_arxiv(query, max_results = 5)

    for i, paper in enumerate(papers, start=1):
        print(f"\n=========== Paper {i} ===========")
        print("Title:", paper["title"])
        print("Authors:", ", ".join(paper["authors"][:5]))
        print("Published:", paper["published"])
        print("Category:", paper["primary_category"])
        print("ID:", paper["arxiv_id"])
        print("Summary:", paper["summary"][:500], "..." if len(paper["summary"]) > 500 else "")

