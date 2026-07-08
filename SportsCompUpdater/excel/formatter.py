from __future__ import annotations

from copy import copy

from openpyxl.cell.cell import Cell


def copy_cell_format(source: Cell, target: Cell) -> None:
    target.font = copy(source.font)
    target.fill = copy(source.fill)
    target.border = copy(source.border)
    target.alignment = copy(source.alignment)
    target.number_format = source.number_format
    target.protection = copy(source.protection)

