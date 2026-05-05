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

def create_news_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news_runs (
            news_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT,
            source TEXT,
            relevance_score INTEGER,
            reason_selected TEXT,
            summary TEXT,
            why_it_matters TEXT,
            who_should_care TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def news_already_saved(news_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM news_runs WHERE news_id = %s LIMIT 1;",
        (news_id,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


def save_news_result(news_item, ranked_info, summary_info):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO news_runs (
            news_id,
            title,
            url,
            source,
            relevance_score,
            reason_selected,
            summary,
            why_it_matters,
            who_should_care
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (news_id) DO NOTHING;
    """, (
        news_item.get("news_id"),
        news_item.get("title"),
        news_item.get("url"),
        news_item.get("source"),
        ranked_info.get("relevance_score"),
        ranked_info.get("reason_selected"),
        summary_info.get("summary"),
        summary_info.get("why_it_matters"),
        summary_info.get("who_should_care"),
    ))

    conn.commit()
    cur.close()
    conn.close()