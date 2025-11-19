import os
import hashlib
import pickle

def bad_code(cmd, password, data):
    os.system(cmd)  # 🚨 Command injection
    hashlib.md5(password.encode()).hexdigest()  # 🚨 Weak hash
    pickle.loads(data)  # 🚨 Insecure deserialization
