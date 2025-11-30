from fastapi import FastAPI
from typing import List, Dict, Any
import uvicorn
# Create FastAPI instance
app = FastAPI(title="Simple FastAPI", version="1.0.0")

# In-memory storage (for demo purposes)
users_db: List[Dict[str, Any]] = []
user_counter = 0

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Simple FastAPI!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Get all users
@app.get("/users")
def get_users():
    return {"users": users_db}

# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user:
        return user
    return {"error": "User not found"}

# Create new user
@app.post("/users")
def create_user(name: str, email: str):
    global user_counter
    user = {"id": user_counter, "name": name, "email": email}
    users_db.append(user)
    user_counter += 1
    return {"message": "User created", "user": user}

# Update user
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user:
        if name:
            user["name"] = name
        if email:
            user["email"] = email
        return {"message": "User updated", "user": user}
    return {"error": "User not found"}

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user:
        users_db = [u for u in users_db if u["id"] != user_id]
        return {"message": "User deleted", "user": user}
    return {"error": "User not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)