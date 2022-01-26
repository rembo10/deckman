from deckman.model.profile import (
    LossySettings,
    LosslessSettings,
    Profile,
    Quality,
    Result,
    is_right_size
)


def test_lossless_calculate_size():
    ls1 = LosslessSettings(1, "ls1", 44100, 16, 2)
    ls2 = LosslessSettings(2, "ls2", 192000, 24, 2)
    ls3 = LosslessSettings(3, "ls3", 192000, 24, 1)
    assert ls1.calculate_size(300) == 52920000
    assert ls2.calculate_size(300) == 345600000
    assert ls3.calculate_size(300) == 172800000


def test_lossy_calculate_size():
    ls = LossySettings(1, "ls", 320)
    assert ls.calculate_size(300) == 12000000


def test_is_right_size():
    min_size = 300
    max_size = 400
    for s, v in [(300, True), (400, True), (299, False), (401, False)]:
        assert is_right_size(min_size, max_size, s) is v


def test_profile_chooses_best_result_single_quality():
    # 300 seconds @ 320kbps == 12000000 bytes
    profile = Profile(
        id=1,
        name="profile1",
        qualities=[
            Quality(
                id=1,
                settings=LossySettings(
                    id=1,
                    name="quality1",
                    bitrate=320
                )
            )
        ],
        tolerance=0.1
    )

    results = [
            Result("1", 7000000),   # outside tolerance
            Result("2", 11000000),  # closest inside tolerance
            Result("3", 15000000)   # outside tolerance
        ]
    assert profile.choose_best_result(results, 300) == results[1]
