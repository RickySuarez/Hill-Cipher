"""A collection of functions for doing my project."""
import numpy as np
from random import randrange
from my_module.classes import Encryptor


def encryptor_generator():
    """
    Generates an Encryptor object for encryption and decryption.

    Returns:
        Encryptor: An Encryptor object.
    """
    
    # Set the gcd to an initial value of 0 in order to set up the while loop
    # n is the maximum value of the allowed Unicode characters
    gcd = 0
    n = 256
    
    # While loop that aids in the creation of the encryption matrix.
    # A matrix A is only invertible mod 256 if gcd(det(A), 256) = 1.
    # Therefore it is necessary to create another random matrix if the gcd is anything but 1.
    while gcd != 1:
        
        # Populating a numpy array with random values up to 256.
        matrix = np.array([[randrange(n), randrange(n)], [randrange(n), randrange(n)]])
        
        # Calculation of the determinant of the matrix.
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        # If the determinant is negative, readjust by adding n until it reaches a positive congruent value mod n.
        while det < 0:
            det += n
        
        # Ensure that the det value is congruent to the det(matrix) and also between 0 and n.
        det %= n
        
        # Calculate the gcd and Bezout coefficients used in the creation of the inverse matrix.
        gcd, x, y = extended_gcd(n, det)
    
    # Calculating the inverse of the matrix through use of the matrix inversion formula.
    inverse = np.array([[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]])
    
    # Ensure that the matrix only has a positive value when applying the mod operator.
    # This is necessary since Python allows for negative remainders which is not helpful
    # when applying the Hill Cipher.
    inverse = ((y * inverse) % n + n) % n
    
    # Return an Encryptor object which is found in classes.py.
    return Encryptor(matrix, inverse)


def extended_gcd(a, b):
    """
    Recursive implementation of the extended Euclidean algorithm.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        Tuple(int, int, int): GCD of the two integers and Bezout coefficients.
    """
    # if b is 0, then gcd(a,b) = a and the Bezout coeficcients are 1 and 0.
    if b == 0:
        return a, 1, 0
    else:
        # If b is not 0, then recurse on b and a % b as defined by the Euclidean Algorithm.
        gcd, x1, y1 = extended_gcd(b, a % b)
        
        # Calculate the Bezout coeficcients as defined by the Extended Euclidean Algorithm.
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y
