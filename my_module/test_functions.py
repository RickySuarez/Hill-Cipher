"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""
from functions import encryptor_generator, extended_gcd
from classes import Encryptor
from random import randrange
import numpy as np

# Multiply the two randomly generated matrices and
# ensure that they are inverses mod 256
def test_valid_inverse():
    encryptor = encryptor_generator()
    product = np.matmul(encryptor.matrix, encryptor.inverse) % 256
    identity = np.identity(encryptor.matrix.shape[0])
    assert np.array_equal(product, identity)

# Manually create an Encryptor object and calculate the
# encryption mapping. This was verified by hand.
def test_encrypt():
    matrix = np.array([[200, 5], [1, 10]])
    inverse = np.array([[222, 145], [29, 88]])
    encryptor = Encryptor(matrix, inverse)
    str1 = chr(1) + chr(57) + chr(58)
    str2 = chr(124) + chr(164)
    str3 = chr(88) + chr(175)
    str4 = chr(35) + chr(173)
    str5 = chr(44) + chr(170)
    str6 = chr(32) + chr(100)
    encrypted = encryptor.encrypt('Hello World')
    assert encrypted == str1 + str2 + str3 + str4 + str5 + str6        
        
    
# Manually create an Encryptor object and calculate the
# decryption mapping. This was verified by hand.
def test_decrypt():
    matrix = np.array([[200, 5], [1, 10]])
    inverse = np.array([[222, 145], [29, 88]])
    encryptor = Encryptor(matrix, inverse)
    str1 = chr(1) + chr(57) + chr(58)
    str2 = chr(124) + chr(164)
    str3 = chr(88) + chr(175)
    str4 = chr(35) + chr(173)
    str5 = chr(44) + chr(170)
    str6 = chr(32) + chr(100)
    decrypted = encryptor.decrypt(str1 + str2 + str3 + str4 + str5 + str6)
    assert decrypted == 'Hello World'

# Generate 256 random strings of lengths 0 - 255 and ensure
# the decryptions match the original strings.
def test_random():
    for x in range(256):
        original = ''
        encryptor = encryptor_generator()
        for y in range(x):
            original += chr(randrange(256))
        encrypted = encryptor.encrypt(original)
        decrypted = encryptor.decrypt(encrypted)
        assert decrypted == original

# Test that the empty string is mapped to the correct encryption
# and is decrypted back to the empty string.
def test_empty():
    matrix = np.array([[200, 5], [1, 10]])
    inverse = np.array([[222, 145], [29, 88]])
    encryptor = Encryptor(matrix, inverse)
    encrypted = encryptor.encrypt('')
    decrypted = encryptor.decrypt(encrypted)
    assert decrypted == ''

#Ensure that the Bezout coefficients were correctly calculated
def test_extended_gcd():
    gcd, x, y = extended_gcd(256, 203)
    assert gcd == 1
    assert x == 23
    assert y == -29