from GPSToolsService.models.gpx.gpx_xml_enumerator import GpxXmlEnumerator
import GPSToolsService.models.gpx.gpx_xml_constants as gpx_constants
import xml.etree.ElementTree as ET

class GpxXmlBytesEnumerator(GpxXmlEnumerator):
    def __init__(self, gpx_bytes: bytes):
        super().__init__()

        try:
            root = ET.fromstring(gpx_bytes)
        except ET.ParseError as e:
            raise ValueError(f"Invalid GPX XML bytes: {e}") from e

        self._points = root.findall(gpx_constants.GPX_TRACK_POINT_XPATH, gpx_constants.GPX_NAMESPACES)
        self._index = -1
        self.length = len(self._points)


    def move_next(self) -> bool:
        self._index += 1
        return self._index < self.length

    
    def current(self) -> ET.Element|None:
        if self._index < 0 or self._index >= self.length:
            return None

        return self._points[self._index]

    
    def reset(self) -> None:
        self._index = -1