from sqlalchemy import select

from core import get_session
from models import User

def register_user(username: str, password: str) -> User | None:
    with get_session() as session:
        stmt = select(User).where(User.username == username)
        user = session.scalars(stmt).first()

        if user:
            raise ValueError(f"User '{username}' already exists.")

        user = User(username=username, password=password)

        session.add(user)
        session.commit()

        session.refresh(user)
        session.expunge(user)

        return user

def authenticate_user(username: str, password: str) -> User | None:
    with get_session() as session:
        stmt = select(User).where(User.username == username)
        user = session.scalars(stmt).first()

        if not user:
            raise ValueError(f"User '{username}' does not exist.")

        if not user.check_password(password=password):
            raise ValueError(f"Invalid password for user '{username}'")

        session.expunge(user)
        return user