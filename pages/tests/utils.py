import random

def random_email_generator(length=10):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    email =  "Testing-".join(random.choice(letters) for i in range(length))
    email += "@gmail.com"
    return email


