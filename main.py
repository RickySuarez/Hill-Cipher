from my_module.Encryptor import Encryptor

val = input("What message do you want encoded?\n")
size = int(input("\nWhat size do you want the matrix to be?\n"))
try:
    encryptor = Encryptor(size)
except:
    while(size < 1):
        size = int(input("The size must be positive.\nWhat size do you want the matrix to be?\n"))


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