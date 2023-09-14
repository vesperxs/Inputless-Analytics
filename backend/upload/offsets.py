from typing import List
from dataclasses import dataclass


@dataclass
class Offset:
    start: str
    end: str
    type: str


@dataclass
class Paragraph:
    case_id: str
    # text    : str
    extracted_text: List[str]
    # offsets : List[Offset]


Case = List[Paragraph]
