#this file generates a 16 characters long alphanumeric string randomly for identifying the unique devices.
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

def genClientID():
    return get_random_string(16)

