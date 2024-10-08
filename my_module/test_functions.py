"""Test for my functions."""
from my_module.Encryptor import Encryptor
from random import randrange
import numpy as np

# Multiply the two randomly generated matrices and
# ensure that they are inverses mod 256
def test_valid_inverse():
    size = randrange(5) + 2
    encryptor = Encryptor(size)
    product = np.matmul(encryptor.matrix, encryptor.inverse) % 256
    identity = np.identity(encryptor.matrix.shape[0])
    assert np.array_equal(product, identity)

# Generate 256 random strings of lengths 0 - 255 and ensure
# the decryptions match the original strings.
def test_random():
    for x in range(256):
        original = ''
        for y in range(x):
            original += chr(randrange(256))
        for y in range(5):
            encryptor = Encryptor(y+2)
            encrypted = encryptor.encrypt(original)
            decrypted = encryptor.decrypt(encrypted)
            assert decrypted == original


#Ensure that the Bezout coefficients were correctly calculated
def test_extended_gcd():
    gcd, x, y = Encryptor.extended_gcd(256, 203)
    assert gcd == 1
    assert x == 23
    assert y == -29