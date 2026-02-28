from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
import models, Schemas
from database import get_db


router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    safe_password = password[:72] 
    return pwd_context.hash(safe_password)

def verify_password(plain, hashed):
    safe_password = plain[:72]
    return pwd_context.verify(safe_password, hashed)

@router.post("/register", response_model=Schemas.UserResponse)

async def register(user_in: Schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:

        result = await db.execute(select(models.User).where(models.User.email == user_in.email))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")


        hashed_pw = hash_password(user_in.password)

        new_user = models.User(
            username=user_in.username, 
            email=user_in.email, 
            hashed_password=hashed_pw
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:

        await db.rollback() 
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/login")
async def login(credentials: Schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    try:

        result = await db.execute(select(models.User).where(models.User.email == credentials.email))

        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )

        return {"message": "Login successful", "username": user.username}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")