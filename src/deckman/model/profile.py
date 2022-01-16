from dataclasses import dataclass
from typing import List


class _QualityBase:
    pass


@dataclass
class LosslessQuality(_QualityBase):
    """Lossless quality representation"""
    sample_rate_khz: float
    bit_depth: int
    channels: int


@dataclass
class LossyQuality(_QualityBase):
    """Lossy quality representation"""
    bitrate: int


@dataclass
class Quality:
    quality: _QualityBase
    finish: bool


@dataclass
class Profile:
    """A way to specify the quality of a track to look for.
    Whether to accept a lower quality temporarily, which
    qualities to mark as `done`, and whether or not to look
    for both lossless and lossy.
    """
    name: str
    tolerance: float
    qualities: List[Quality]
    dual_formats: bool = False


qualities = {
    "cd lossless": LosslessQuality(44.1, 16, 2),
    "hi-res lossless": LosslessQuality(192, 24, 2),
    "320cbr": LossyQuality(320),
    "256cbr": LossyQuality(256),
    "192cbr": LossyQuality(192),
    "v0": LossyQuality(245),
    "v1": LossyQuality(225),
    "v2": LossyQuality(190),
    "v3": LossyQuality(175)
}

initial_profiles = [
    Profile("CD Lossless", 0.2, [
        Quality(qualities["cd lossless"], True)
    ]),
    Profile("Hi-Res Lossless", 0.2, [
        Quality(qualities["hi-res lossless"], True)
    ]),
    Profile("Best Available (Hi-Res)", 0.2, [
        Quality(qualities["hi-res lossless"], True),
        Quality(qualities["cd lossless"], False),
        Quality(qualities["320cbr"], False),
        Quality(qualities["v0"], False),
        Quality(qualities["256cbr"], False),
    ]),
    Profile("Best Available", 0.2, [
        Quality(qualities["cd lossless"], True),
        Quality(qualities["320cbr"], False),
        Quality(qualities["v0"], False),
        Quality(qualities["256cbr"], False),
        Quality(qualities["v1"], False)
    ]),
    Profile("FLAC or MP3", 0.2, [
        Quality(qualities["cd lossless"], True),
        Quality(qualities["320cbr"], True),
        Quality(qualities["v0"], True),
    ]),
    Profile("MP3", 0.2, [
        Quality(qualities["v0"], True),
        Quality(qualities["320cbr"], True),
        Quality(qualities["v1"], True)
    ])
]
