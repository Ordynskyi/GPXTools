from typing import Final

GPX_NAMESPACES: Final[dict[str, str]] = {
    "default": "http://www.topografix.com/GPX/1/1",
    "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
}

GPX_TRACK_POINT_XPATH: Final[str] = './/default:trkpt'
GPX_EXTENSIONS_XPATH: Final[str] = 'default:extensions/gpxtpx:TrackPointExtension'
GPX_ELEVATION_XPATH: Final[str] = 'default:ele'
GPX_CADENCE_XPATH: Final[str] = 'gpxtpx:cad'
GPX_HEART_RATE_XPATH: Final[str] = 'gpxtpx:hr'
GPX_POWER_XPATH: Final[str] = 'gpxtpx:power'
GPX_TEMPERATURE_XPATH: Final[str] = 'gpxtpx:atemp'
GPX_SPEED_XPATH: Final[str] = 'gpxtpx:speed'
GPX_TIME_XPATH: Final[str] = 'default:time'