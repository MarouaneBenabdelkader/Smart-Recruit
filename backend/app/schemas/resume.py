from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ResumeCreateRequest(BaseModel):
    file_path: str = Field(..., description="Path where the resume file is stored")
    upload_date: datetime = Field(
        default_factory=datetime.utcnow, description="Upload date of the resume"
    )
    category: Optional[str] = Field(None, description="Category of the resume")

    class Config:
        schema_extra = {
            "example": {
                "file_path": "static/storage/resume.pdf",
                "upload_date": "2024-05-29T12:34:56.789Z",
                "category": "Engineering",
            }
        }


class ResumeResponse(BaseModel):
    resume_id: str
    file_path: Optional[str] = Field(None, description="Path to the resume file")
    upload_date: Optional[datetime] = Field(
        None, description="Upload date of the resume"
    )
    category: Optional[str] = Field(
        None, description="Predicted category of the resume"
    )
    skills: Optional[List[str]] = Field(
        None, description="Extracted skills from the resume"
    )
    email: Optional[str] = Field(None, description="Extracted email from the resume")
    phone: Optional[str] = Field(
        None, description="Extracted phone number from the resume"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "Resume uploaded successfully",
                "resume_id": "1234567890abcdef",
                "file_path": "static/storage/resume.pdf",
                "upload_date": "2024-05-29T12:34:56.789Z",
                "category": "Engineering",
                "skills": ["Python", "Machine Learning", "Data Analysis"],
            }
        }


class RankedResume(BaseModel):
    resume_id: str
    path: str
    score: float


# Adjust the endpoint to use this model in the response
