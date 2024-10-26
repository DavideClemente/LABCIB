from Crypto.PublicKey import RSA

# Read the public key from the file
with open('Arduino\Part1\public_key.txt', 'r') as file:
    pem_key = file.read()

# Load the public key using PyCryptodome
public_key = RSA.import_key(pem_key)

# Print the public key components (for example)
print("Public Key:")
print(public_key.export_key(format='PEM').decode())
