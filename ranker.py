import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

SYSTEM_PROMPT = """
You are a research paper finder.

Your job is to review newly published arXiv papers and identify the ones
most relevant to a user interested in:
- AI Agents
- Retrieval Augmented Generation (RAG)
- Multimodal AI
- AI ethics

Prefer papers that are clearly relevant to the user’s interests and avoid selecting multiple papers that appear redundant or highly overlapping.

Return ONLY valid JSON as a list of the top 5 papers sorted by relevance_score descending.

Each item must have:
- arxiv_id
- title
- relevance_score
- reason_selected

Use only the provided title and abstract.
Be concrete.
"""

def create_rank_prompt(papers):
    prompt = []
    for i, paper in enumerate(papers):
        prompt.append(
            f"""
            Paper{i+1}
            arxiv_id:{paper.get("arxiv_id")}
            arxiv_id: {paper.get("arxiv_id", "")}
            title: {paper.get("title", "")}
            category: {paper.get("primary_category", "")}
            published: {paper.get("published", "")}
            authors: {", ".join(paper.get("authors", []))}
            abstract: {paper.get("summary", "")}
            """.strip()
        )

    return "These are the papers to choose from:\n\n"+"\n\n".join(prompt)

def rank_papers(papers):
    prompt = create_rank_prompt(papers)

    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
        ],)
    
    response = response.choices[0].message.content
    
    if response.startswith("```json"):
        response = response.removeprefix("```json").removesuffix("```").strip()
    elif response.startswith("```"):
        response = response.removeprefix("```").removesuffix("```").strip()

    return json.loads(response)

