from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from civiczone.qa import ZoneAnswer, answer_zoning_question
from civiczone.rule_lookup import DISCLAIMER


STAFF_VISIBILITY = "staff_only"
OPEN_QUEUE_STATUSES = {"open", "in_review"}
RESOLVED_QUEUE_STATUSES = {"resolved", "closed"}
QUEUE_STATUSES = OPEN_QUEUE_STATUSES | RESOLVED_QUEUE_STATUSES


@dataclass(frozen=True)
class CodeCrossReference:
    citation: str
    source: str
    relevance: str


@dataclass(frozen=True)
class StaffQuestionRecord:
    id: str
    zone_code: str
    question_text: str
    status: str
    answer_text: str
    citations: tuple[str, ...]
    code_cross_references: tuple[CodeCrossReference, ...]
    created_by: str
    created_at: datetime
    visibility: str = STAFF_VISIBILITY
    disclaimer: str = DISCLAIMER


@dataclass(frozen=True)
class AmbiguityReviewItem:
    id: str
    zone_code: str
    question_text: str
    reason: str
    status: str
    assigned_to: str | None
    resolution: str | None
    source_question_id: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime
    visibility: str = STAFF_VISIBILITY


@dataclass(frozen=True)
class HighVolumeQuestion:
    zone_code: str
    question_text: str
    count: int
    statuses: tuple[str, ...]
    latest_question_id: str


@dataclass(frozen=True)
class StaffQuestionAnalytics:
    total_questions: int
    by_status: dict[str, int]
    high_volume_questions: tuple[HighVolumeQuestion, ...]
    generated_at: datetime
    visibility: str = STAFF_VISIBILITY


@dataclass(frozen=True)
class StaffReportOutline:
    id: str
    title: str
    sections: tuple[dict[str, object], ...]
    source_question_ids: tuple[str, ...]
    source_queue_item_ids: tuple[str, ...]
    created_by: str
    created_at: datetime
    visibility: str = STAFF_VISIBILITY
    disclaimer: str = "Draft staff outline only; verify citations before publication."


@dataclass(frozen=True)
class FlaggedAnswerReview:
    id: str
    zone_code: str
    question_text: str
    original_answer: str
    flag_reason: str
    citations: tuple[str, ...]
    status: str
    improved_answer: str | None
    improvement_notes: str | None
    reviewed_by: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime
    visibility: str = STAFF_VISIBILITY


class StaffWorkflowStore:
    """In-process staff workflow data store for local v1 staff API behavior."""

    def __init__(self) -> None:
        self._questions: dict[str, StaffQuestionRecord] = {}
        self._queue: dict[str, AmbiguityReviewItem] = {}
        self._flagged_answers: dict[str, FlaggedAnswerReview] = {}

    def answer_planner_question(
        self,
        *,
        zone_code: str,
        question_text: str,
        created_by: str,
    ) -> StaffQuestionRecord:
        answer = answer_zoning_question(zone_code=zone_code, question=question_text)
        record = StaffQuestionRecord(
            id=str(uuid4()),
            zone_code=zone_code.strip().upper(),
            question_text=question_text,
            status=answer.status,
            answer_text=answer.answer,
            citations=tuple(answer.citations),
            code_cross_references=_cross_references_from_answer(answer),
            created_by=created_by,
            created_at=datetime.now(UTC),
        )
        self._questions[record.id] = record
        if answer.status in {"escalate", "refused"}:
            self.create_queue_item(
                zone_code=record.zone_code,
                question_text=record.question_text,
                reason=answer.next_step,
                created_by=created_by,
                source_question_id=record.id,
            )
        return record

    def create_queue_item(
        self,
        *,
        zone_code: str,
        question_text: str,
        reason: str,
        created_by: str,
        source_question_id: str | None = None,
    ) -> AmbiguityReviewItem:
        now = datetime.now(UTC)
        item = AmbiguityReviewItem(
            id=str(uuid4()),
            zone_code=zone_code.strip().upper(),
            question_text=question_text,
            reason=reason,
            status="open",
            assigned_to=None,
            resolution=None,
            source_question_id=source_question_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )
        self._queue[item.id] = item
        return item

    def list_queue_items(self, *, status: str | None = None) -> tuple[AmbiguityReviewItem, ...]:
        items = tuple(sorted(self._queue.values(), key=lambda item: item.created_at))
        if status is None:
            return items
        return tuple(item for item in items if item.status == status)

    def update_queue_item(
        self,
        *,
        item_id: str,
        status: str,
        assigned_to: str | None,
        resolution: str | None,
    ) -> AmbiguityReviewItem | None:
        if status not in QUEUE_STATUSES:
            raise ValueError("status must be one of: closed, in_review, open, resolved.")
        current = self._queue.get(item_id)
        if current is None:
            return None
        if status in RESOLVED_QUEUE_STATUSES and not resolution:
            raise ValueError("resolution is required when resolving or closing a queue item.")
        updated = AmbiguityReviewItem(
            id=current.id,
            zone_code=current.zone_code,
            question_text=current.question_text,
            reason=current.reason,
            status=status,
            assigned_to=assigned_to if assigned_to is not None else current.assigned_to,
            resolution=resolution if resolution is not None else current.resolution,
            source_question_id=current.source_question_id,
            created_by=current.created_by,
            created_at=current.created_at,
            updated_at=datetime.now(UTC),
        )
        self._queue[item_id] = updated
        return updated

    def analytics(self, *, high_volume_threshold: int = 2) -> StaffQuestionAnalytics:
        status_counts = Counter(record.status for record in self._questions.values())
        grouped: dict[tuple[str, str], list[StaffQuestionRecord]] = {}
        for record in self._questions.values():
            key = (record.zone_code, _normalize_question(record.question_text))
            grouped.setdefault(key, []).append(record)

        high_volume: list[HighVolumeQuestion] = []
        for records in grouped.values():
            if len(records) < high_volume_threshold:
                continue
            latest = max(records, key=lambda record: record.created_at)
            high_volume.append(
                HighVolumeQuestion(
                    zone_code=latest.zone_code,
                    question_text=latest.question_text,
                    count=len(records),
                    statuses=tuple(sorted({record.status for record in records})),
                    latest_question_id=latest.id,
                )
            )

        return StaffQuestionAnalytics(
            total_questions=len(self._questions),
            by_status=dict(sorted(status_counts.items())),
            high_volume_questions=tuple(
                sorted(high_volume, key=lambda question: (-question.count, question.question_text))
            ),
            generated_at=datetime.now(UTC),
        )

    def draft_report_outline(
        self,
        *,
        title: str,
        question_ids: Iterable[str],
        queue_item_ids: Iterable[str],
        created_by: str,
    ) -> StaffReportOutline:
        selected_questions = tuple(
            self._questions[question_id]
            for question_id in question_ids
            if question_id in self._questions
        )
        selected_queue_items = tuple(
            self._queue[item_id] for item_id in queue_item_ids if item_id in self._queue
        )
        cited_sections = sorted(
            {citation for question in selected_questions for citation in question.citations}
        )
        sections: tuple[dict[str, object], ...] = (
            {
                "heading": "Issue Summary",
                "prompts": tuple(item.question_text for item in selected_queue_items)
                or tuple(question.question_text for question in selected_questions),
            },
            {
                "heading": "Code Cross-References",
                "citations": tuple(cited_sections),
                "instruction": "Verify each cited section against the authoritative code text.",
            },
            {
                "heading": "Recommended Staff Review",
                "open_queue_items": tuple(
                    item.id for item in selected_queue_items if item.status in OPEN_QUEUE_STATUSES
                ),
                "instruction": "Resolve open ambiguity items before issuing a determination.",
            },
        )
        return StaffReportOutline(
            id=str(uuid4()),
            title=title,
            sections=sections,
            source_question_ids=tuple(question.id for question in selected_questions),
            source_queue_item_ids=tuple(item.id for item in selected_queue_items),
            created_by=created_by,
            created_at=datetime.now(UTC),
        )

    def flag_answer(
        self,
        *,
        zone_code: str,
        question_text: str,
        original_answer: str,
        flag_reason: str,
        citations: Iterable[str],
        created_by: str,
    ) -> FlaggedAnswerReview:
        now = datetime.now(UTC)
        review = FlaggedAnswerReview(
            id=str(uuid4()),
            zone_code=zone_code.strip().upper(),
            question_text=question_text,
            original_answer=original_answer,
            flag_reason=flag_reason,
            citations=tuple(citations),
            status="flagged",
            improved_answer=None,
            improvement_notes=None,
            reviewed_by=None,
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )
        self._flagged_answers[review.id] = review
        return review

    def improve_flagged_answer(
        self,
        *,
        review_id: str,
        improved_answer: str,
        improvement_notes: str,
        reviewed_by: str,
    ) -> FlaggedAnswerReview | None:
        current = self._flagged_answers.get(review_id)
        if current is None:
            return None
        updated = FlaggedAnswerReview(
            id=current.id,
            zone_code=current.zone_code,
            question_text=current.question_text,
            original_answer=current.original_answer,
            flag_reason=current.flag_reason,
            citations=current.citations,
            status="improved",
            improved_answer=improved_answer,
            improvement_notes=improvement_notes,
            reviewed_by=reviewed_by,
            created_by=current.created_by,
            created_at=current.created_at,
            updated_at=datetime.now(UTC),
        )
        self._flagged_answers[review_id] = updated
        return updated


def _cross_references_from_answer(answer: ZoneAnswer) -> tuple[CodeCrossReference, ...]:
    return tuple(
        CodeCrossReference(
            citation=citation,
            source="CivicCode section reference",
            relevance="Supports the planner-facing informational answer.",
        )
        for citation in answer.citations
    )


def _normalize_question(question_text: str) -> str:
    return " ".join(question_text.casefold().split())
