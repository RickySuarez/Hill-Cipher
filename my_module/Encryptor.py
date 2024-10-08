"""Classes used throughout project"""
import numpy as np
from my_module.matrix_operations import determinant, adjoint
from random import randrange

class Encryptor:
    """
    Encryptor class for encrypting and decrypting strings using a Hill Cipher.

    Attributes:
        matrix (numpy.ndarray): The encryption matrix.
        inverse (numpy.ndarray): The inverse matrix used for decryption.

    Raises:
        Exception: If the given matrices are not inverses mod 256.

    Methods:
        __init__(matrix, inverse): Initializes the Encryptor with encryption and decryption matrices.
        encrypt(str_to_encrypt): Encrypts a string using the encryption matrix.
        decrypt(str_to_decrypt): Decrypts a string using the decryption matrix.
    """
    
    def __init__(self, size):
        if size < 1:
            raise Exception('Invalid matrix size. The size must be positive.')
        self.matrix, self.inverse = Encryptor.matrix_generator(size)
        
   
    def encrypt(self, str_to_encrypt):
        """
        Encrypts a string using the encryption matrix.

        Args:
            str_to_encrypt (str_to_encrypt): The string to be encrypted.

        Returns:
            str: The encrypted string.
        """
        
        # Stores the result.
        result = ''
        
        # Keeps count of how many characters are used to pad the string. 
        count = 0
        
        # Padding the string to match the matrix dimensions
        while len(str_to_encrypt) % self.matrix.shape[1] != 0:
            str_to_encrypt += chr(0)
            count += 1
        
        # While loop that iterates through every character of the string and fills up
        # the column matrix as needed to ensure the two matrices can be multiplied.
        index = 0
        while index < len(str_to_encrypt):
            
            # Store the unicode value of the characters in the matrix.
            # The size of this matrix is determined by the size of the columns in the matrix instance attribute. 
            ls = []
            for x in range(self.matrix.shape[1]):
                ls.append([ord(str_to_encrypt[index])])
                index += 1
                
            # Create a numpy array that is populated by the unicode values.
            arr = np.array(ls)
            
            # Multiply the matrices and mod out the entries by 256. 
            # This will give the characters a new mapping.
            encoded = np.matmul(self.matrix, arr) % 256
            
            # Each value in the encoded array is the unicode value for the encrypted string.
            # Concatenate these characters with result.
            for x in encoded:
                result += chr(int(x[0]))
                
        # When the loop is over return result prepended by the count used to determine how
        # many characters where appended at the beginning of the function.
        return chr(count) + result
    
    def decrypt(self, str_to_decrypt):
        """
        Decrypts a string using the decryption matrix.

        Args:
            str_to_decrypt (str_to_decrypt): The string to be decrypted.

        Returns:
            str: The decrypted string.
        """
        
        # Used to store the result.
        result = ''
        
        # Number of characters to remove as determined by the encoding process.
        count = ord(str_to_decrypt[0])
        
        # Begin at index 1 since the the value at index 0 was used for the count.
        index = 1
        while index < len(str_to_decrypt):
            
            # List used to store the unicode values in a column matrix.
            # The size of the column matrix is determined by the size of the columns in the inverse.
            ls = []
            for x in range(self.inverse.shape[1]):
                ls.append([ord(str_to_decrypt[index])])
                index += 1
            
            # Create numpy array with the values from ls
            arr = np.array(ls)
            
            # Multiply arr by the inverse matrix on the left and mod out by 256
            # to get the original unicode values.
            decoded = np.matmul(self.inverse, arr) % 256
            
            # Append the characters to result.
            for x in decoded:
                result += chr(int(x[0]))
        
        # Return the string obtained when removing the padded characters.
        return result[:len(result) - count]
    
    # Pass matrices to printMatrix to neatly display values.
    def showMatrix(self):
        Encryptor.printMatrix(self.matrix)

    def showInverse(self):
        Encryptor.printMatrix(self.inverse)

    # Static method used to neatly display matrices.
    def printMatrix(matrix):
        size = matrix.shape[0]
        print(u'\u250C\u2500' + ' ' * (size*4 - 1) + u'\u2500\u2510')
        for x in range(size):
            row = u'\u2502'
            for y in range(size):
                row = row + ' {:3}'.format(str(matrix[x][y]))
            row = row + ' ' + u'\u2502'
            print(row)
        print(u'\u2514\u2500' + ' ' * (size*4 - 1) + u'\u2500\u2518')
    
    def matrix_generator(size):
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
            ls = []
            for x in range(size):
                tmp = []
                for y in range(size):
                    tmp.append(randrange(n))
                ls.append(tmp)
            matrix = np.array(ls)
            
            # Calculation of the determinant of the matrix.
            det = determinant(matrix)
            
            # If the determinant is negative, readjust by adding n until it reaches a positive congruent value mod n.
            while det < 0:
                det += n
            
            # Ensure that the det value is congruent to the det(matrix) and also between 0 and n.
            det %= n
            
            # Calculate the gcd and Bezout coefficients used in the creation of the inverse matrix.
            gcd, x, y = Encryptor.extended_gcd(n, det)
        
        # Calculating the inverse of the matrix through use of the matrix inversion formula.
        inverse = adjoint(matrix)
        
        # Ensure that the matrix only has a positive value when applying the mod operator.
        # This is necessary since Python allows for negative remainders which is not helpful
        # when applying the Hill Cipher.
        inverse = ((y * inverse) % n + n) % n
        
        # Return an Encryptor object which is found in classes.py.
        return matrix, inverse


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
            gcd, x1, y1 = Encryptor.extended_gcd(b, a % b)
            
            # Calculate the Bezout coeficcients as defined by the Extended Euclidean Algorithm.
            x = y1
            y = x1 - (a // b) * y1
            return gcd, x, y