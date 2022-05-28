from fastapi import FastAPI , Depends, status , HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/blog")
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    # return {'title': blog.title, 'body': blog.body}
    new_blog = models.Blog(title=blog.title, body=blog.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id ).delete(synchronize_session=False)
    db.commit()

    return 'done'


@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id) #{'title': "update title"}
    if not  blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.update(request.dict())
    db.commit()

    return 'updated'  


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    return blog