from my_module.Encryptor import Encryptor

val = input("What message do you want encoded?\n")
size = int(input("\nWhat size do you want the matrix to be?\n"))
encryptor = Encryptor(size)

print("\nEncrypting \"" + val + "\" with the matrix:")
encryptor.showMatrix()

encoded = encryptor.encrypt(val)
print("\nEncryption:")
print(encoded)

decoded = encryptor.decrypt(encoded)
print("\nDecrypting \"" + encoded + "\" with the matrix:")
encryptor.showInverse()

print("\nDecryption:")
print(decoded + "\n")