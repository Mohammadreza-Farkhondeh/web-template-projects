from typing import List

from sqlalchemy.orm import Session

from app.db.models import User
from app.crud.base import CRUDBase
from app.api.schemas import UserCreate, UserUpdate


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(
        self, db: Session, passenger_id: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return db.query(self.model).filter(self.model.passenger_id == passenger_id).offset(skip).limit(limit).all()

    def get_by_name(
        self, db: Session, driver_id: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return db.query(self.model).filter(self.model.driver_id == driver_id).offset(skip).limit(limit).all()


ride_crud = UserCRUD(User)
