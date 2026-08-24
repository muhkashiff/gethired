"""
Enterprise education equivalency engine.

Purpose
-------
Provide one deterministic, explainable education acceptance policy for:

* JD requirement matching
* candidate-facing match results
* ATS keyword satisfaction

The engine treats education as an ordered qualification hierarchy while
respecting field/major constraints when the JD explicitly names a field.

Default hierarchy:

    PhD / Doctorate  >  Master  >  Bachelor  >  Associate  >  Diploma  >  Certificate

A higher academic level satisfies a lower level requirement when the JD does
not impose a narrower field/credential constraint.

Examples
--------

    JD: Bachelor's degree
    Resume: M.Sc. Chemistry
    -> MATCHED (master is above bachelor)

    JD: Bachelor's degree in Computer Science
    Resume: M.Sc. Computer Science
    -> MATCHED (higher level + relevant field)

    JD: Bachelor's degree in Computer Science
    Resume: M.Sc. Chemistry
    -> PARTIAL / UNMATCHED depending on caller policy; field mismatch is explicit
       and never silently treated as an education match.

    JD: Master's degree
    Resume: Bachelor's degree
    -> NOT MATCHED
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable


@dataclass(frozen=True)
class EducationMatch:
    matched: bool
    score: float
    reason: str
    required_level: str = ""
    candidate_level: str = ""
    candidate_degree: str = ""
    candidate_major: str = ""
    field_required: bool = False
    field_matched: bool = True
    equivalent: bool = False


class EducationEquivalence:
    """Deterministic education-level and field-equivalence policy."""

    # Higher numeric value means a higher academic level.
    LEVEL_RANK = {
        "certificate": 1,
        "diploma": 2,
        "associate": 3,
        "bachelor": 4,
        "master": 5,
        "phd": 6,
    }

    LEVEL_ALIASES = {
        "certificate": "certificate",
        "certification": "certificate",
        "credential": "certificate",
        "diploma": "diploma",
        "associate": "associate",
        "associate degree": "associate",
        "bachelor": "bachelor",
        "bachelors": "bachelor",
        "bachelor's": "bachelor",
        "undergraduate": "bachelor",
        "master": "master",
        "masters": "master",
        "master's": "master",
        "postgraduate": "master",
        "post-graduate": "master",
        "phd": "phd",
        "ph.d": "phd",
        "doctorate": "phd",
        "doctoral": "phd",
        "dphil": "phd",
    }

    LEVEL_PATTERNS = (
        (re.compile(r"\b(?:ph\.?\s*d\.?|d\.?\s*phil\.?|doctorate|doctoral)\b", re.I), "phd"),
        (re.compile(r"\b(?:m\.?\s*sc\.?|m\.?\s*s\.?|m\.?\s*a\.?|m\.?\s*b\.?\s*a\.?|m\.?\s*eng\.?|m\.?\s*tech\.?|master(?:'s)?|post[-\s]?graduate)\b", re.I), "master"),
        (re.compile(r"\b(?:b\.?\s*sc\.?|b\.?\s*s\.?|b\.?\s*a\.?|b\.?\s*eng\.?|b\.?\s*tech\.?|bachelor(?:'s)?|undergraduate)\b", re.I), "bachelor"),
        (re.compile(r"\b(?:associate(?:'s)?\s+degree|associate)\b", re.I), "associate"),
        (re.compile(r"\b(?:diploma|post[-\s]?graduate\s+diploma)\b", re.I), "diploma"),
        (re.compile(r"\b(?:certificate|certification|credential)\b", re.I), "certificate"),
    )

    # Common academic stopwords. They are deliberately small: the field
    # matcher should remain explainable rather than pretending to be a full
    # semantic embedding model.
    STOPWORDS = {
        "a", "an", "and", "or", "the", "of", "in", "on", "for", "with",
        "degree", "degrees", "qualification", "qualifications", "equivalent",
        "relevant", "related", "field", "area", "discipline", "major",
        "preferred", "required", "minimum", "must", "candidate", "relevant",
    }

    @classmethod
    def normalize(cls, value: Any) -> str:
        text = str(value or "").casefold()
        text = text.replace("&", " and ")
        text = re.sub(r"[^a-z0-9+#.]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def infer_level(cls, value: Any) -> str:
        """Infer the normalized academic level from level/degree text."""
        text = cls.normalize(value)
        if not text:
            return ""

        # Explicit normalized level wins.
        if text in cls.LEVEL_ALIASES:
            return cls.LEVEL_ALIASES[text]

        for pattern, level in cls.LEVEL_PATTERNS:
            if pattern.search(text):
                return level
        return ""

    @classmethod
    def _text_value(cls, value: Any) -> str:
        """Convert scalar/list/dict structured evidence into safe text.

        Resume education fields are not guaranteed to be scalar strings.
        In particular, ``keywords`` is a list[str] in the canonical Education
        model. This helper keeps all downstream matching string-safe while
        preserving useful values for explainable evidence.
        """
        if value is None:
            return ""

        if isinstance(value, str):
            return value.strip()

        if isinstance(value, (list, tuple, set)):
            parts = [cls._text_value(item) for item in value]
            return " ".join(part for part in parts if part).strip()

        if isinstance(value, dict):
            parts = [cls._text_value(item) for item in value.values()]
            return " ".join(part for part in parts if part).strip()

        return str(value).strip()

    @classmethod
    def candidate_level(cls, education: Any) -> str:
        explicit = cls._value(education, "level")
        level = cls.infer_level(explicit)
        if level:
            return level
        return cls.infer_level(cls._value(education, "degree"))

    @classmethod
    def candidate_text(cls, education: Any) -> str:
        return " ".join(
            part
            for part in (
                cls._text_value(cls._value(education, "degree")),
                cls._text_value(cls._value(education, "major")),
                cls._text_value(cls._value(education, "keywords")),
                cls._text_value(cls._value(education, "description")),
            )
            if part
        ).strip()

    @classmethod
    def match_requirement(
        cls,
        requirement: Any,
        education_records: Iterable[Any],
    ) -> EducationMatch:
        evidence = cls._value(requirement, "evidence")
        subject = cls._value(requirement, "subject")
        metadata = cls._value(requirement, "metadata")
        metadata = metadata if isinstance(metadata, dict) else {}

        jd_text = " ".join(part for part in (subject, evidence) if part).strip()
        required_level = (
            cls.infer_level(metadata.get("education_level"))
            or cls.infer_level(jd_text)
        )

        # A generic "degree" requirement is treated as bachelor's-level by
        # default because that is the conventional minimum academic degree in
        # professional JDs. Higher levels still satisfy it.
        if not required_level and re.search(r"\bdegree\b", cls.normalize(jd_text)):
            required_level = "bachelor"

        field_terms = metadata.get("education_field_terms")
        if not field_terms:
            field_terms = cls.extract_field_terms(jd_text)
        elif isinstance(field_terms, str):
            field_terms = [field_terms]
        field_terms = [cls.normalize(term) for term in field_terms if cls.normalize(term)]

        records = list(education_records or ())
        if not records:
            return EducationMatch(
                matched=False,
                score=0.0,
                reason="No structured education evidence was found in the resume.",
                required_level=required_level,
                field_required=bool(field_terms),
                field_matched=False if field_terms else True,
            )

        best: EducationMatch | None = None
        for education in records:
            candidate_degree = cls._text_value(cls._value(education, "degree"))
            candidate_major = cls._text_value(cls._value(education, "major"))
            candidate_level = cls.candidate_level(education)
            if not candidate_level:
                continue

            candidate_field_text = cls.normalize(
                " ".join(
                    part
                    for part in (
                        candidate_degree,
                        candidate_major,
                        cls._text_value(cls._value(education, "keywords")),
                    )
                    if part
                )
            )

            field_required = bool(field_terms)
            field_matched = True
            field_score = 1.0

            if field_required:
                field_score = cls._field_similarity(field_terms, candidate_field_text)
                field_matched = field_score >= 0.45

            required_rank = cls.LEVEL_RANK.get(required_level, 0)
            candidate_rank = cls.LEVEL_RANK.get(candidate_level, 0)

            if required_rank == 0:
                level_ok = True
                level_score = 0.80
            else:
                level_ok = candidate_rank >= required_rank
                if candidate_rank >= required_rank:
                    level_score = 1.0 if candidate_rank == required_rank else 0.96
                elif candidate_rank == required_rank - 1:
                    level_score = 0.45
                else:
                    level_score = 0.0

            matched = level_ok and field_matched
            if matched:
                if candidate_rank > required_rank:
                    reason = (
                        f"Candidate holds a {candidate_level} qualification, "
                        f"which is above the required {required_level} level."
                    )
                    equivalent = True
                else:
                    reason = f"Candidate holds the required {candidate_level} education level."
                    equivalent = False

                if field_required:
                    reason += " The stated field/major is relevant to the JD requirement."

                score = min(1.0, 0.96 * level_score * field_score)
            else:
                if not level_ok:
                    reason = (
                        f"Candidate's highest detected level ({candidate_level}) "
                        f"does not meet the required {required_level} level."
                    )
                else:
                    reason = (
                        "Candidate meets the education level, but the stated "
                        "field/major is not sufficiently aligned with the JD."
                    )
                score = min(0.79, 0.60 * level_score + 0.20 * field_score)
                equivalent = False

            candidate_result = EducationMatch(
                matched=matched,
                score=score,
                reason=reason,
                required_level=required_level,
                candidate_level=candidate_level,
                candidate_degree=candidate_degree,
                candidate_major=candidate_major,
                field_required=field_required,
                field_matched=field_matched,
                equivalent=equivalent,
            )

            if best is None or candidate_result.score > best.score:
                best = candidate_result

        if best is None:
            return EducationMatch(
                matched=False,
                score=0.0,
                reason="Resume education records were present but no recognized academic level could be determined.",
                required_level=required_level,
                field_required=bool(field_terms),
                field_matched=False if field_terms else True,
            )
        return best

    @classmethod
    def match_keyword(
        cls,
        keyword: str,
        education_records: Iterable[Any],
        requirement: Any = None,
    ) -> EducationMatch:
        """Match an ATS education keyword against structured resume education."""
        keyword = str(keyword or "").strip()
        if not keyword or not cls.looks_like_education(keyword):
            return EducationMatch(False, 0.0, "Not an education keyword.")

        if requirement is not None:
            return cls.match_requirement(requirement, education_records)

        required_level = cls.infer_level(keyword)
        if not required_level:
            required_level = "bachelor" if "degree" in cls.normalize(keyword) else ""

        best = None
        for education in education_records or ():
            candidate_level = cls.candidate_level(education)
            candidate_rank = cls.LEVEL_RANK.get(candidate_level, 0)
            required_rank = cls.LEVEL_RANK.get(required_level, 0)
            if required_rank and candidate_rank >= required_rank:
                result = EducationMatch(
                    True,
                    0.96 if candidate_rank > required_rank else 1.0,
                    f"Candidate's {candidate_level} qualification satisfies the {required_level} education keyword.",
                    required_level=required_level,
                    candidate_level=candidate_level,
                    candidate_degree=cls._text_value(cls._value(education, "degree")),
                    candidate_major=cls._text_value(cls._value(education, "major")),
                    equivalent=candidate_rank > required_rank,
                )
            else:
                result = EducationMatch(
                    False,
                    0.0,
                    f"Candidate's education does not meet the {required_level or 'requested'} level.",
                    required_level=required_level,
                    candidate_level=candidate_level,
                    candidate_degree=cls._text_value(cls._value(education, "degree")),
                    candidate_major=cls._text_value(cls._value(education, "major")),
                )
            if best is None or result.score > best.score:
                best = result
        return best or EducationMatch(False, 0.0, "No structured education evidence was found in the resume.", required_level=required_level)

    @classmethod
    def looks_like_education(cls, text: str) -> bool:
        value = cls.normalize(text)
        return bool(cls.infer_level(value) or re.search(r"\bdegree\b|\bqualification\b|\bequivalent\b", value))

    @classmethod
    def extract_field_terms(cls, text: str) -> list[str]:
        """Extract explicit academic field hints from JD wording."""
        value = cls.normalize(text)
        if not value:
            return []

        # Only treat the clause after "in" / "of" as a field when it is
        # attached to an education phrase. This avoids interpreting arbitrary
        # words such as "degree in the role" as an academic field.
        match = re.search(
            r"(?:degree|bachelor(?:'s)?|master(?:'s)?|ph\.?d\.?|doctorate)\s+(?:degree\s+)?(?:in|of)\s+(.+)$",
            value,
            re.I,
        )
        if not match:
            return []

        clause = re.split(
            r"\b(?:or|and|with|plus|preferred|required|equivalent)\b",
            match.group(1),
            maxsplit=1,
            flags=re.I,
        )[0]
        tokens = [token for token in cls.normalize(clause).split() if token not in cls.STOPWORDS]
        if not tokens:
            return []
        return [" ".join(tokens)]

    @classmethod
    def _field_similarity(cls, required_terms: list[str], candidate_text: str) -> float:
        candidate_tokens = {
            token for token in cls.normalize(candidate_text).split()
            if token not in cls.STOPWORDS
        }
        if not candidate_tokens:
            return 0.0

        best = 0.0
        for term in required_terms:
            required_tokens = {
                token for token in cls.normalize(term).split()
                if token not in cls.STOPWORDS
            }
            if not required_tokens:
                continue
            if " ".join(sorted(required_tokens)) in " ".join(sorted(candidate_tokens)):
                best = max(best, 1.0)
            overlap = len(required_tokens & candidate_tokens) / max(len(required_tokens), 1)
            best = max(best, overlap)

            # Common academic abbreviations and obvious stem relationships.
            for token in required_tokens:
                if any(token in candidate or candidate in token for candidate in candidate_tokens if len(token) >= 4):
                    best = max(best, 0.60)
        return min(best, 1.0)

    @staticmethod
    def _value(obj: Any, name: str) -> Any:
        if isinstance(obj, dict):
            return obj.get(name, "")
        return getattr(obj, name, "")


__all__ = ["EducationMatch", "EducationEquivalence"]
