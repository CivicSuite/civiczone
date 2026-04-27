# Milestone 5 Done

Milestone 5 produced citation-grounded sample resident Q&A:

- `answer_zoning_question()` for ADU and setback sample questions.
- `POST /api/v1/civiczone/questions/answer`.
- Every answered response includes citations and the non-determination disclaimer.
- Determination requests escalate.
- Unknown/uncited questions are refused.

Still not shipped:

- Live LLM calls.
- Live GIS import.
- Staff review queue.
- Public workflow UI.
