from GPSToolsService.models.gpx.gpx_xml_enumerator import GpxXmlEnumerator
import GPSToolsService.models.gpx.gpx_xml_constants as gpx_constants
from GPSToolsService.models.track import TrackEnumerator, TrackPoint, ReadonlyTrackPoint, Position
from logging import getLogger
import xml.etree.ElementTree as ET
from typing import TypeVar
import datetime as dt


class GpxTrackEnumerator(TrackEnumerator):
    def __init__(self, xml_enumerator: GpxXmlEnumerator):
        self._logger = getLogger(__name__)
        self._cached_point = TrackPoint()
        self._display_point: TrackPoint|None = None
        self._xml_enumerator = xml_enumerator


    def move_next(self) -> bool:
        self._display_point = None

        if ( not self._xml_enumerator.move_next() ):
            return False

        element = self._xml_enumerator.current()

        if ( element is not None ):
            self.update_point(element)
            self._display_point = self._cached_point

        return self._display_point is not None


    def current_point(self) -> ReadonlyTrackPoint|None:
        return self._display_point
        

    def update_point(self, point_node: ET.Element) -> None:
        self._cached_point.position = self._get_position(point_node)
        self._cached_point.datetime = self._get_datetime(point_node)
        self._cached_point.elevation = self._get_value(point_node, gpx_constants.GPX_ELEVATION_XPATH, float)

        extensions_node = point_node.find(gpx_constants.GPX_EXTENSIONS_XPATH, gpx_constants.GPX_NAMESPACES)
        
        self._cached_point.cadence = self._get_value(extensions_node, gpx_constants.GPX_CADENCE_XPATH, int)
        self._cached_point.heart_rate = self._get_value(extensions_node, gpx_constants.GPX_HEART_RATE_XPATH, int)
        self._cached_point.power = self._get_value(extensions_node, gpx_constants.GPX_POWER_XPATH, int)
        self._cached_point.temperature = self._get_value(extensions_node, gpx_constants.GPX_TEMPERATURE_XPATH, float)
        self._cached_point.speed = self._get_value(extensions_node, gpx_constants.GPX_SPEED_XPATH, float)


    def reset(self) -> None:
        self._xml_enumerator.reset()
        new_point = self._xml_enumerator.current()
    
        if ( new_point is not None ):
            self.update_point(new_point)
            self._display_point = self._cached_point
        else:
            self._display_point = None


    def _get_position(self, point: ET.Element) -> Position|None:
        latitude_text = point.get('lat')
        longitude_text = point.get('lon')
                
        if latitude_text is None or longitude_text is None:
            return None
        
        try:
            latitude = float(latitude_text)
            longitude = float(longitude_text)
            return Position(latitude=latitude, longitude=longitude)
        except Exception as e:
            self._logger.error("Error parsing position: %s. Latitude: %s, Longitude: %s", e, latitude_text, longitude_text)
            return None


    def _get_datetime(self, point: ET.Element) -> dt.datetime|None:
        time_elem = point.find(gpx_constants.GPX_TIME_XPATH, gpx_constants.GPX_NAMESPACES)
        
        if time_elem is None or time_elem.text is None:
            return None

        try:
            return dt.datetime.fromisoformat(time_elem.text)
        except Exception as e:
            self._logger.error("Error parsing datetime: %s. Value: %s", e, time_elem.text)
            return None
    
    
    T = TypeVar('T', float, int)
    def _get_value(self, node: ET.Element|None, xpath: str, value_type: type[T]) -> T|None:
        if node is None:
            return None

        target_elem = node.find(xpath, gpx_constants.GPX_NAMESPACES)
        if target_elem is None or target_elem.text is None:
            return None

        try:
            return value_type(target_elem.text)
        except Exception as e:
            self._logger.error("Error parsing %s value: %s. Value: %s; XPath: %s", value_type.__name__, e, target_elem.text, xpath)
            return None