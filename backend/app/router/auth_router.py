from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from models.user import User
from database import get_database

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def jsonable_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [jsonable_encoder(item) for item in obj]
    if isinstance(obj, dict):
        return {key: jsonable_encoder(value) for key, value in obj.items()}
    return obj


async def get_user(db, username: str):
    user_model = User(db)
    user = await user_model.find_user_by_email(username)
    return user


async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user["Password"]):
        return False
    return user


# Dependency
async def get_current_user(
    db=Depends(get_database), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    # use json to serialize the user object
    user = jsonable_encoder(user)
    return user


class UserCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=3, max_length=100)
    company_name: str = Field(..., min_length=3, max_length=100)


@router.post("/register")
async def register_user(user: UserCreateRequest, db=Depends(get_database)):
    user_model = User(db)
    # check if user already exists
    user_exists = await user_model.find_user_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    hashed_password = get_password_hash(user.password)
    user_id = await user_model.create_user(
        full_name=user.full_name,
        password=hashed_password,
        email=user.email,
        department=user.department,
        company_name=user.company_name,
    )
    return jsonable_encoder(
        {"user_id": user_id, "message": "User registered successfully"}
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["Email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


class UserResponse(BaseModel):
    _id: str
    FullName: str
    Email: str
    Department: str
    CompanyName: str
    Resumes: list = []


@router.get(
    "/users/me/",
    response_model=UserResponse,
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # This endpoint doesn't need to do much since logout is managed on the client-side.
    return {"message": "Successfully logged out"}
