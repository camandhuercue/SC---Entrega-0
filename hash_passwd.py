import bcrypt

def hash_passwd(passwd):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed

def check_passwd(passwd, hashed):
    if bcrypt.checkpw(passwd, hashed):
        return True
    else:
        return False
