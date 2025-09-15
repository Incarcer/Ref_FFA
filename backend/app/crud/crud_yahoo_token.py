from typing import Optional
from sqlalchemy.orm import Session
from app.models.yahoo_token import YahooToken
from app.schemas.yahoo_token import YahooTokenCreate

def get_by_user_id(db: Session, *, user_id: int) -> Optional[YahooToken]:
    return db.query(YahooToken).filter(YahooToken.user_id == user_id).first()

def create_or_update(
    db: Session, *, obj_in: YahooTokenCreate, user_id: int
) -> YahooToken:
    db_obj = get_by_user_id(db, user_id=user_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    if db_obj:
        for field, value in update_data.items():
            setattr(db_obj, field, value)
    else:
        db_obj = YahooToken(**update_data, user_id=user_id)
        db.add(db_obj)

    db.commit()
    db.refresh(db_obj)
    return db_obj