from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from ... import schemas, models


def create_vote(db: Session, vote: schemas.VoteCreate, cur_user: schemas.User):
    
    db_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found",
        )
    vote_exists = db.query(models.Vote).filter(
        models.Vote.user_id == cur_user.id, models.Vote.post_id == vote.post_id).first()
    if vote.value == 1:
        if vote_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id {cur_user.id} already voted post with id {vote.post_id}",
            )
        # db_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        # db_post.upvotes += 1
        db_vote = models.Vote(**vote.model_dump(), user_id=cur_user.id)
        db.add(db_vote)
        db.commit()
    elif vote.value == 0:
        if vote_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {cur_user.id} has not voted post with id {vote.post_id}",
            )
        db.delete(vote_exists)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vote value must be 1 or 0",
        )
    return Response(status_code=status.HTTP_201_CREATED)
