from fastapi import APIRouter, Depends, HTTPException
from models.post import Post, PostToSave
from db import get_database
from bson import ObjectId
from typing import List


router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(post: PostToSave, db=Depends(get_database)):
    try:
        # Create a new post in the database
        inserted_post = await db.post.insert_one(post.dict())
        post_id = inserted_post.inserted_id
        post = await db.post.find_one({"_id": post_id})
        modified_post = {"id": str(post.pop("_id")), **post}
        print(modified_post)
        return Post(**modified_post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: str, db=Depends(get_database)):
    # Retrieve a post from the database by ID
    print(post_id)
    postId = ObjectId(post_id)
    post = await db.post.find_one({"_id": postId})
    modified_post = {"id": str(post.pop("_id")), **post}
    print(post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**modified_post)


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post, db=Depends(get_database)):
    # Check if the post exists
    postId = ObjectId(post_id)
    print(postId)
    print("post", post)
    existing_post = await db.post.find_one({"_id": postId})
    print("existing_post", existing_post)
    # del post[id]
    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update the post in the database
    replika_post = {"title": post.title,
                    "description": post.description, "image": post.image}
    await db.post.update_one({"_id": postId}, {"$set": replika_post})
    updated_post = await db.post.find_one({"_id": postId})
    print(updated_post)
    modified_post = {"id": str(updated_post.pop("_id")), **updated_post}

    return Post(**modified_post)


@router.delete("/posts/{post_id}", response_model=Post)
async def delete_post(post_id: str, db=Depends(get_database)):
    # Check if the post exists
    postId = ObjectId(post_id)
    existing_post = await db.post.find_one({"_id": postId})
    print(existing_post)
    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Delete the post from the database
    res = await db.post.delete_one({"_id": postId})
    print(res.deleted_count)
    modified_post = {"id": str(existing_post.pop("_id")), **existing_post}
    return Post(**modified_post)


@router.get("/posts/", response_model=List[Post])
async def read_posts(db=Depends(get_database)):
    try:
        # Retrieve all posts from the database
        posts = await db.post.find().to_list(length=None)
        modified_posts = [{"id": str(post.pop("_id")), **post}
                          for post in posts]
        return modified_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
