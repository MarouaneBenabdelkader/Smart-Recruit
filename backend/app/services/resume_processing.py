from datetime import datetime
from fastapi import BackgroundTasks
from utils.info_extraction import extract_info
from models.resume import Resume
from utils.text_extraction import extract_text_from_pdf
from utils.text_normalization import normalize_text
from utils.skill_extraction import extract_skills
from resources.nlp_loader import NLPResources
from bson import ObjectId  # Make sure to import ObjectId


async def process_resume(resume_id: str, pdf_path: str, user_id: str, db):
    resources = NLPResources.get_instance()
    es_client = resources["es"]
    matcher = resources["matcher"]
    nlp = resources["nlp"]
    vectorizer = resources["vectorizer"]
    svm_model = resources["model"]

    # Text extraction and processing
    text = extract_text_from_pdf(pdf_path)
    normalized_text = normalize_text(text, nlp)
    skills = extract_skills(text, matcher)

    # Model prediction
    text_vector = vectorizer.transform([normalized_text])
    predicted_category = svm_model.predict(text_vector)[0]
    information = extract_info(text)
    phone = information.get("phone")
    email = information.get("email")
    # MongoDB operations
    resume_model = Resume(db)
    await resume_model.update_category(ObjectId(resume_id), predicted_category)
    await resume_model.update_skills(resume_id, skills)
    await resume_model.update_phone_numbers(resume_id, phone)
    await resume_model.update_emails(resume_id, email)
    # Retrieve the upload date from MongoDB
    resume_data = await resume_model.find_resume(ObjectId(resume_id))
    upload_date = resume_data.get(
        "UploadDate", datetime.now()
    )  # Fallback to current time if not found

    # Prepare the document to be indexed in Elasticsearch
    doc = {
        "userId": user_id,
        "resume_id": resume_id,
        "filename": pdf_path.split("/")[-1],
        "path": pdf_path,
        "text": text,
        "normalized_text": normalized_text,
        "skills": skills,
        "category": predicted_category,
        "phone": phone,
        "email": email,
        "UploadDate": upload_date.strftime(
            "%Y-%m-%dT%H:%M:%S"
        ),  # Formatting date to ISO 8601 format
    }

    # Index the document in Elasticsearch
    es_client.index(index="resumes", id=resume_id, body=doc)
    print(
        "Elasticsearch document updated with MongoDB resume_id, user_id, and upload date."
    )


def add_resume_processing_task(
    background_tasks: BackgroundTasks, resume_id: str, pdf_path: str, user_id: str, db
):
    background_tasks.add_task(process_resume, resume_id, pdf_path, user_id, db)


async def delete_resume_from_elasticsearch(es, resume_id):
    try:
        es.delete(index="resumes", id=resume_id)
        print(f"Successfully deleted resume {resume_id} from Elasticsearch.")
    except Exception as e:
        print(f"Error deleting resume {resume_id} from Elasticsearch: {e}")
