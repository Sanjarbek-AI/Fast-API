from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(self: str):
        return pwd_context.hash(self)
