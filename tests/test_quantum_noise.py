from quantum.noise import bit_flip
from quantum.syndrome import detect
from quantum.recovery import recover


def test_syndrome_detection():

    tx = [0] * 20

    rx = tx.copy()
    rx[5] = 1

    syndrome = detect(tx, rx)

    assert syndrome.has_error()
    assert syndrome.weight() == 1


def test_recovery():

    tx = [0] * 20

    rx = tx.copy()
    rx[3] = 1
    rx[10] = 1

    corrected = recover(tx, rx)

    assert corrected == tx


def test_bit_flip_preserves_length():

    tx = [0] * 20

    rx = bit_flip(tx, p=0.25)

    assert len(rx) == 20