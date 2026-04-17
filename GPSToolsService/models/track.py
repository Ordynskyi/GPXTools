from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
import datetime as dt


@dataclass(slots=True)
class Position:
    latitude: float
    longitude: float


class ReadOnlyPosition(Protocol):
    @property
    def latitude(self) -> float: ...
    @property
    def longitude(self) -> float: ...


@dataclass(slots=True)
class TrackPoint:
    position: Position|None = None
    datetime: dt.datetime|None = None
    cadence: int|None = None
    heart_rate: int|None = None
    power: int|None = None
    elevation: float|None = None
    temperature: float|None = None
    speed: float|None = None


class ReadonlyTrackPoint(Protocol):
    @property
    def position(self) -> ReadOnlyPosition|None: ...
    @property
    def datetime(self) -> dt.datetime|None: ...
    @property
    def cadence(self) -> int|None: ...
    @property
    def heart_rate(self) -> int|None: ...
    @property
    def power(self) -> int|None: ...
    @property
    def elevation(self) -> float|None: ...
    @property
    def temperature(self) -> float|None: ...
    @property
    def speed(self) -> float|None: ...


class TrackEnumerator(ABC):
    @abstractmethod
    def current_point(self) -> ReadonlyTrackPoint|None: ...

    @abstractmethod
    def move_next(self) -> bool: ...

    @abstractmethod
    def reset(self) -> None: ...