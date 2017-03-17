# The MIT License (MIT)
#
# Copyright (c) 2014 Matthias Eisen (http://www.matthiaseisen.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    TableStyle,
    PageBreak,
    Paragraph
)
from reportlab.lib.colors import lightgrey, black
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet


def list_of_columns(entries,
    num_of_columns=5,
    num_of_rows=5
):
    numbers = range(1,len(entries));
    slice_length = len(numbers) // num_of_columns
    return [
        #sorted(
            random.sample(
                entries[i * slice_length: (i + 1) * slice_length],
                num_of_rows
            )
        #)
        #(
        #    random.sample(
        #        entries[i * num_of_rows: (i + 1) * num_of_rows],
        #        num_of_rows
        #    )
        #)
        for i in range(num_of_columns)
    ]


def list_of_rows(list_of_columns):
    return [list(row) for row in zip(*list_of_columns)]


def insert_free_spaces(numbers, coords=[(2, 2)]):
    return [
        [
            n if not (x, y) in coords else None
            for x, n in enumerate(numbers[y])
        ]
        for y in range(len(numbers))
    ]


def prepend_title_row(numbers):
    return [['B', 'I', 'N', 'G', 'O']] + numbers


def card_data(entries):
    return prepend_title_row(
        #insert_free_spaces(
            list_of_rows(
                list_of_columns(entries)
        #    )
        )
    )


def stylesheet():
    return {
        'bingo': TableStyle(
            [
                ('FONTSIZE', (0, 0), (-1, 0), 28),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 11),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                ('BOX', (0, 0), (-1, 0), 2.0, black),
                ('BOX', (0, 1), (-1, -1), 2.0, black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (2, 3), (2, 3), lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), lightgrey),
            ]
        ),
    }


def pages(entries, number_of_pages, stylesheet):
    pages = zip(
        [
            Table(
                card_data(entries),
                5 * [3.5 * cm],  # column widths
                6 * [3.5 * cm],  # row heights
                style=stylesheet['bingo']
            )
            for i in range(number_of_pages)
        ],
        [
            PageBreak()
        ] * number_of_pages
    )
    return [e for p in pages for e in p]


def build_pdf(filename, pages):
    doc = BaseDocTemplate(filename)
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )
    doc.build(pages)

styles = getSampleStyleSheet()
fname = "cell_entries"
with open(fname) as f:
    cell_entries = f.readlines()
for s in range(0,len(cell_entries)):
    cell_entries[s] = Paragraph(cell_entries[s].rstrip(), styles['Normal'])

#print(cell_entries)

build_pdf('1000_disaster_bingo_cards.pdf', pages(cell_entries, 1000, stylesheet()))
