"""
GetHired

Production Resume Reader

Reads DOCX resumes while preserving the
original document order.

Supports

✓ Paragraphs
✓ Tables
✓ Nested Tables

Future

□ Headers
□ Footers
□ Text Boxes
□ Shapes
"""

from pathlib import Path

from docx import Document
from docx.document import Document as DocxDocument
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl


class ResumeReader:

    def __init__(self):

        pass

    # =====================================================
    # PUBLIC
    # =====================================================

    def read(self, file_path):

        document = Document(Path(file_path))

        lines = []

        for block in self.iter_block_items(document):

            # --------------------------
            # Paragraph
            # --------------------------

            if isinstance(block, Paragraph):

                text = block.text.strip()

                if text:
                    lines.append(text)

            # --------------------------
            # Table
            # --------------------------

            elif isinstance(block, Table):

                lines.extend(
                    self.read_table(block)
                )

        return lines

    # =====================================================
    # READ TABLE
    # =====================================================

    def read_table(self, table):

        lines = []

        for row in table.rows:

            for cell in row.cells:

                lines.extend(
                    self.read_cell(cell)
                )

        return lines

    # =====================================================
    # READ CELL
    # =====================================================

    def read_cell(self, cell):

        lines = []

        for block in self.iter_block_items(cell):

            if isinstance(block, Paragraph):

                text = block.text.strip()

                if text:

                    lines.append(text)

            elif isinstance(block, Table):

                lines.extend(
                    self.read_table(block)
                )

        return lines

    # =====================================================
    # ITERATE DOCUMENT IN ORDER
    # =====================================================

    def iter_block_items(self, parent):
        """
        Yield Paragraph and Table objects
        in the order they appear inside Word.
        """

        if isinstance(parent, DocxDocument):

            parent_element = parent.element.body

        elif isinstance(parent, _Cell):

            parent_element = parent._tc

        else:

            raise TypeError(
                f"Unsupported parent: {type(parent)}"
            )

        for child in parent_element.iterchildren():

            if isinstance(child, CT_P):

                yield Paragraph(child, parent)

            elif isinstance(child, CT_Tbl):

                yield Table(child, parent)