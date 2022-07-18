import pytest
from light_lock import misc


@pytest.mark.parametrize(
    "value, expected",
    [
        ("20", 20),
        ("20s", 20),
        ("20m", 20 * 60),
        ("20h", 20 * 60 * 60),
        ("20d", 20 * 24 * 60 * 60),
        ("20w", 20 * 7 * 24 * 60 * 60),
    ],
)
def test_to_timedelta_ext(value: str, expected: int):
    assert misc.to_timedelta_ext(value).total_seconds() == expected
