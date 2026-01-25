import string
from secrets import choice


def generate_trash_string(length: int):
    ans = ''
    for _ in range(length):
        ans += choice(ALPHABET)
    return ans


ALPHABET = string.digits + string.ascii_letters

a = '1234567890'

a_c = ''
for i in a:
    a_c += i + choice(ALPHABET)

print(a_c)

clear = a_c[::2]


print(clear)
