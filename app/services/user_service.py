from app.database import db
from bson import ObjectId

def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "phone": user["phone"],
    }


class UserService:
    @staticmethod
    async def create_user(data):
        result = await db.users.insert_one(data)
        user = await db.users.find_one({"_id": result.inserted_id})
        return user_entity(user)

    @staticmethod
    async def get_user(id: str):
        user = await db.users.find_one({"_id": ObjectId(id)})
        return user_entity(user) if user else None

    @staticmethod
    async def get_all_users():
        users = await db.users.find().to_list(100)
        return [user_entity(u) for u in users]
