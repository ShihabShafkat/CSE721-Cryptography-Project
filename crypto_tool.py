import string
import math
import numpy as np

ALPHABET = string.ascii_uppercase

# ------------------ CAESAR CIPHER ------------------
def caesar_encrypt(text, shift):
    result = ""
    text = text.upper()
    for char in text:
        if char in ALPHABET:
            result += ALPHABET[(ALPHABET.index(char) + shift) % 26]
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ------------------ AFFINE CIPHER ------------------
def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(text, a, b):
    text = text.upper()
    result = ""
    for char in text:
        if char in ALPHABET:
            x = ALPHABET.index(char)
            result += ALPHABET[(a * x + b) % 26]
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    inv = mod_inverse(a, 26)
    if inv is None:
        return "Invalid key!"
    result = ""
    for char in text:
        if char in ALPHABET:
            y = ALPHABET.index(char)
            result += ALPHABET[(inv * (y - b)) % 26]
        else:
            result += char
    return result


# ------------------ PLAYFAIR CIPHER ------------------
def playfair_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))
    matrix = key + "".join(c for c in ALPHABET if c not in key and c != 'J')
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_pairs(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs

def playfair_encrypt(text, key):
    matrix = playfair_matrix(key)
    pairs = playfair_pairs(text)
    result = ""

    for pair in pairs:
        r1, c1 = [(r, row.index(pair[0])) for r, row in enumerate(matrix) if pair[0] in row][0]
        r2, c2 = [(r, row.index(pair[1])) for r, row in enumerate(matrix) if pair[1] in row][0]

        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result


# ------------------ HILL CIPHER (2x2) ------------------
def hill_encrypt(text, key):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'

    key_matrix = np.array(key)
    result = ""

    for i in range(0, len(text), 2):
        vector = np.array([[ALPHABET.index(text[i])],
                           [ALPHABET.index(text[i+1])]])
        res = key_matrix.dot(vector) % 26
        result += ALPHABET[int(res[0])] + ALPHABET[int(res[1])]
    return result

def hill_decrypt(text, key):
    key_matrix = np.array(key)
    det = int(round(np.linalg.det(key_matrix)))
    det_inv = mod_inverse(det % 26, 26)

    if det_inv is None:
        return "Invalid key matrix!"

    adj = np.array([[key_matrix[1][1], -key_matrix[0][1]],
                    [-key_matrix[1][0], key_matrix[0][0]]])

    inv_key = (det_inv * adj) % 26
    return hill_encrypt(text, inv_key)


# ------------------ MENU ------------------
def menu():
    print("\n--- CRYPTO TOOL ---")
    print("1. Caesar Cipher")
    print("2. Affine Cipher")
    print("3. Playfair Cipher")
    print("4. Hill Cipher")
    choice = input("Choose cipher: ")

    if choice == '1':
        text = input("Text: ")
        shift = int(input("Shift: "))
        op = input("E/D: ").upper()
        print(caesar_encrypt(text, shift) if op == 'E' else caesar_decrypt(text, shift))

    elif choice == '2':
        text = input("Text: ")
        a = int(input("a: "))
        b = int(input("b: "))
        op = input("E/D: ").upper()
        print(affine_encrypt(text, a, b) if op == 'E' else affine_decrypt(text, a, b))

    elif choice == '3':
        text = input("Text: ")
        key = input("Key: ")
        print(playfair_encrypt(text, key))

    elif choice == '4':
        text = input("Text: ")
        key = [[int(input(f"Key[{i}][{j}]: ")) for j in range(2)] for i in range(2)]
        op = input("E/D: ").upper()
        print(hill_encrypt(text, key) if op == 'E' else hill_decrypt(text, key))

menu()
