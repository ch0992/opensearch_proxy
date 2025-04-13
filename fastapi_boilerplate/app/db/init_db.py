import logging

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But we create them here for testing purposes
    from app.db.base_class import Base
    from app.db.session import engine
    Base.metadata.create_all(bind=engine)
    
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info("Created first superuser")
