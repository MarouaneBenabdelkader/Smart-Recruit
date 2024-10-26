from pymongo import MongoClient
from bson import ObjectId


class User:
    def __init__(self, db):
        self.collection = db.users

    async def create_user(self, full_name, password, email, department, company_name):
        user = {
            "FullName": full_name,
            "Password": password,  # Ensure this is hashed in production
            "Email": email,
            "Department": department,
            "CompanyName": company_name,
            "Resumes": [],  # List to store references to resumes
        }
        result = await self.collection.insert_one(user)
        return result.inserted_id

    async def add_resume_to_user(self, user_id, resume_id):
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$push": {"Resumes": ObjectId(resume_id)}}
        )
        return result.modified_count  # Return the count of documents modified

    async def remove_resume_from_user(self, user_id, resume_id):
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$pull": {"Resumes": ObjectId(resume_id)}}
        )
        return result.modified_count  # Return the count of documents modified

    async def get_user_resumes(self, user_id):
        user = await self.collection.find_one(
            {"_id": ObjectId(user_id)}, {"Resumes": 1}
        )
        if user and "Resumes" in user:
            resume_ids = user["Resumes"]
            return [
                str(resume_id) for resume_id in resume_ids
            ]  # Return resume IDs as strings
        return []

    async def update_user(self, user_id, update_data):
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return result.modified_count  # Return the count of documents modified

    async def find_user_by_email(self, email):
        user = await self.collection.find_one({"Email": email})
        return user

    async def delete_user(self, user_id):
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count  # Return the count of documents deleted

    async def get_resumes(self, user_id):
        """
        Fetch all resume IDs associated with the user.
        """
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return user.get("Resumes", []) if user else []
