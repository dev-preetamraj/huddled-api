from django.conf import settings


def decrypt(text):
    key = settings.SECRET_KEY
    decrypted = ''
    for i in range(len(text)):
        char_code = ord(text[i]) ^ ord(key[i % len(key)])
        decrypted += chr(char_code)
    return decrypted
