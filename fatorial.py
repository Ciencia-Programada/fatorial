import pytest


def fatorial(numero):
    if numero in (0, 1):
        return 1
    else:
        return numero * fatorial(numero - 1)


def test_fatorial_quatro():
    assert fatorial(4) == 24


def test_fatorial_tres():
    assert fatorial(3) == 6


def test_fatorial_dois():
    assert fatorial(2) == 2


def test_fatorial_zero():
    assert fatorial(0) == 1


def test_fatorial_um():
    assert fatorial(1) == 1


if __name__ == '__main__':
    pytest.main([__file__, '--verbose'])
