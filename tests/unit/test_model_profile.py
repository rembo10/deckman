from deckman.model.profile import (
    LossySettings,
    LosslessSettings,
    Profile,
    Quality,
    Result,
    is_right_size
)


def test_lossless_calculate_size():
    ls1 = LosslessSettings("ls1", 44.1, 16, 2)
    ls2 = LosslessSettings("ls2", 192, 24, 2)
    ls3 = LosslessSettings("ls3", 192, 24, 1)
    assert ls1.calculate_size(300) == 52920000
    assert ls2.calculate_size(300) == 345600000
    assert ls3.calculate_size(300) == 172800000


def test_lossy_calculate_size():
    ls = LossySettings("ls", 320)
    assert ls.calculate_size(300) == 12000000


def test_is_right_size():
    min_size = 300
    max_size = 400
    for s, v in [(300, True), (400, True), (299, False), (401, False)]:
        assert is_right_size(min_size, max_size, s) is v


def test_profile_chooses_best_result_single_quality():
    # 300 seconds @ 320kbps == 12000000 bytes
    p = Profile("p", [Quality(LossySettings("q1", 320))], 0.1)
    r = [
            Result("1", 7000000),   # outside tolerance
            Result("2", 11000000),  # closest inside tolerance
            Result("3", 15000000)   # outside tolerance
        ]
    assert p.choose_best_result(r, 300) == r[1]
