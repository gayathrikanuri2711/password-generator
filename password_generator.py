import random
import string
import hashlib
import sqlite3

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    favourite TEXT,
    password TEXT
)
""")
conn.commit()

used_passwords = set()

def generate_password(username, favourite, length):

    # Take meaningful parts (NOT too short)
    user_part = username[:4]
    fav_part = favourite[:4]

    # Create hash for uniqueness
    seed = username + favourite
    hashed = hashlib.sha256(seed.encode()).hexdigest()

    # Character sets
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%&*"

    # Ensure minimum structure
    base = user_part + fav_part
    symbol = random.choice(symbols)
    digit = random.choice(digits)

    # Remaining characters
    remaining_length = length - len(base) - 2  # -2 for symbol + digit

    if remaining_length < 2:
        remaining_length = 2  # safety

    random_part = ''.join(random.choice(letters) for _ in range(remaining_length))

    # Final password
    password = base + symbol + digit + random_part + hashed[:2]

    # Trim ONLY if needed
    password = password[:length]

    # Ensure uniqueness
    if password not in used_passwords:
        used_passwords.add(password)
        return password
    else:
        return generate_password(username, favourite, length)


# ---------------- MAIN ----------------
print("🔐 Password Generator")

username = input("Enter username: ")
favourite = input("Enter favourite thing: ")
length = int(input("Enter password length (min 8): "))

if length < 8:
    length = 8

password = generate_password(username, favourite, length)

cursor.execute(
    "INSERT INTO passwords (username, favourite, password) VALUES (?, ?, ?)",
    (username, favourite, password)
)
conn.commit()

print("\nGenerated Password:", password)
print("Length:", len(password))
print("Saved successfully ✅")