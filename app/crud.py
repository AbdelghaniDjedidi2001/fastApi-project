from sqlalchemy.orm import Session

from . import models, schemas


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    
    db.delete(db_post)
    db.commit()
    return db_post

def update_post(db: Session, post_id: int, post: schemas.PostCreate):
    db_post_query = db.query(models.Post).filter(models.Post.id == post_id)
    db_post = db_post_query.first()
    
    if not db_post:
        return None
    
    db_post_query.update(post.model_dump())
    db.commit()
    db.refresh(db_post)
    return db_post


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user