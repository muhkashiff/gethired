"""
GetHired

Enterprise V5 Resume Reader

Reads DOCX resumes while preserving:

- document order
- paragraphs
- tables
- nested tables
- source position
- block type

Canonical input format:
    DOCX

Canonical output:
    ResumeBlock[]

The reader does NOT perform semantic extraction.

Its responsibility is document ingestion only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

from docx import Document
from docx.document import Document as DocxDocument
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl


# ================================================================
# RESUME BLOCK
# ================================================================


@dataclass
class ResumeBlock:

    # ------------------------------------------------------------
    # POSITION
    # ------------------------------------------------------------

    index: int = -1

    # ------------------------------------------------------------
    # CONTENT
    # ------------------------------------------------------------

    text: str = ""

    # ------------------------------------------------------------
    # STRUCTURE
    # ------------------------------------------------------------

    block_type: str = "paragraph"

    section: str = "header"

    # ------------------------------------------------------------
    # DOCUMENT LOCATION
    # ------------------------------------------------------------

    paragraph_index: int = -1

    table_index: int = -1

    row_index: int = -1

    cell_index: int = -1

    parent_block_index: int = -1

    # ------------------------------------------------------------
    # SOURCE
    # ------------------------------------------------------------

    source: str = "docx"

    metadata: dict = field(
        default_factory=dict
    )

    @property
    def is_paragraph(self) -> bool:

        return self.block_type == "paragraph"

    @property
    def is_table(self) -> bool:

        return self.block_type == "table"

    def __repr__(self) -> str:

        return (
            "ResumeBlock("
            f"index={self.index!r}, "
            f"text={self.text!r}, "
            f"block_type={self.block_type!r}, "
            f"section={self.section!r}, "
            f"paragraph_index={self.paragraph_index!r}, "
            f"table_index={self.table_index!r}, "
            f"row_index={self.row_index!r}, "
            f"cell_index={self.cell_index!r}"
            ")"
        )


# ================================================================
# RESUME READER
# ================================================================


class ResumeReader:

    """
    Enterprise DOCX reader.

    Important:

    This class only reads the document.

    It does NOT:

    - detect entities
    - detect ontology
    - analyze skills
    - analyze leadership
    - score candidates
    - analyze JD matching
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        pass

    # ============================================================
    # PUBLIC
    # ============================================================

    def read(
        self,
        file_path,
    ) -> list[ResumeBlock]:

        document = Document(
            Path(file_path)
        )

        blocks = []

        paragraph_index = 0
        table_index = 0

        for block in self.iter_block_items(document):

            # ----------------------------------------------------
            # PARAGRAPH
            # ----------------------------------------------------

            if isinstance(
                block,
                Paragraph,
            ):

                text = block.text.strip()

                if not text:
                    continue

                blocks.append(
                    ResumeBlock(
                        index=len(blocks),
                        text=text,
                        block_type="paragraph",
                        paragraph_index=paragraph_index,
                    )
                )

                paragraph_index += 1

            # ----------------------------------------------------
            # TABLE
            # ----------------------------------------------------

            elif isinstance(
                block,
                Table,
            ):

                table_blocks = self.read_table(
                    block,
                    table_index=table_index,
                    parent_block_index=len(blocks),
                )

                blocks.extend(
                    table_blocks
                )

                table_index += 1

        # --------------------------------------------------------
        # Re-index after all blocks have been collected
        # --------------------------------------------------------

        for index, block in enumerate(blocks):

            block.index = index

        return blocks

    # ============================================================
    # READ TABLE
    # ============================================================

    def read_table(
        self,
        table,
        table_index: int = -1,
        parent_block_index: int = -1,
    ) -> list[ResumeBlock]:

        blocks = []

        for row_index, row in enumerate(
            table.rows
        ):

            for cell_index, cell in enumerate(
                row.cells
            ):

                cell_blocks = self.read_cell(
                    cell,
                    table_index=table_index,
                    row_index=row_index,
                    cell_index=cell_index,
                    parent_block_index=parent_block_index,
                )

                blocks.extend(
                    cell_blocks
                )

        return blocks

    # ============================================================
    # READ CELL
    # ============================================================

    def read_cell(
        self,
        cell,
        table_index: int = -1,
        row_index: int = -1,
        cell_index: int = -1,
        parent_block_index: int = -1,
    ) -> list[ResumeBlock]:

        blocks = []

        for block in self.iter_block_items(
            cell
        ):

            # ----------------------------------------------------
            # PARAGRAPH
            # ----------------------------------------------------

            if isinstance(
                block,
                Paragraph,
            ):

                text = block.text.strip()

                if not text:
                    continue

                blocks.append(
                    ResumeBlock(
                        index=-1,
                        text=text,
                        block_type="table_cell_paragraph",
                        table_index=table_index,
                        row_index=row_index,
                        cell_index=cell_index,
                        parent_block_index=parent_block_index,
                    )
                )

            # ----------------------------------------------------
            # NESTED TABLE
            # ----------------------------------------------------

            elif isinstance(
                block,
                Table,
            ):

                blocks.extend(
                    self.read_table(
                        block,
                        table_index=table_index,
                        parent_block_index=parent_block_index,
                    )
                )

        return blocks

    # ============================================================
    # ITERATE DOCUMENT IN ORDER
    # ============================================================

    def iter_block_items(
        self,
        parent,
    ) -> Iterator:

        if isinstance(
            parent,
            DocxDocument,
        ):

            parent_element = (
                parent.element.body
            )

        elif isinstance(
            parent,
            _Cell,
        ):

            parent_element = parent._tc

        else:

            raise TypeError(
                f"Unsupported parent: {type(parent)}"
            )

        for child in parent_element.iterchildren():

            if isinstance(
                child,
                CT_P,
            ):

                yield Paragraph(
                    child,
                    parent,
                )

            elif isinstance(
                child,
                CT_Tbl,
            ):

                yield Table(
                    child,
                    parent,
                )