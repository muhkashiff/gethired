"""
Enterprise JD non-ontology requirement extraction.

This module deliberately sits beside the ontology pipeline.  It extracts
requirements that cannot safely be represented by ontology JSON alone:
section semantics, education, experience wording, languages, location/work
authorization, employment type, schedule, travel, compensation, and generic
qualification evidence.

It is deterministic, explainable, dependency-free, and safe to run before or
after ontology extraction.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable


@dataclass(frozen=True)
class JDSectionContext:
    name: str = ""
    kind: str = "contextual"
    priority: str = "contextual"
    line_number: int = 0


@dataclass(frozen=True)
class JDNonOntologyEvidence:
    kind: str
    subject: str
    evidence: str
    section: str = ""
    priority: str = "contextual"
    line_number: int = 0
    minimum_years: float | None = None
    confidence: float = 0.0
    metadata: dict[str, object] = field(default_factory=dict)


class JDNonOntologyExtractor:
    """Extract structured JD evidence without requiring ontology entries."""

    _HEADING_ALIASES = {
        "responsibility": {
            "responsibilities", "key responsibilities", "primary responsibilities",
            "role responsibilities", "duties", "key duties", "essential duties",
            "job duties", "what youll do", "what you will do", "what youll be doing",
            "your responsibilities", "main responsibilities",
        },
        "required": {
            "requirements", "required", "required qualifications", "minimum qualifications",
            "minimum requirements", "essential qualifications", "must have", "must-have",
            "required skills", "candidate requirements", "qualifications", "essential requirements",
        },
        "preferred": {
            "preferred", "preferred qualifications", "preferred experience", "preferred skills",
            "preferred requirements", "desired qualifications", "desired skills", "nice to have",
            "nice-to-have", "additional qualifications", "preferred background",
        },
        "education": {
            "education", "educational requirements", "educational qualifications",
            "academic qualifications", "academic requirements", "degree requirements",
            "academic background",
        },
        "experience": {
            "experience", "required experience", "professional experience", "industry experience",
            "experience requirements", "relevant experience", "work experience requirements",
        },
        "language": {
            "language", "languages", "language requirements", "language skills",
            "language proficiency",
        },
        "location": {
            "location", "job location", "work location", "location requirements", "work arrangement",
            "remote", "hybrid", "onsite", "on-site",
        },
        "work_authorization": {
            "work authorization", "work eligibility", "eligibility to work", "visa", "visa sponsorship",
            "right to work", "employment authorization",
        },
        "employment_type": {
            "employment type", "job type", "position type", "contract type", "employment status",
        },
        "schedule": {
            "schedule", "working hours", "work hours", "shift", "shifts", "working schedule",
            "hours", "availability",
        },
        "travel": {
            "travel", "travel requirements", "travel required", "travel expectations",
        },
        "compensation": {
            "salary", "compensation", "pay", "salary and benefits", "benefits", "remuneration",
        },
    }

    _REQUIRED_RE = re.compile(
        r"\b(?:required|required to|must|mandatory|essential|minimum|need to|needs to|shall|compulsory)\b",
        re.I,
    )
    _PREFERRED_RE = re.compile(
        r"\b(?:preferred|preferably|desired|desirable|highly preferred|nice to have|nice-to-have|plus|advantageous|would be an advantage|an advantage)\b",
        re.I,
    )
    _YEARS_RE = re.compile(
        r"\b(?:at\s+least\s+|minimum\s+|over\s+|more\s+than\s+)?(\d+(?:\.\d+)?)\s*\+?\s*years?\b",
        re.I,
    )
    _EDUCATION_RE = re.compile(
        r"\b(?:bachelor(?:'s)?|master(?:'s)?|ph\.?d\.?|doctorate|doctoral|associate(?:'s)?|diploma|degree|certificate|certification|postgraduate|post-graduate|undergraduate)\b",
        re.I,
    )
    _CERTIFICATION_RE = re.compile(
        r"\b(?:certification|certified|license|licence|accreditation|credential)\b",
        re.I,
    )
    _LANGUAGE_NAMES = {
        "english", "urdu", "arabic", "french", "spanish", "german", "italian", "portuguese",
        "russian", "mandarin", "chinese", "hindi", "bengali", "punjabi", "pashto", "persian",
        "turkish", "dutch", "japanese", "korean",
    }
    _LOCATION_RE = re.compile(
        r"\b(?:located in|based in|location(?:\s*required)?|work from|onsite in|on-site in|remote from|hybrid in)\b\s*[:\-]?\s*(.+)$",
        re.I,
    )
    _WORK_AUTH_RE = re.compile(
        r"\b(?:authorized|authorised|eligible|eligibility|visa sponsorship|sponsorship|right to work|work authorization|work authori[sz]ation)\b",
        re.I,
    )
    _TRAVEL_RE = re.compile(
        r"\b(?:travel|traveling|travelling|willing to travel|travel up to)\b",
        re.I,
    )
    _SCHEDULE_RE = re.compile(
        r"\b(?:shift|shifts|night shift|day shift|weekend|working hours|work hours|schedule|availability|flexible hours)\b",
        re.I,
    )
    _EMPLOYMENT_RE = re.compile(
        r"\b(?:full[- ]time|part[- ]time|contract|temporary|permanent|freelance|internship|intern|hybrid|remote|on[- ]site|onsite)\b",
        re.I,
    )
    _COMPENSATION_RE = re.compile(
        r"(?:\$|€|£|₨|salary|compensation|pay range|hourly rate|per hour|per annum|annual salary)",
        re.I,
    )

    def extract(self, text: str | Iterable[str]) -> list[JDNonOntologyEvidence]:
        lines = self._lines(text)
        if not lines:
            return []

        result: list[JDNonOntologyEvidence] = []
        context = JDSectionContext()

        for index, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue

            heading = self._heading(line)
            if heading:
                context = JDSectionContext(
                    name=heading[0],
                    kind=heading[1],
                    priority=self._heading_priority(heading[1]),
                    line_number=index,
                )
                continue

            content = self._clean_bullet(line)
            if not content:
                continue

            kind = self._infer_kind(content, context.kind)
            priority = self.priority_for_text(content, context)
            years = self._years(content)

            # Responsibilities remain visible as contextual evidence.  The
            # ontology classifier may add action-backed requirements; the
            # classifier later de-duplicates by evidence.
            if kind == "responsibility":
                result.append(self._evidence(
                    kind, content, content, context, priority, index, years, 0.84
                ))
                continue

            # Ignore generic prose outside requirement-like sections unless it
            # contains explicit requirement language.
            requirement_like = context.kind in {
                "required", "preferred", "education", "experience", "language",
                "location", "work_authorization", "employment_type", "schedule",
                "travel", "compensation",
            } or self._REQUIRED_RE.search(content) or self._PREFERRED_RE.search(content)
            if not requirement_like:
                continue

            subject = self._subject(content, kind)
            if not subject:
                continue

            result.append(self._evidence(
                kind, subject, content, context, priority, index, years,
                self._confidence(kind, context, content),
            ))

        return self._dedupe(result)

    def context_for_text(self, text: str, source_text: str) -> JDSectionContext:
        """Resolve the best section context for a semantic statement."""
        lines = self._lines(source_text)
        if not lines or not text:
            return JDSectionContext()

        contexts: list[tuple[str, str, str, int]] = []
        current = JDSectionContext()
        for index, raw in enumerate(lines, start=1):
            line = raw.strip()
            heading = self._heading(line) if line else None
            if heading:
                current = JDSectionContext(
                    name=heading[0], kind=heading[1],
                    priority=self._heading_priority(heading[1]), line_number=index,
                )
                continue
            if line:
                contexts.append((line, current.name, current.kind, current.line_number))

        target = self._norm(text)
        if not target:
            return JDSectionContext()

        best = None
        best_score = 0.0
        target_tokens = set(target.split())
        for line, name, kind, heading_line in contexts:
            candidate = self._norm(self._clean_bullet(line))
            if not candidate:
                continue
            if target == candidate or target in candidate or candidate in target:
                score = 1.0
            else:
                tokens = set(candidate.split())
                score = len(target_tokens & tokens) / max(len(target_tokens | tokens), 1)
            if score > best_score:
                best_score = score
                best = JDSectionContext(
                    name=name, kind=kind,
                    priority=self._heading_priority(kind),
                    line_number=heading_line,
                )

        if best is None:
            return JDSectionContext()

        # Explicit wording in the source line outranks the section heading.
        matched_line = next(
            (line for line, name, kind, heading_line in contexts
             if name == best.name and kind == best.kind and
             (target == self._norm(self._clean_bullet(line)) or
              target in self._norm(self._clean_bullet(line)) or
              self._norm(self._clean_bullet(line)) in target)),
            "",
        )
        priority = self.priority_for_text(matched_line, best)
        return JDSectionContext(best.name, best.kind, priority, best.line_number)

    def priority_for_text(self, text: str, context: JDSectionContext | None = None) -> str:
        normalized = (text or "").casefold()
        # Responsibility sections are contextual by definition in the
        # candidate-facing requirement summary.
        if context and context.kind == "responsibility":
            return "contextual"
        if self._PREFERRED_RE.search(normalized):
            return "preferred"
        if self._REQUIRED_RE.search(normalized):
            return "required"
        if context and context.priority in {"required", "preferred"}:
            return context.priority
        return "contextual"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _lines(text: str | Iterable[str]) -> list[str]:
        if text is None:
            return []
        if isinstance(text, str):
            return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        return [str(item) for item in text]

    @classmethod
    def _heading(cls, line: str) -> tuple[str, str] | None:
        value = cls._norm(line)
        if not value or len(value) > 80:
            return None
        for kind, aliases in cls._HEADING_ALIASES.items():
            if value in aliases:
                return (line.strip(), kind)
        # Common numbered/bold-like headings.
        stripped = re.sub(r"^\d+[.)]\s*", "", value)
        for kind, aliases in cls._HEADING_ALIASES.items():
            if stripped in aliases:
                return (line.strip(), kind)
        return None

    @staticmethod
    def _heading_priority(kind: str) -> str:
        if kind == "required":
            return "required"
        if kind == "preferred":
            return "preferred"
        if kind in {"education", "experience", "language", "location", "work_authorization", "employment_type", "schedule", "travel", "compensation"}:
            return "required"
        return "contextual"

    @classmethod
    def _infer_kind(cls, text: str, section_kind: str) -> str:
        if section_kind == "responsibility":
            return "responsibility"
        if section_kind == "education" or cls._EDUCATION_RE.search(text):
            return "education"
        if section_kind == "language" or cls._looks_like_language(text):
            return "language"
        if section_kind == "work_authorization" or cls._WORK_AUTH_RE.search(text):
            return "work_authorization"
        if section_kind == "location" or cls._LOCATION_RE.search(text):
            return "location"
        if section_kind == "employment_type" or cls._EMPLOYMENT_RE.search(text):
            return "employment_type"
        if section_kind == "schedule" or cls._SCHEDULE_RE.search(text):
            return "schedule"
        if section_kind == "travel" or cls._TRAVEL_RE.search(text):
            return "travel"
        if section_kind == "compensation" or cls._COMPENSATION_RE.search(text):
            return "compensation"
        if cls._CERTIFICATION_RE.search(text):
            return "certification"
        if section_kind == "experience" or cls._YEARS_RE.search(text) or re.search(r"\bexperience\b", text, re.I):
            return "experience"
        return "qualification"

    @classmethod
    def _subject(cls, text: str, kind: str) -> str:
        if kind == "education":
            # Preserve the actual qualification phrase (for example
            # "Bachelor's degree or equivalent qualification") instead of
            # deleting the degree level. The education equivalency matcher
            # needs that level to decide whether a higher credential such as
            # an M.Sc. satisfies a Bachelor requirement.
            value = cls._clean_subject(text, None)
            value = re.sub(
                r"\b(?:is|are|was|were)\s+(?:required|mandatory|essential|preferred|desired|highly preferred)\b.*$",
                "",
                value,
                flags=re.I,
            )
            return value
        if kind == "experience":
            years_removed = cls._YEARS_RE.sub("", text)
            years_removed = re.sub(r"\b(?:of\s+)?experience\b", "experience", years_removed, flags=re.I)
            return cls._clean_subject(years_removed, None) or "relevant professional experience"
        if kind == "language":
            names = [name.title() for name in cls._LANGUAGE_NAMES if re.search(rf"\b{re.escape(name)}\b", text, re.I)]
            if names:
                return ", ".join(dict.fromkeys(names))
            return cls._clean_subject(text, None)
        if kind == "location":
            match = cls._LOCATION_RE.search(text)
            return (match.group(1).strip(" .") if match else cls._clean_subject(text, None))
        if kind == "responsibility":
            return cls._clean_subject(text, None)
        return cls._clean_subject(text, None)

    @staticmethod
    def _clean_subject(text: str, pattern: re.Pattern | None) -> str:
        value = text.strip().lstrip("•▪●*-–— ").strip()
        if pattern is not None:
            # Keep the useful phrase but remove boilerplate requirement tails.
            value = pattern.sub("", value, count=1).strip(" ,;:-") or text.strip()
        value = re.sub(
            r"\b(?:is|are|was|were)\s+(?:required|mandatory|essential|preferred|desired|highly preferred)\b.*$",
            "",
            value,
            flags=re.I,
        )
        value = re.sub(
            r"\b(?:is|are)\s+(?:highly\s+)?preferred\b.*$",
            "",
            value,
            flags=re.I,
        )
        value = re.sub(r"\s+", " ", value).strip(" .,:;-–—")
        return value

    @classmethod
    def _looks_like_language(cls, text: str) -> bool:
        if any(re.search(rf"\b{re.escape(name)}\b", text, re.I) for name in cls._LANGUAGE_NAMES):
            return True
        return bool(re.search(r"\b(?:fluent|proficient|native|bilingual|conversational|written|spoken)\b", text, re.I))

    @classmethod
    def _years(cls, text: str) -> float | None:
        match = cls._YEARS_RE.search(text)
        return float(match.group(1)) if match else None

    @classmethod
    def _confidence(cls, kind: str, context: JDSectionContext, text: str) -> float:
        base = {
            "education": 0.96,
            "experience": 0.94,
            "language": 0.92,
            "certification": 0.92,
            "work_authorization": 0.90,
            "location": 0.88,
            "employment_type": 0.88,
            "schedule": 0.86,
            "travel": 0.86,
            "compensation": 0.82,
            "qualification": 0.78,
            "responsibility": 0.84,
        }.get(kind, 0.75)
        if context.priority in {"required", "preferred"}:
            base += 0.03
        if cls._REQUIRED_RE.search(text) or cls._PREFERRED_RE.search(text):
            base += 0.02
        return min(base, 0.99)

    @staticmethod
    def _clean_bullet(line: str) -> str:
        return re.sub(r"^\s*(?:[-*•▪●◦‣–—]+|\d+[.)])\s*", "", line).strip()

    @staticmethod
    def _norm(value: str) -> str:
        value = re.sub(r"[^\w+#]+", " ", value.casefold(), flags=re.UNICODE)
        return re.sub(r"\s+", " ", value).strip()

    @staticmethod
    def _evidence(kind, subject, evidence, context, priority, line_number, years, confidence):
        metadata = {
            "source": "jd_non_ontology_extractor",
            "section_kind": context.kind,
        }

        if kind == "education":
            from app.intelligence.utilities.knowledge.education.education_equivalence import (
                EducationEquivalence,
            )

            metadata["education_level"] = EducationEquivalence.infer_level(evidence)
            metadata["education_field_terms"] = EducationEquivalence.extract_field_terms(evidence)
            metadata["accept_higher_levels"] = True

        return JDNonOntologyEvidence(
            kind=kind,
            subject=subject,
            evidence=evidence,
            section=context.name,
            priority=priority,
            line_number=line_number,
            minimum_years=years,
            confidence=confidence,
            metadata=metadata,
        )

    @classmethod
    def _dedupe(cls, items: list[JDNonOntologyEvidence]) -> list[JDNonOntologyEvidence]:
        seen = set()
        result = []
        for item in items:
            key = (item.kind, cls._norm(item.subject), item.priority, cls._norm(item.evidence))
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
        return result


__all__ = [
    "JDSectionContext",
    "JDNonOntologyEvidence",
    "JDNonOntologyExtractor",
]
