from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/api/posts", tags=["posts"])

# CRUD
@router.post("", response_model=schemas.PostOut, status_code=201)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = models.Post(title=payload.title, content=payload.content, owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("", response_model=List[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.owner_id != user.id:
        raise HTTPException(403, "Not the owner")
    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.owner_id != user.id:
        raise HTTPException(403, "Not the owner")
    db.delete(post)
    db.commit()
    return

# Likes
@router.post("/{post_id}/like", status_code=201)
def like_post(post_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    existing = db.query(models.Like).filter(models.Like.post_id == post_id, models.Like.user_id == user.id).first()
    if existing:
        return {"detail": "Already liked"}  # idempotent
    like = models.Like(post_id=post_id, user_id=user.id)
    db.add(like)
    db.commit()
    return {"detail": "Liked"}

# Comments
@router.post("/{post_id}/comment", response_model=schemas.CommentOut, status_code=201)
def add_comment(post_id: int, payload: schemas.CommentCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    comment = models.Comment(post_id=post_id, user_id=user.id, content=payload.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/{post_id}/comments", response_model=List[schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).order_by(models.Comment.created_at.desc()).all()
