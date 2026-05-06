from dataclasses import dataclass
from typing import NamedTuple


class ChosenColor(NamedTuple):
    red: int
    green: int
    blue: int
    rgb: int


@dataclass(slots=True, frozen=True)
class ChosenFont:
    face_name: str
    point_size: float
    weight: int
    italic: bool
    underline: bool
    strike_out: bool
    color: ChosenColor
