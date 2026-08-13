from core import get_session
from models import User

def are_mutual_friends(user_a_id: int, user_b_id: int) -> bool:
    if user_a_id == user_b_id:
        return False

    with get_session() as session:
        user_a = session.get(User, user_a_id)
        user_b = session.get(User, user_b_id)

        if not user_a or not user_b:
            return False

        a_follows_b = user_b in user_a.following
        b_follows_a = user_b in user_a.followers

        return a_follows_b and b_follows_a