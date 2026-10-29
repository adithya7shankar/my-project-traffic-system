import pytest
from utils import extract_speed

@pytest.mark.parametrize('value,expected',[
    ('{"speed":55}',55),
    ("{'speed':'55mph'}",55),
    ('speed=60mph,size=sedan',60),
    ({'speed':'42 mph'},42),
    ('not a speed',0),
])
def test_supported_speed_formats(value,expected):
    assert extract_speed(value)==expected
