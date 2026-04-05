import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a research summarizer for data scientists.

Your goal is to explain papers in a way that is:
- easy to understand
- intuitive
- not overly academic or full of complex jargon

Do NOT just rewrite the abstract.

Instead:
- explain what the paper is actually doing in simple terms
- make it feel like you're explaining to a smart coworker in the technical field
- prefer clarity over technical precision when needed

Return ONLY valid JSON as a list.

Each item must contain:
- arxiv_id
- title
- short_summary
- main_contribution
- why_it_matters

Writing rules:
- short_summary: 3–5 sentences, plain English, explain the idea clearly
- main_contribution: 1–2 sentences, what is new or different
- why_it_matters: 1–2 sentences, practical or conceptual importance

Style rules:
- avoid dense academic wording
- explain unfamiliar concepts briefly if needed
- use simple, direct language
- if unclear from abstract, say so plainly
"""

def create_summary_prompt(selected_papers):
    blocks = []

    for i, paper in enumerate(selected_papers):
        blocks.append(
            f"""
            Paper {i+1}
            arxiv_id: {paper.get("arxiv_id", "")}
            title: {paper.get("title", "")}
            category: {paper.get("primary_category", "")}
            published: {paper.get("published", "")}
            authors: {", ".join(paper.get("authors", []))}
            abstract: {paper.get("summary", "")}
            """.strip()
        )

    return "Summarize these selected papers:\n\n" + "\n\n".join(blocks)

def summarize_papers(selected_papers):
    prompt = create_summary_prompt(selected_papers)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()

    return json.loads(content)