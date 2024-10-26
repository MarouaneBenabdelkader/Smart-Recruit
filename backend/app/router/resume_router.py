from tempfile import NamedTemporaryFile
from fastapi import (
    APIRouter,
    Path,
    Query,
    Response,
    UploadFile,
    File,
    BackgroundTasks,
    Depends,
    HTTPException,
)
import zipfile
from bson import ObjectId
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from models.resume import Resume
from models.user import User
from services.resume_processing import (
    add_resume_processing_task,
    delete_resume_from_elasticsearch,
)
from database import get_database
from resources.nlp_loader import NLPResources
from schemas.resume import (
    RankedResume,
    ResumeCreateRequest,
    ResumeResponse,
)  # Define these Pydantic models appropriately
from typing import Any, List, Optional
from .auth_router import get_current_user
from datetime import datetime
import os

router = APIRouter(tags=["Resume"], responses={404: {"description": "Not found"}})


@router.post("/resumes/", status_code=201)
async def create_resumes(
    *,
    resume_files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks,
    db=Depends(get_database),
    current_user: dict = Depends(
        get_current_user
    ),  # Ensure that current_user is expected to be a dictionary
):
    uploaded_resumes = []
    for resume_file in resume_files:
        # Check file type
        if resume_file.content_type not in ["application/pdf"]:
            continue  # Skip files that are not PDFs, or handle differently

        # Save the file temporarily
        file_location = f"static/storage/{resume_file.filename}"

        with open(file_location, "wb") as file:
            contents = await resume_file.read()
            file.write(contents)

        # Create resume entry in MongoDB
        resume_model = Resume(db)
        resume_id = await resume_model.create_resume(
            file_path=file_location,
            upload_date=datetime.utcnow(),
            category="Unknown",  # Initial category, will be updated by background task
        )

        # Add resume to the current user's list of resumes
        user_model = User(db)
        await user_model.add_resume_to_user(
            current_user["_id"], resume_id
        )  # Corrected current_user ID access

        # Add a background task to process the resume
        add_resume_processing_task(
            background_tasks, str(resume_id), file_location, current_user["_id"], db
        )

        # Append successful upload info for response
        uploaded_resumes.append(
            {"resume_id": str(resume_id), "file_name": resume_file.filename}
        )

    if not uploaded_resumes:
        raise HTTPException(status_code=400, detail="No valid PDF files were uploaded.")

    return {
        "message": "Resumes uploaded successfully",
        "uploaded_resumes": uploaded_resumes,
    }


@router.get("/resumes", response_model=List[ResumeResponse])
async def get_user_resumes(
    db=Depends(get_database), current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user_model = User(db)
    resume_model = Resume(db)
    user_id = current_user["_id"]

    user_resumes = await user_model.get_resumes(user_id)
    if not user_resumes or len(user_resumes) == 0:
        return JSONResponse(
            status_code=404, content={"detail": "No resumes found for the user"}
        )

    resume_data = []
    for resume_id in user_resumes:
        resume = await resume_model.find_resume(resume_id)
        if resume:
            resume_data.append(
                ResumeResponse(
                    resume_id=str(resume_id),
                    upload_date=resume["UploadDate"],
                    category=resume["Category"],
                    file_path=resume["FilePath"],
                    skills=resume.get("Skills", []),
                    email=resume.get("Emails"),
                    phone=resume.get("PhoneNumbers"),
                )
            )

    return resume_data


@router.get("/resumes/files")
async def get_user_resume_files(
    db=Depends(get_database), current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user_model = User(db)
    resume_model = Resume(db)
    user_id = current_user["_id"]

    user_resumes = await user_model.get_resumes(user_id)
    if not user_resumes:
        return JSONResponse(
            status_code=404, content={"detail": "No resumes found for the user"}
        )

    zip_path = "temp_resumes.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for resume_id in user_resumes:
            resume = await resume_model.find_resume(resume_id)
            if resume and "FilePath" in resume:
                file_path = resume["FilePath"]
                if os.path.exists(file_path):
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                else:
                    continue  # Log or handle missing files separately

    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
        return FileResponse(
            path=zip_path, media_type="application/zip", filename=zip_path
        )
    else:
        os.remove(zip_path)  # Clean up empty zip if necessary
        return JSONResponse(
            status_code=404, content={"detail": "No accessible files found"}
        )


@router.get("/resumes/files/{resume_id}")
async def get_resume_file(
    resume_id: str = Path(..., description="The ID of the resume to retrieve"),
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    resume_model = Resume(db)
    resume = await resume_model.find_resume(ObjectId(resume_id))
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    file_path = resume.get("FilePath")
    if not file_path:
        raise HTTPException(status_code=404, detail="Resume file not found")

    return FileResponse(path=file_path, filename=file_path)


@router.get("/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str = Path(..., description="The ID of the resume to retrieve"),
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    resume_model = Resume(db)
    resume = await resume_model.find_resume(ObjectId(resume_id))
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return ResumeResponse(
        resume_id=str(resume_id),
        upload_date=resume["UploadDate"],
        category=resume["Category"],
        skills=resume.get("Skills", []),
    )


@router.get("/rank-resumes", response_model=List[RankedResume])
async def rank_resumes(
    job_description: str,
    latest: Optional[bool] = Query(
        None, description="Filter to only include resumes uploaded today"
    ),
    current_user: dict = Depends(get_current_user),
    size: int = Query(100, description="Number of results to return"),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    es = NLPResources.get_instance()["es"]  # Get Elasticsearch client from singleton

    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"text": job_description}},
                    {"match_all": {}},  # Ensures all documents are considered
                ],
                "minimum_should_match": 1,
                "filter": [],  # At least one of the should conditions must be met
            }
        },
        "sort": [{"_score": {"order": "desc"}}],  # Sort by BM25 score
        "size": size,
    }

    if latest:
        today_str = datetime.now().strftime("%Y-%m-%d")
        if "filter" not in search_body["query"]["bool"]:
            search_body["query"]["bool"]["filter"] = []
        search_body["query"]["bool"]["filter"].append(
            {
                "range": {
                    "UploadDate": {
                        "gte": f"{today_str}T00:00:00",
                        "lte": f"{today_str}T23:59:59",
                    }
                }
            }
        )
    # keep only resume of the current user
    search_body["query"]["bool"]["filter"].append(
        {"term": {"userId": current_user["_id"]}}
    )
    response = es.search(index="resumes", body=search_body)
    results = [
        RankedResume(
            resume_id=hit["_id"], path=hit["_source"]["path"], score=hit["_score"]
        )
        for hit in response["hits"]["hits"]
    ]
    return results


@router.delete("/delete-resume/{resume_id}", status_code=204)
async def delete_resume(
    *,
    resume_id: str = Path(..., description="The ID of the resume to delete"),
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(
        get_current_user
    ),  # Assuming authentication is required
    db=Depends(
        get_database
    ),  # Assuming you have a dependency that provides the database session
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Deleting from MongoDB
    resume_model = Resume(db)
    user_model = User(db)
    # delete resume from the filepath
    resume = await resume_model.find_resume(ObjectId(resume_id))
    # remove the resume id from the user's resume list
    await user_model.remove_resume_from_user(current_user["_id"], resume_id)
    if resume and "FilePath" in resume:
        file_path = resume["FilePath"]
        if os.path.exists(file_path):
            os.remove(file_path)
    delete_result = await resume_model.delete_resume(ObjectId(resume_id))
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Schedule deletion from Elasticsearch as a background task
    es = NLPResources.get_instance()["es"]
    background_tasks.add_task(delete_resume_from_elasticsearch, es, resume_id)

    return {"message": "Resume deletion initiated"}


@router.delete("/delete-resumes", status_code=204)
async def delete_resumes(
    resume_ids: List[str],  # List of resume IDs to be deleted
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db=Depends(
        get_database
    ),  # Assuming you have a dependency that provides the database session
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    es = NLPResources.get_instance()["es"]
    resume_model = Resume(db)
    user_model = User(db)
    #  fetch resumes to delete from the filepath
    for resume_id in resume_ids:
        resume = await resume_model.find_resume(ObjectId(resume_id))
        # remove the resume id from the user's resume list
        await user_model.remove_resume_from_user(current_user["_id"], resume_id)
        if resume and "FilePath" in resume:
            file_path = resume["FilePath"]
            if os.path.exists(file_path):
                os.remove(file_path)
    deleted_count = 0
    for resume_id in resume_ids:
        # MongoDB deletion
        delete_result = await resume_model.delete_resume(ObjectId(resume_id))
        deleted_count += delete_result.deleted_count

        # Schedule Elasticsearch deletion as a background task
        background_tasks.add_task(delete_resume_from_elasticsearch, es, resume_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="None of the resumes found")

    return {"message": f"Initiated deletion of {deleted_count} resumes."}
