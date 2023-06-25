from fastapi import FastAPI,Depends,HTTPException,status,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from .database import engine,get_db
from sqlalchemy.orm import Session
from api import models,schemas
from .utils import get_hashed_password,verify_password,create_access_token,create_refresh_token,decrypt_token

app =FastAPI()

models.Base.metadata.create_all(bind = engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token')
def token(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    password = str(form_data.password)
    check_hashed = db.query(models.User).filter(models.User.username == form_data.username).first()
    hashed_password = verify_password(password,check_hashed.password)
    if not hashed_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    else:
        access_token = create_access_token(check_hashed.username)
        refresh_token = create_refresh_token(check_hashed.username)
        return {"access_token":access_token,"refresh_token": refresh_token}
    

@app.get('/')
def index(token: str = Depends(oauth2_scheme)):
    return {"token":token}

@app.post('/create_user')
def create_User(payload : schemas.UserSchema, db :  Session = Depends(get_db)):
    try:
        payloadDict= payload.dict()
        password = payloadDict["password"]
        hashed_password = get_hashed_password(password)
        payloadDict["password"] = hashed_password
        new_user = models.User(**payloadDict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(status_code=status.HTTP_226_IM_USED)

@app.post('/post')
def create_post(payload : schemas.PostSchema, db: Session =  Depends(get_db),token: str = Depends(oauth2_scheme)):
     user = decrypt_token(token)
     user = db.query(models.User).filter(models.User.username == user).first()
     id = user.id
     new_post = models.Post(title = payload.title , owner_id = id)
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     return new_post

@app.get('/display_post')
def post_display(db : Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    user = decrypt_token(token)
    user = db.query(models.User).filter(models.User.username == user).first()
    id = user.id
    posts = db.query(models.Post).filter(models.Post.owner_id == id).all()
    return posts

@app.patch('/update/{postId}')
def post_update(postId : int, payload : schemas.PostSchema, db : Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
     post_query = db.query(models.Post).filter(models.Post.id == postId)
     db_post = post_query.first()

     if not db_post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
     update_data = payload.dict(exclude_unset=True)
     post_query.filter(models.Post.id == postId).update(update_data,synchronize_session=False)
     db.commit()
     db.refresh(db_post)
     return db_post

@app.delete('/delete/{postId}')
def post_delete(postId : int ,db : Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    user = decrypt_token(token)
    user = db.query(models.User).filter(models.User.username == user).first()
    id = user.id
    post_query = db.query(models.Post).filter(models.Post.id == postId, models.Post.owner_id == id)
    db_post = post_query.first()

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
     
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete('/delete_user/{userId}')
def delete_user(userId : int , db : Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    user = decrypt_token(token)
    username = "random"
    if user != username :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_query = db.query(models.User).filter(models.User.id == userId)
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)