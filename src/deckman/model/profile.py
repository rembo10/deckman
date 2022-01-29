from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class SettingsLossless:
    """Lossless quality representation"""
    id: int
    name: str
    sample_rate_hz: int
    bit_depth: int
    channels: int

    def calculate_size(self, seconds: int) -> int:
        """Returns number of bytes"""
        return round(
            self.sample_rate_hz
            * self.bit_depth
            * self.channels
            * seconds
            / 8)

    def __eq__(self, other):
        return (
            self.sample_rate_hz == other.sample_rate_hz and
            self.bit_depth == other.bit_depth and
            self.channels == other.channels
        )


@dataclass
class SettingsLossy:
    """Lossy quality representation"""
    id: int
    name: str
    bitrate: int

    def calculate_size(self, seconds: int) -> int:
        """Returns number of bytes"""
        return round(self.bitrate * 1000 * seconds / 8)

    def __eq__(self, other):
        return self.bitrate == other.bitrate


Settings = Union[SettingsLossless, SettingsLossy]


@dataclass
class TargetSize:
    target: int
    min: int
    max: int


@dataclass(frozen=True)
class Quality:

    id: int
    profile_id: int
    position: int
    settings_lossless_id: Settings
    settings_lossy_id: Settings
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


@dataclass(frozen=True)
class Result:
    name: str
    size: int


@dataclass(frozen=True)
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
    id: int
    name: str
    position: int
    enabled: bool
    #qualities: List[Quality]
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


class ProfileRepo(ABC):

    @abstractmethod
    def list(self) -> List[Profile]:
        """Return all the profiles"""

    @abstractmethod
    def create(self, name: str) -> Profile:
        """Create a new profile from a name"""

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete a profile by id"""

    @abstractmethod
    def update(self, id: int, **kwargs) -> None:
        """Update a profile (name, tolerance, dual_formats)"""

    @abstractmethod
    def bulk_update(self, profiles: List[Profile]) -> None:
        """Used for updating the positions"""


class QualityRepo(ABC):

    @abstractmethod
    def list(self) -> List[Quality]:
        """
        List of qualities. The settings attribute should
        either be SettingsLossy or SettingsLossless
        """

    @abstractmethod
    def create(
        self,
        profile_id: int,
        settings_id: int,
        finish: bool = False
    ) -> Quality:
        """
        Create a new Quality from a profile_id, a settings id
        and optionally whether to finish on this quality
        """

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete a quality by id"""

    @abstractmethod
    def update(self, id: int, **kwargs) -> None:
        """Used to update a quality"""

    @abstractmethod
    def bulk_update(self, qualities: List[Quality]) -> None:
        """Used for updating the positions"""


class SettingsLosslessRepo(ABC):
    @abstractmethod
    def list(self) -> List[SettingsLossless]:
        """List lossless settings"""

    @abstractmethod
    def create(
        self,
        sample_rate_hz: int,
        bit_depth: int,
        channels: int
    ) -> SettingsLossless:
        """Create a new lossless setting from sample_rate_hz,
        bit_depth and channels"""

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete lossless setting by id"""

    @abstractmethod
    def update(self, id: int, **kwargs) -> None:
        """Change property or properties in lossless seeing
        by id.
        """


class SettingsLossyRepo(ABC):
    @abstractmethod
    def list(self) -> List[SettingsLossy]:
        """List lossy settings"""

    @abstractmethod
    def create(self, bitrate: int) -> SettingsLossy:
        """Create new lossy settings from bitrate"""

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete lossy settings by id"""

    @abstractmethod
    def update(self, id: int, **kwargs) -> None:
        """Update name or bitrate of lossy settings"""
