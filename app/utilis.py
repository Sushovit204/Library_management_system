from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashes the password using the library
def hash(password: str):
    return pwd_context.hash(password)

#compares the hash and plain password for validation 
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)