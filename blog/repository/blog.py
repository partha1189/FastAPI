from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status, Response
from sqlalchemy.sql import text

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    # return {'title':blog.title, 'body': blog.body}
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int, request:models.Blog, db:Session):
    blog = db.query(models.Blog).filter( models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    # blog.update(request, synchronize_session=False)
    query = text("""UPDATE blogs SET title=:title, body=:body WHERE id=:id""").params(title=request.title, body=request.body, id=id)
    db.execute(query)
    db.commit()
    return 'updated'

def show(id:int, response:Response ,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} is not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not available')
    return blog