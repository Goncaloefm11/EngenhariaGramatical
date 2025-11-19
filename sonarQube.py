# main.py — vulnerabilidades pro Sonar detectar

import hashlib
import sqlite3

def insecure_password_check(pwd: str) -> bool:
    # Hardcoded credential
    if pwd == "12345":
        print("Weak password!")
    return len(pwd) > 5

def unsafe_eval(user_input: str):
    # Code injection risk
    return eval(user_input)

def weak_hash(data: str) -> str:
    # Uso inseguro de MD5
    return hashlib.md5(data.encode()).hexdigest()

def sql_injection_example(db_path: str, username: str):
    # SQL injection (concatenação direta)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)  # vulnerável
    rows = cur.fetchall()
    conn.close()
    return rows

def division(a: int, b: int):
    try:
        return a / b
    except Exception:  # captura genérica
        return None

if __name__ == "__main__":
    pwd = "12345"
    insecure_password_check(pwd)
    print(unsafe_eval("2+2"))
    print(weak_hash("secret"))
    print(sql_injection_example(":memory:", "admin' OR '1'='1"))
    print(division(10, 0))
