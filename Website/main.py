import pyodbc
import warnings
from AESutils import generate_cmk, generate_cek, to_bytes, encrypt_aes_with_cek, decrypt_aes_with_cek
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
import os
warnings.filterwarnings("ignore")

# Generate CMK and CEK
cmk = generate_cmk()
file_path = r'C:\Users\rjtdu\OneDrive\Desktop\Hitachi_techenergy\cek.txt'

if os.path.exists(file_path):
    # File exists, read the contents
    with open(file_path, 'rb') as file:
        cek = file.read()
    print(f'CEK loaded.')
else:
    # File doesn't exist, generate a new CEK
    cek = generate_cek()
    # Write the new CEK to the file
    with open(file_path, 'wb') as file:
        file.write(cek)
    print(f'CEK generated.')


# Use CMK to encrypt CEK (Key Wrapping)
cmk_encrypted_cek = cmk.public_key().encrypt(
    cek,
    OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

def enter_data(a,b,c):
    conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=CRUEL;"

            "Database=rajat;"

            "Trusted_Connection=yes;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query1 = "SELECT fullname FROM user_info WHERE email = ?"
    cursor.execute(query1, (b,))

    i = cursor.fetchall()
    if len(i) != 0:
        print("This email already exists.")
        cursor.close()
        return 0
    else:
        #Call the function which encrypts the data
        cc = to_bytes(c)
        encrypted_data = encrypt_aes_with_cek(cek, cc)

        # Use parameterized query to avoid SQL injection
        query2 = "INSERT INTO user_info VALUES (?, ?, ?)"
        cursor.execute(query2, (a, b, b64encode(encrypted_data).decode()))
        #cursor.execute(query2, (a, b, encrypted_data.decode('latin-1')))

        #print('Database ma halnu aghi',b64encode(encrypted_data).decode())
        #cursor.execute(f"INSERT INTO user_info values ({a},{b},{c})")
        cursor.commit()
        cursor.close()
        print("Information Stored and Encrypted successfully.")
        return 1

def retreive_data(d):
    conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=CRUEL;"

            "Database=rajat;"

            "Trusted_Connection=yes;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # Use parameterized query to avoid SQL injection
    query = "SELECT fullname FROM user_info WHERE email = ?"
    cursor.execute(query, (d,))

    i = cursor.fetchall()
    if len(i) == 0:
        print("Error: No such email found.")
        cursor.close()
    else:

        cursor.execute(f"Select * from user_info where email = '{d}'")
        row = cursor.fetchone()
        cursor.close()

        #Decrypt the credit card number now -- Card no is stored in row[2]
        x = row[2]
        #print('SQL bata tanesi:', x)
        val = b64decode(x)
        #print('SQL bata taneko decode vayesi', val)
        decrypted_data = decrypt_aes_with_cek(cek, val)


        print(f"Name: {row[0]}")
        print(f"Email: {row[1]}")
        print(f"Credit card number encrypted: {row[2]}")
        print(f"Credit card number decrypted:", decrypted_data.decode())
        return row[0], row[1], decrypted_data.decode()

#enter_data('rajat', 'rjtdulal@gmail.com', 'Ad34-A34-45Dd-34ff')
#retreive_data('rjtdulal@gmail.com')