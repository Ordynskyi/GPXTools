import pytest
from GPSToolsService.models.gpx.gpx_xml_enumerator import GpxXmlEnumerator
from GPSToolsService.models.gpx.gpx_xml_bytes_enumerator import GpxXmlBytesEnumerator
from GPSToolsService.models.gpx.gpx_track_enumerator import GpxTrackEnumerator
import xml.etree.ElementTree as ET
import datetime as dt


class GpxXmlTestEnumerator(GpxXmlEnumerator):
    def __init__(self):
        self.current_element: ET.Element|None = None
        self.move_next_returns: bool = False        
        self.move_next_calls_count: int = 0
        self.reset_calls_count: int = 0

    def move_next(self) -> bool:
        self.move_next_calls_count += 1
        return self.move_next_returns
    
    def current(self) -> ET.Element|None:
        return self.current_element
    
    def reset(self) -> None:
        self.reset_calls_count += 1


@pytest.fixture
def test_enumerator() -> GpxXmlTestEnumerator:
    return GpxXmlTestEnumerator()

@pytest.fixture
def gpx_bytes() -> bytes:
    return b"""<?xml version="1.0" encoding="UTF-8"?>
        <gpx creator="StravaGPX" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
            <metadata>
                <time>2026-04-12T17:06:13Z</time>
            </metadata>
            <trk>
                <name>Morning Ride</name>
                <type>cycling</type>
                <trkseg>
                    <trkpt lat="49.1625420" lon="-123.1351300">
                        <ele>4.4</ele>
                        <time>2026-04-12T17:06:13Z</time>
                        <extensions>
                            <gpxtpx:TrackPointExtension>
                                <gpxtpx:atemp>22</gpxtpx:atemp>
                                <gpxtpx:hr>92</gpxtpx:hr>
                                <gpxtpx:cad>5</gpxtpx:cad>
                                <gpxtpx:power>300</gpxtpx:power>
                                <gpxtpx:speed>40</gpxtpx:speed>
                            </gpxtpx:TrackPointExtension>
                        </extensions>
                    </trkpt>
                    <trkpt lat="49.1626520"> 
                        <ele>6.4</ele>
                        <time>Invalid Time</time>
                        <extensions>
                        <gpxtpx:TrackPointExtension>
                            <gpxtpx:atemp>22</gpxtpx:atemp>
                            <gpxtpx:hr>Invalid Val</gpxtpx:hr>
                            <gpxtpx:cad>5</gpxtpx:cad>
                        </gpxtpx:TrackPointExtension>
                        </extensions>
                    </trkpt>                    
                </trkseg>
            </trk>
        </gpx>"""

@pytest.fixture
def gpx_track_elements(gpx_bytes: bytes) -> list[ET.Element]:
    example_gpx = ET.fromstring(gpx_bytes)
    return example_gpx.findall(".//{http://www.topografix.com/GPX/1/1}trkpt")

@pytest.fixture
def gpx_track_elements_no_extensions() -> list[ET.Element]:
    example_gpx = ET.fromstring(b"""<?xml version="1.0" encoding="UTF-8"?>
        <gpx creator="StravaGPX" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
            <metadata>
                <time>2026-04-12T17:06:13Z</time>
            </metadata>
            <trk>
                <name>Morning Ride</name>
                <type>cycling</type>
                <trkseg>
                    <trkpt lat="49.1625420" lon="-123.1351300">
                        <ele>4.4</ele>
                        <time>2026-04-12T17:06:13Z</time>
                    </trkpt>
                </trkseg>
            </trk>
        </gpx>""")
    return example_gpx.findall(".//{http://www.topografix.com/GPX/1/1}trkpt")

def test_gpx_track_enumerator_initializes_with_test_enumerator(test_enumerator: GpxXmlTestEnumerator):
    GpxTrackEnumerator(test_enumerator)
    assert test_enumerator.move_next_calls_count == 0
    assert test_enumerator.reset_calls_count == 0


def test_gpx_track_enumerator_returns_current_point(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    current_point = track_enumerator.current_point()
    assert current_point is None

    # current_point is not none, but move_next returns false => current_point should be None
    test_enumerator.current_element = gpx_track_elements[0]
    test_enumerator.move_next_returns = False
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is None

    # current point is None, but move_next returns true => current_point should be None
    test_enumerator.current_element = None
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is None

    # current_point is not none, move_next returns true => current_point should be updated    
    test_enumerator.current_element = gpx_track_elements[0]
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is not None
    assert current_point.position.latitude == 49.1625420
    assert current_point.position.longitude == -123.1351300
    assert current_point.elevation == 4.4
    assert current_point.datetime == dt.datetime(2026, 4, 12, 17, 6, 13, tzinfo=dt.timezone.utc)
    assert current_point.cadence == 5
    assert current_point.heart_rate == 92
    assert current_point.temperature == 22
    assert current_point.power == 300
    assert current_point.speed == 40
    
    # current point is correct after reset is called: expected the track enumerator
    # to adapt the xml enumerator's current element. 
    track_enumerator.reset()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.elevation == 4.4

    # current_point is still correct after move_next is called
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.elevation == 4.4

    # current_point is None after move_next returns false
    test_enumerator.current_element = None
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is None


def test_gpx_track_enumerator_calls_move_next(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    
    # move_next returns false, current_element is None => moved should be False
    test_enumerator.move_next_returns = False
    test_enumerator.current_element = None
    moved = track_enumerator.move_next()
    assert moved is False
    assert test_enumerator.move_next_calls_count == 1

    # move_next returns false, current_element is not None => moved should be False
    test_enumerator.move_next_returns = False
    test_enumerator.current_element = gpx_track_elements[0]
    moved = track_enumerator.move_next()
    assert moved is False
    assert test_enumerator.move_next_calls_count == 2

    # move_next returns true, current_element is None => moved should be False
    test_enumerator.move_next_returns = True
    test_enumerator.current_element = None
    moved = track_enumerator.move_next()
    assert moved is False
    assert test_enumerator.move_next_calls_count == 3

    # move_next returns true, current_element is not None => moved should be True
    test_enumerator.move_next_returns = True
    test_enumerator.current_element = gpx_track_elements[0]
    moved = track_enumerator.move_next()
    assert moved is True
    assert test_enumerator.move_next_calls_count == 4


def test_gpx_track_enumerator_calls_reset(test_enumerator: GpxXmlTestEnumerator):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    track_enumerator.reset()
    assert test_enumerator.reset_calls_count == 1
    track_enumerator.reset()
    assert test_enumerator.reset_calls_count == 2


def test_gpx_track_enumerator_with_no_extensions(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements_no_extensions: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    test_enumerator.current_element = gpx_track_elements_no_extensions[0]
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.cadence is None
    assert current_point.heart_rate is None
    assert current_point.temperature is None
    assert current_point.power is None
    assert current_point.speed is None

def test_gpx_track_enumerator_point_position_dimention_invalid_val(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    target_element.set('lat', '')
    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is None

def test_gpx_track_enumerator_point_position_dimention_missing(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    target_element.attrib.pop('lat')
    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is None

def test_gpx_track_enumerator_time_invalid_format(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    time_element = target_element.find('{http://www.topografix.com/GPX/1/1}time')
    assert time_element is not None
    time_element.text = 'invalid time format'
    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.datetime is None

def test_gpx_track_enumerator_time_not_exists(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    time_element = target_element.find('{http://www.topografix.com/GPX/1/1}time')
    if time_element is not None:
        target_element.remove(time_element)
    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.datetime is None

def test_gpx_track_enumerator_point_with_extensions_missing_values(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    extensions_node = target_element.find('{http://www.topografix.com/GPX/1/1}extensions')
    assert extensions_node is not None
    tpx_node = extensions_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
    assert tpx_node is not None
    atemp_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}atemp')
    hr_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr')
    cad_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad')
    power_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}power')
    speed_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}speed')

    if atemp_node is not None:
        tpx_node.remove(atemp_node)
    
    if hr_node is not None:
        tpx_node.remove(hr_node)

    if cad_node is not None:
        tpx_node.remove(cad_node)

    if power_node is not None:
        tpx_node.remove(power_node)

    if speed_node is not None:
        tpx_node.remove(speed_node)

    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.cadence is None
    assert current_point.heart_rate is None
    assert current_point.temperature is None


def test_gpx_track_enumerator_point_with_extensions_invalid_values(test_enumerator: GpxXmlTestEnumerator, gpx_track_elements: list[ET.Element]):
    track_enumerator = GpxTrackEnumerator(test_enumerator)
    target_element = gpx_track_elements[0]
    extensions_node = target_element.find('{http://www.topografix.com/GPX/1/1}extensions')
    assert extensions_node is not None
    tpx_node = extensions_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
    assert tpx_node is not None
    atemp_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}atemp')
    hr_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr')
    cad_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad')
    power_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}power')
    speed_node = tpx_node.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}speed')

    if atemp_node is not None:
        atemp_node.text = 'invalid float'
    
    if hr_node is not None:
        hr_node.text = 'invalid int'

    if cad_node is not None:
        cad_node.text = 'invalid int'

    if power_node is not None:
        power_node.text = 'invalid int'

    if speed_node is not None:
        speed_node.text = 'invalid float'

    test_enumerator.current_element = target_element
    test_enumerator.move_next_returns = True
    track_enumerator.move_next()
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.cadence is None
    assert current_point.heart_rate is None
    assert current_point.temperature is None


def test_gpx_track_enumerator_integration(gpx_bytes: bytes):
    xml_enumerator = GpxXmlBytesEnumerator(gpx_bytes)
    track_enumerator = GpxTrackEnumerator(xml_enumerator)

    assert track_enumerator.current_point() is None
    assert track_enumerator.move_next() is True
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is not None
    assert current_point.position.latitude == 49.1625420
    assert current_point.position.longitude == -123.1351300
    assert current_point.elevation == 4.4
    assert current_point.datetime == dt.datetime(2026, 4, 12, 17, 6, 13, tzinfo=dt.timezone.utc)
    assert current_point.cadence == 5
    assert current_point.heart_rate == 92
    assert current_point.temperature == 22
    assert current_point.power == 300
    assert current_point.speed == 40

    # move_next should return true even if the time format is invalid, but the datetime of the current point should be None
    assert track_enumerator.move_next() is True
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is None
    assert current_point.elevation == 6.4
    assert current_point.datetime is None
    assert current_point.cadence == 5
    assert current_point.heart_rate is None
    assert current_point.temperature == 22
    assert current_point.power is None
    assert current_point.speed is None

    assert track_enumerator.move_next() is False
    assert track_enumerator.current_point() is None

    track_enumerator.reset()
    assert track_enumerator.current_point() is None
    assert track_enumerator.move_next() is True
    current_point = track_enumerator.current_point()
    assert current_point is not None
    assert current_point.position is not None
    assert current_point.position.latitude == 49.1625420
    assert current_point.position.longitude == -123.1351300