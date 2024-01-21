import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_cmk():
    # Generate a Customer Master Key (CMK)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

def generate_cek():
    # Generate a Column Encryption Key (CEK)
    return os.urandom(32)  # 256 bits for AES-256

def to_bytes(value):
    if isinstance(value, str):
        return bytes(value, 'utf-8')
    elif isinstance(value, int):
        return value.to_bytes((value.bit_length() + 7) // 8, 'big')
    elif isinstance(value, float):
        # Convert the float to its IEEE 754 binary representation
        return struct.pack('!d', value)
    elif isinstance(value, bytes):
        return value
    else:
        # For other types, attempt to convert to string and then to bytes
        return bytes(str(value), 'utf-8')

def encrypt_aes_with_cek(cek, plaintext):
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)

    # Pad the plaintext using PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Create an AES cipher object using the CEK
    cipher = Cipher(algorithms.AES(cek), modes.CFB(iv), backend=default_backend())

    # Encrypt the padded data
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the IV and ciphertext as a tuple
    return iv + ciphertext

def decrypt_aes_with_cek(cek,ciphertext):
    # Extract the IV from the ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]


    # Create an AES cipher object using the CEK
    cipher = Cipher(algorithms.AES(cek), modes.CFB(iv), backend=default_backend())

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    #Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    return plaintext
