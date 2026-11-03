import pytest
from protocol import ProtocolError, encode_fire, decode_fire

def test_fire_round_trip():
    paket = encode_fire(3, 4)
    assert paket == b"\x01\x01\x03\x04"
    assert decode_fire(paket) == (3, 4)

def test_fire_truncated():
    with pytest.raises(ProtocolError):
        decode_fire(b"\x01\x01\x03")

def test_fire_unknown_type():
    with pytest.raises(ProtocolError):
        decode_fire(b"\x01\x09\x03\x04")

def test_fire_bad_version():
    with pytest.raises(ProtocolError):
        decode_fire(b"\x09\x01\x03\x04")

def test_fire_too_long():
    with pytest.raises(ProtocolError):
        decode_fire(b"\x01\x01\x03\x04\x04")

def test_fire_coordinate_out_of_range():
    with pytest.raises(ProtocolError):
        encode_fire(300,1)
