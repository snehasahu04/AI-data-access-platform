from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.user import User
from ..schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# Get all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users
