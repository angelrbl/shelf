from sqlalchemy import select, delete, func

from core import get_session
from models import User, Follow

def follow_user(current_user_id: int, target_user_id: int) -> None:
    if current_user_id == target_user_id:
        return
    
    with get_session() as session:
        is_following = session.scalar(
            select(Follow)
            .where(Follow.follower_id == current_user_id, Follow.followed_id == target_user_id)
        )

        if not is_following:
            new_follow = Follow(follower_id=current_user_id, followed_id=target_user_id)
            session.add(new_follow)
            session.commit()

def unfollow_user(current_user_id: int, target_user_id: int) -> None:
    if current_user_id == target_user_id:
        return
    
    with get_session() as session:
        stmt = (
            delete(Follow)
            .where(Follow.follower_id == current_user_id, Follow.followed_id == target_user_id)
        )
        session.execute(stmt)
        session.commit()

def is_following(current_user_id: int, target_user_id: int) -> bool:
    if current_user_id == target_user_id:
        return False

    with get_session() as session:
        stmt = (
            select(Follow)
            .where(Follow.follower_id == current_user_id, Follow.followed_id == target_user_id)
        )
        follow = session.scalar(stmt)

        return True if follow else False

def are_mutual_friends(current_user_id: int, target_user_id: int) -> bool:
    return is_following(current_user_id, target_user_id) and is_following(target_user_id, current_user_id)

def get_followers(user_id: int) -> list[User]:
    with get_session() as session:
        user = session.get(User, user_id)

        if not user:
            return []
        
        return list(user.followers)

def get_following(user_id: int) -> list[User]:
    with get_session() as session:
        user = session.get(User, user_id)

        if not user:
            return []
        
        return list(user.following)

def get_friends(user_id: int) -> list[User]:
    with get_session() as session:
        user = session.get(User, user_id)

        if not user:
            return []

        return list(set(user.followers) & set(user.following))
    
def get_follower_count(user_id: int) -> int:
    with get_session() as session:
        stmt = (
            select(func.count())
            .select_from(Follow)
            .where(Follow.followed_id == user_id)
        )

        return session.scalar(stmt)

def get_following_count(user_id: int) -> int:
    with get_session() as session:
        stmt = (
            select(func.count())
            .select_from(Follow)
            .where(Follow.follower_id == user_id)
        )

        return session.scalar(stmt)