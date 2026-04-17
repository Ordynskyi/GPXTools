import pytest
from GPSToolsService.models.gpx.gpx_xml_bytes_enumerator import GpxXmlBytesEnumerator
import xml.etree.ElementTree as ET

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
                            </gpxtpx:TrackPointExtension>
                        </extensions>
                    </trkpt>
                    <trkpt lat="49.1626520" lon="-123.1350710">
                        <ele>4.4</ele>
                        <time>2026-04-12T17:06:14Z</time>
                        <extensions>
                        <gpxtpx:TrackPointExtension>
                            <gpxtpx:atemp>22</gpxtpx:atemp>
                            <gpxtpx:hr>92</gpxtpx:hr>
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


def test_xml_bytes_enumerator_throws_on_invalid_xml():
    with pytest.raises(ValueError):
        GpxXmlBytesEnumerator(b"invalid xml")


def test_xml_bytes_enumerator_initializes_on_valid_xml(gpx_bytes: bytes):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)               
    assert enumerator.length == 2

def test_xml_bytes_enumerator_current_is_none_before_move_next(gpx_bytes: bytes):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)
    assert enumerator.current() is None

def test_xml_bytes_enumerator_moves_through_points(gpx_bytes: bytes):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)

    assert enumerator.move_next() is True
    assert enumerator.current() is not None

    assert enumerator.move_next() is True
    assert enumerator.current() is not None

    assert enumerator.move_next() is False
    assert enumerator.current() is None

def test_xml_bytes_enumerator_returns_valid_elements(gpx_bytes: bytes, gpx_track_elements: list[ET.Element]):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)
        
    enumerator.move_next()
    element = enumerator.current()
    assert element is not None
    assert gpx_track_elements[0] is not None
    assert ET.tostring(element) == ET.tostring(gpx_track_elements[0])

    enumerator.move_next()
    element = enumerator.current()
    assert element is not None 
    assert gpx_track_elements[1] is not None
    assert ET.tostring(element) == ET.tostring(gpx_track_elements[1])

    enumerator.move_next()
    assert enumerator.current() is None


def test_xml_bytes_enumerator_current_is_none_after_reset(gpx_bytes: bytes):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)
    enumerator.move_next()
    assert enumerator.current() is not None

    enumerator.reset()
    assert enumerator.current() is None


def test_xml_bytes_enumerator_element_correct_after_reset(gpx_bytes: bytes, gpx_track_elements: list[ET.Element]):
    enumerator = GpxXmlBytesEnumerator(gpx_bytes)
    enumerator.move_next()
    enumerator.move_next()
    enumerator.move_next()
    enumerator.reset()
    enumerator.move_next()
    element = enumerator.current()
    expected_element = gpx_track_elements[0]
    assert element is not None
    assert expected_element is not None
    assert ET.tostring(element) == ET.tostring(expected_element)