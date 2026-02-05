import re


def answer_question(
    question: str,
    excel_data: dict | None,
    pdf_text: str | None,
    chat_history: list,
    ask_ollama
) -> str:
    """
    Routes questions correctly:
    - Numeric facts → Python (instant, exact)
    - Comparisons → Python
    - Explanations / follow-ups → LLM (with fact memory)
    """

    q = question.lower()

    # -------------------------------------------------
    # 1️⃣ NUMERIC LOOKUP (FAST + EXACT)
    # -------------------------------------------------
    if excel_data:
        for item, years in excel_data.items():
            if item in q:
                year_match = re.search(r"(20\d{2})", q)
                if year_match:
                    year = year_match.group(1)
                    if year in years:
                        value = years[year]

                        # 🧠 Store fact memory
                        chat_history.append({
                            "fact": f"{item} {year}",
                            "value": value
                        })

                        return f"The {item.title()} for {year} is {value:,}."

    # -------------------------------------------------
    # 2️⃣ SIMPLE COMPARISON / CHANGE (NO LLM)
    # -------------------------------------------------
    if excel_data and any(k in q for k in ["compare", "increase", "decrease", "difference"]):
        for item, years in excel_data.items():
            if item in q and len(years) >= 2:
                sorted_years = sorted(years.keys())
                y1, y2 = sorted_years[-2], sorted_years[-1]
                diff = years[y2] - years[y1]

                # 🧠 Store comparison as fact
                chat_history.append({
                    "fact": f"{item} change {y1}-{y2}",
                    "value": diff
                })

                return (
                    f"The {item.title()} changed from {years[y1]:,} in {y1} "
                    f"to {years[y2]:,} in {y2}, a difference of {diff:,}."
                )

    # -------------------------------------------------
    # 3️⃣ BUILD FACT MEMORY (ChatGPT-like context)
    # -------------------------------------------------
    known_facts = []
    for entry in chat_history:
        if isinstance(entry, dict) and "fact" in entry:
            known_facts.append(
                f"- {entry['fact'].title()}: {entry['value']:,}"
            )

    facts_text = "\n".join(known_facts) if known_facts else "None yet."

    # -------------------------------------------------
    # 4️⃣ LLM FALLBACK (EXPLANATIONS / FOLLOW-UPS)
    # -------------------------------------------------
    if excel_data:
        data_context = "\n".join(
            f"{item.title()}: {values}"
            for item, values in excel_data.items()
        )
    else:
        data_context = (pdf_text or "")[:1200]

    context = f"""
KNOWN FACTS FROM THIS CONVERSATION:
{facts_text}

AVAILABLE DOCUMENT DATA:
{data_context}
"""

    return ask_ollama(
        question=question,
        context=context,
        chat_history=chat_history
    )