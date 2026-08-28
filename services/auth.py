from sqlalchemy import select

from core import get_session
from models import User

def register_user(username: str, password: str) -> User | None:
    with get_session() as session:
        stmt = select(User).where(User.username == username)
        user = session.scalars(stmt).first()

        if user:
            raise ValueError("error_username_already_exists")

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
            raise ValueError("error_user_usrname_does_not_exist")

        if not user.check_password(password=password):
            raise ValueError("error_invalid_password")

        session.expunge(user)
        return user

def delete_user(user_id: int, password: str) -> bool:
    with get_session() as session:
        user = session.get(User, user_id)

        if not user:
            raise ValueError("error_user_does_not_exist")

        if not user.check_password(password=password):
            raise ValueError("error_invalid_password")

        session.delete(user)
        session.commit()

        return True

def update_username(user_id: int, new_username: str) -> None:
    with get_session() as session:
        stmt = select(User).where(User.username == new_username)
        existing_user = session.scalar(stmt)

        if existing_user and existing_user.id != user_id:
            raise ValueError("error_username_already_exists")

        user = session.get(User, user_id)
        if not user:
            raise ValueError("error_user_no_longer_exists")
        
        user.username = new_username
        session.commit()

def update_password(user_id: int, new_password: str) -> None:
    with get_session() as session:
        user = session.get(User, user_id)

        if not user:
            raise ValueError("error_user_does_not_exist")
        
        if user.check_password(password=new_password):
            raise ValueError("error_password_already_used")

        user.password = new_password
        session.commit()

def get_user_by_id(user_id: int) -> User | None:
    if not user_id:
        return None

    with get_session() as session:
        return session.get(User, user_id)

def get_user_by_username(username: str) -> User | None:
    with get_session() as session:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)