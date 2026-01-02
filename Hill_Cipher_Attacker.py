import numpy as np
import string
import math

ALPHABET = string.ascii_uppercase

def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def text_to_matrix(text):
    text = text.upper().replace(" ", "")
    nums = [ALPHABET.index(c) for c in text]

    # COLUMN-WISE construction
    return [[nums[0], nums[2]],
            [nums[1], nums[3]]]

def matrix_inverse_mod26(matrix):
    det = int(round(np.linalg.det(matrix))) % 26
    det_inv = mod_inverse(det, 26)

    if det_inv is None:
        return None

    adj = np.array([[matrix[1][1], -matrix[0][1]],
                    [-matrix[1][0], matrix[0][0]]])

    return (det_inv * adj) % 26

def hill_known_plaintext_attack(plaintext, ciphertext):
    p = np.array(text_to_matrix(plaintext))
    c = np.array(text_to_matrix(ciphertext))

    det = int(round(np.linalg.det(p))) % 26
    if math.gcd(det, 26) != 1:
        return "Plaintext matrix is NOT invertible modulo 26!"

    p_inv = matrix_inverse_mod26(p)
    key = (c.dot(p_inv)) % 26
    return key

# ----------- RUN -----------
pt = input("Known Plaintext (4 letters): ")
ct = input("Corresponding Ciphertext (4 letters): ")

key = hill_known_plaintext_attack(pt, ct)
print("\nRecovered Key Matrix:")
print(key)
