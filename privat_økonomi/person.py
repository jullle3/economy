from dataclasses import dataclass


@dataclass
class Person:
    """Indeholder indkomst samt fradrag for en person"""
    yearly_income: int
