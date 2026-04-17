from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET

class GpxXmlEnumerator(ABC):
    @abstractmethod
    def move_next(self) -> bool: ...

    @abstractmethod
    def current(self) -> ET.Element|None: ...

    @abstractmethod
    def reset(self) -> None: ...