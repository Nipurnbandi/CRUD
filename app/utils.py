from passlib.context import CryptContext

# create hashing object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash password
def hash(password: str):
    return pwd_context.hash(password)

# verify password (for login)
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong(password):
    if len(password) < 8:
        return False

    hasUpper =False
    hasLower =False
    hasDigit =False
    hasSpecial =False

    for p in password:
        if p.isupper():
            hasUpper = True
        elif p.islower():
            hasLower = True
        elif p.isdigit():
            hasDigit = True
        elif not p.isalnum():
            hasSpecial = True

    return hasUpper and hasLower and hasDigit and hasSpecial
































    

    
