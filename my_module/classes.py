"""Classes used throughout project"""
import numpy as np

"""Objects of the Encryptor class have two numpy arrays as instance attributes in order to encrypt and decrypt"""
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
    
    def __init__(self, matrix, inverse):
        """
        Constructor assigns a matrix and its inverse used to encrypt and decrypt.
        This constructor ensures that the matrices are inverses mod 256.
        Otherwise, it raises an exception.

        Args:
            matrix (numpy.ndarray): The encryption matrix.
            inverse (numpy.ndarray): The inverse matrix used for decryption.
        """
        
        # Multiply the matrices.
        product = np.matmul(matrix, inverse) % 256
        
        # If the product is equal to an identity matrix,
        # Assign instance attributes.
        identity = np.identity(matrix.shape[0])
        if np.array_equal(product, identity):
            self.matrix = np.array(matrix)
            self.inverse = np.array(inverse)
        
        # If the product is not equal to an identity matrix,
        # raise an exception.
        else:
            raise Exception('The given matrices are not inverses mod 256.')
        
   
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