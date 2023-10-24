from fastapi import HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models
from ... import schemas




def get_post(db: Session, post_id: int):
    db_post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} not found",
            )
    return db_post

def get_posts(db: Session, skip: int, limit: int, search: str):
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.craeted_at.desc())
    return posts.filter(
            models.Post.title.contains(search)).offset(skip).limit(limit).all()

def create_post(db: Session,id: int ,post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump(),user_id=id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session,user_id: int,post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} not found",
            )
    if db_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Not ALlowed",
            )
    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)

def update_post(db: Session, post_id: int,user_id: int,post: schemas.PostCreate):
    db_post_query = db.query(models.Post).filter(models.Post.id == post_id)
    db_post = db_post_query.first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} not found",
            )
    
    if db_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Not ALlowed",
            )
    for key, value in post.model_dump().items():
        if value != None:
            setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post
