from bson import ObjectId


class Resume:
    def __init__(self, db):
        self.collection = db.resumes

    async def create_resume(self, file_path, upload_date, category):
        resume = {
            "FilePath": file_path,
            "UploadDate": upload_date,
            "Category": category,
            "Skills": [],
            "PhoneNumbers": "",
            "Emails": "",
        }
        result = await self.collection.insert_one(resume)
        return result.inserted_id

    async def update_resume(self, resume_id, update_data):
        result = await self.collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": update_data}
        )
        return result

    async def delete_resume(self, resume_id):
        result = await self.collection.delete_one({"_id": ObjectId(resume_id)})
        return result

    async def find_resume(self, resume_id):
        resume = await self.collection.find_one({"_id": ObjectId(resume_id)})
        return resume

    async def update_category(self, resume_id, category):
        return await self.collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": {"Category": category}}
        )

    async def update_skills(self, resume_id, skills):
        return await self.collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": {"Skills": skills}}
        )

    async def update_phone_numbers(self, resume_id, phone_numbers):
        return await self.collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": {"PhoneNumbers": phone_numbers}}
        )

    async def update_emails(self, resume_id, emails):
        return await self.collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": {"Emails": emails}}
        )

    async def get_skills(self, resume_id):
        resume = await self.collection.find_one(
            {"_id": ObjectId(resume_id)}, {"Skills": 1}
        )
        return resume.get("Skills", [])

    async def find_resumes_by_user_id(self, user_id):
        cursor = self.collection.find({"UserId": user_id})
        return await cursor.to_list(length=None)
