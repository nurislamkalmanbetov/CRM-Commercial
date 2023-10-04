import random
import string


def generate_random_string(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generate_random_email():
    title = generate_random_string(7)
    return f'{title}@gmail.com'


def generate_random_phone():
    codes = ['550', '700', '900', '770', '552', '554', '556', '555']
    
    phone_number = ''

    for i in range(6):
        phone_number = phone_number + str(random.randint(0, 9))

    return f'996{codes[random.randint(0,len(codes) - 1)]}{phone_number}'
