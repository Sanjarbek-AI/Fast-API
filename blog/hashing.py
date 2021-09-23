from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(self: str):
        return pwd_context.hash(self)

    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)
