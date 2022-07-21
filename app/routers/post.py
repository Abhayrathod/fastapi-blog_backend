from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from .. database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



# post_list = [{"title":"new_model","content":"anjkndjvk","id":1},{'title':'dsjjsdvn','content':"sdfhsdbvhdvj","id":2}]


# @router.get("/posts")
# def root():
#     return post_list


# @router.get("/sqlalchemy")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}




    
# @router.post("/posts")
# def  create_posts(payload:dict = Body(...)):
#     payload1 = {}
#     payload1 = payload
#     print(payload1)
#     return {"message":f"title {payload1['title']} and content is {payload1['content']}"}

# @router.post("/posts")
# def create_posts(new_post:Posts,status_code=status.HTTP_201_CREATED):
#     # print(new_post.title)
#     # print(new_post.dict())
#     post_d = new_post.dict()
#     post_d['id'] = randrange(0,10000)
#     post_list.append(post_d)
#     return {"data": post_d}


# def find_post(id):
#     for P in post_list:
#         if P["id"] == id:
#             return  P

# def find_index(id):
#     for i,p in enumerate(post_list):
#         if p['id'] == id:
#             return i

#--------------------------method1
# @app.get("/posts/{id}")
# def get_id(id:int,response:Response):
#     # if id == post_list[id]:
#     #     return post_list[id]
#     print(type(id))
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail":"Not found"}
#     return {"data": post}

# #---------------------------method2
# @router.get("/posts/{id}")
# def get_id(id:int):
#     # if id == post_list[id]:
#     #     return post_list[id]
#     # print(type(id))
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
#     return {"data": post}



# @router.get("/post/latest")           #this will not work because of the above api to run this
# def latest():                                                       #to run this comment the  whole above code 
#     posts = post_list[len(post_list)-1]
#     return {"detail":posts}


# @router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     index = find_index(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found")
#     post_list.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.put("/posts/{id}")
# def update_post(id:int, post:Posts):
#     index = find_index(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found")
    
#     post_dict = post.dict()
#     post_dict['id'] = id
#     post_list[index] = post_dict
#     return {"data": post_dict}

@router.post("",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # print(**post.dict())
    # new_post = models.Post(title=post.title, content=post.Content , published=post.published)
    new_post = models.Post(owner_id=user_id.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id:int,db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    return {"detail":post}


@router.get("",status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
def get_post(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).all()
    post = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() #to get only loggedin user post, comment aboce query for this to work
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_post(updated_post: schemas.PostUpdate, id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    print(updated_post.dict())

    db.commit()
    return post_query.first()