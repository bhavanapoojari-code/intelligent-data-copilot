def answer_question(question: str) -> dict:
    """
    Simple placeholder RAG response.
    Replace logic later with FAISS / embeddings if needed.
    """

    answer = (
        "daily_revenue = SUM(order_amount)\n"
        "order_count = COUNT(order_id)\n"
        "avg_order_value = daily_revenue / order_count\n\n"
        "Checks:\n"
        "- order_id must be unique\n"
        "- order_amount must be > 0\n"
        "- order_date cannot be NULL"
    )

    sources = [
        "metrics.md",
        "metrics_definition.md",
        "data_quality_rules.md",
        "anomaly_runbook.md",
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
