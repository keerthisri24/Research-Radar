import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS paper_runs (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            published TEXT,
            category TEXT,
            relevance_score INTEGER,
            reason_selected TEXT,
            short_summary TEXT,
            main_contribution TEXT,
            why_it_matters TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def paper_already_saved(arxiv_id):
    conn = get_connection()
    cur = conn.cursor()

    # print(arxiv_id)
    
    cur.execute(
        "SELECT 1 FROM paper_runs WHERE arxiv_id = %s LIMIT 1;",
        (arxiv_id,)
    )
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


def save_paper_result(paper, ranked_info, summary_info):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO paper_runs (
            arxiv_id,
            title,
            published,
            category,
            relevance_score,
            reason_selected,
            short_summary,
            main_contribution,
            why_it_matters
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (arxiv_id) DO NOTHING;
    """, (
        paper.get("arxiv_id"),
        paper.get("title"),
        paper.get("published"),
        paper.get("primary_category"),
        ranked_info.get("relevance_score"),
        ranked_info.get("reason_selected"),
        summary_info.get("short_summary"),
        summary_info.get("main_contribution"),
        summary_info.get("why_it_matters"),
    ))

    conn.commit()
    cur.close()
    conn.close()