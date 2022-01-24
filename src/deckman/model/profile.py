from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class LosslessSettings:
    """Lossless quality representation"""
    name: str
    sample_rate_khz: float
    bit_depth: int
    channels: int

    def calculate_size(self, seconds: int) -> int:
        """Returns number of bytes"""
        return round(
            self.sample_rate_khz * 1000
            * self.bit_depth
            * self.channels
            * seconds
            / 8)

    def __eq__(self, other):
        return (
            self.sample_rate_khz == other.sample_rate_khz and
            self.bit_depth == other.bit_depth and
            self.channels == other.channels
        )


@dataclass
class LossySettings:
    """Lossy quality representation"""
    name: str
    bitrate: int

    def calculate_size(self, seconds: int) -> int:
        """Returns number of bytes"""
        return round(self.bitrate * 1000 * seconds / 8)

    def __eq__(self, other):
        return self.bitrate == other.bitrate


Settings = Union[LosslessSettings, LossySettings]


@dataclass
class TargetSize:
    target: int
    min: int
    max: int


@dataclass
class Quality:

    settings: Settings
    finish: bool = False

    @property
    def name(self) -> str:
        return self.settings.name

    def _calculate_size(self, seconds: int) -> int:
        return self.settings.calculate_size(seconds)

    def calculate_target_size(
        self,
        seconds: int,
        tolerance: float
    ) -> TargetSize:
        target_size = self._calculate_size(seconds)
        return TargetSize(
            target_size,
            round((1 - tolerance) * target_size),
            round((1 + tolerance) * target_size)
        )


def is_right_size(min_size: int, max_size: int, size: int) -> bool:
    return min_size <= size <= max_size


@dataclass
class Result:
    name: str
    size: int


@dataclass
class Profile:
    """A way to specify the quality of a track to look for.
    Whether to accept a lower quality temporarily, which
    qualities to mark as `done`, and whether or not to look
    for both lossless and lossy.

    Profiles will also be attached to trackable entities,
    e.g. artists, labels etc., to be able to override
    the default and set a profile for any incoming
    tracks / albums.
    """
    name: str
    qualities: List[Quality]
    tolerance: float = 0.2
    dual_formats: Optional[bool] = False

    def choose_best_result(
        self,
        results: List[Result],
        seconds: int
    ) -> Optional[Result]:
        for quality in self.qualities:
            target_size = quality.calculate_target_size(
                seconds, self.tolerance
            )
            sorted_results = sorted(
                results,
                key=lambda result: target_size.target - result.size
            )
            for result in sorted_results:
                if is_right_size(
                    target_size.min,
                    target_size.max,
                    result.size
                ):
                    return result

        return None
