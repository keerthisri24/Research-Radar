
# Sources:
# arxiv api documentation: https://info.arxiv.org/help/api/user-manual.html
# xml ET docuumentation: https://docs.python.org/3/library/xml.etree.elementtree.html

import requests
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

ARXIV_URL = "http://export.arxiv.org/api/query"

# retry because of rate limits
def get_retry(url, retries=5):
    for attempt in range(retries):
        try:
            time.sleep(5)

            response = requests.get(url, timeout=60, headers={"User-Agent": "ResearchRadar/1.0"})

            if response.status_code == 429:
                wait_time = 30 * (attempt + 1)
                print(f"arXiv rate limit error. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response

        except requests.exceptions.ReadTimeout:
            wait_time = 20 * (attempt + 1)
            print(f"arXiv timed out. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        except requests.exceptions.ConnectionError:
            wait_time = 20 * (attempt + 1)
            print(f"Connection error. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

    raise Exception("arXiv request failed after retries.")


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

    retrieved_papers = get_retry(url)

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
        paper_url = entry.findtext("atom:id", default="", namespaces=namespace)
        arxiv_id = paper_url.rstrip("/").split("/")[-1]

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
                "arxiv_id": arxiv_id,
                "link": paper_url,
                "title": title,
                "summary": summary,
                "published": published,
                "updated": updated,
                "authors": authors,
                "primary_category": primary_category,
            }
        )

       
    # print(entry)

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

