
"""
GetHired

Enterprise V5 Resume Section Model

Parser-layer object representing one logical section
of a resume.

This belongs to the RESUME PARSER layer.

It must NOT depend on the Knowledge Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass
class ResumeSection:
    """
    Represents one logical resume section.

    Example
    -------
    ResumeSection(
        name="experience",
        items=[
            "QA Chemist | Coca-Cola...",
            "Led quality improvement..."
        ]
    )
    """

    # ============================================================
    # SECTION IDENTITY
    # ============================================================

    name: str = ""

    # Human-readable / canonical section name
    title: str = ""

    # ============================================================
    # SECTION CONTENT
    # ============================================================

    items: list[Any] = field(
        default_factory=list
    )

    # ============================================================
    # SOURCE INFORMATION
    # ============================================================

    start_index: int = -1

    end_index: int = -1

    # ============================================================
    # CONVENIENCE
    # ============================================================

    @property
    def item_count(self) -> int:
        """
        Number of items contained in the section.
        """

        return len(self.items)

    @property
    def text(self) -> str:
        """
        Return section content as newline-separated text.
        """

        return "\n".join(
            item.text
            if hasattr(item, "text")
            else str(item)
            for item in self.items
        )

    @property
    def is_empty(self) -> bool:
        """
        Return True when the section has no content.
        """

        return not bool(self.items)

    # ============================================================
    # ITERATION
    # ============================================================

    def __iter__(self) -> Iterator[Any]:
        """
        Allow:

            for item in section:
                ...
        """

        return iter(self.items)

    def __len__(self) -> int:
        """
        Allow:

            len(section)
        """

        return len(self.items)

    def __getitem__(self, index: int) -> Any:
        """
        Allow:

            section[0]
        """

        return self.items[index]

    # ============================================================
    # DEBUG
    # ============================================================

    def __repr__(self) -> str:

        return (
            "ResumeSection("
            f"name={self.name!r}, "
            f"title={self.title!r}, "
            f"items={len(self.items)!r}, "
            f"start_index={self.start_index!r}, "
            f"end_index={self.end_index!r}"
            ")"
        )

