# QUESTION 1 - PERSONAL PORTFOLIO API

# Develop a fully functional API for a personal portfolio website.
# Include endpoints for projects (add, edit, delete, all project, single project),
# blog posts (add, edit, delete, all blog posts, single blog post),
# and contact information (add, edit, delete).
# Use SQLite as a database.
# Document the API endpoints and push your codes to your github repository.


from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import sqlite3

# Database setup
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Create tables for projects, blog posts, and contact information
cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  link TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS blog_posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT,
                  author TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  message TEXT)''')

conn.commit()

app = FastAPI()

# Models for API endpoints
class Project(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None

class BlogPost(BaseModel):
    title: str
    content: Optional[str] = None
    author: Optional[str] = None

class Contact(BaseModel):
    name: str
    email: str
    message: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Personal Portfolio API"}

# CRUD for Projects
@app.post("/projects/")
async def add_project(project: Project):
    cursor.execute("INSERT INTO projects (name, description, link) VALUES (?, ?, ?)", 
                   (project.name, project.description, project.link))
    conn.commit()
    return {"message": "Project added successfully"}

@app.get("/projects/")
async def get_projects():
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    return {"projects": projects}

@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if project:
        return {"project": project}
    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}")
async def update_project(project_id: int, project: Project):
    cursor.execute("UPDATE projects SET name = ?, description = ?, link = ? WHERE id = ?", 
                   (project.name, project.description, project.link, project_id))
    conn.commit()
    return {"message": "Project updated successfully"}

@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    return {"message": "Project deleted successfully"}

# CRUD for Blog Posts
@app.post("/blogposts/")
async def add_blogpost(blogpost: BlogPost):
    cursor.execute("INSERT INTO blog_posts (title, content, author) VALUES (?, ?, ?)", 
                   (blogpost.title, blogpost.content, blogpost.author))
    conn.commit()
    return {"message": "Blog post added successfully"}

@app.get("/blogposts/")
async def get_blogposts():
    cursor.execute("SELECT * FROM blog_posts")
    blogposts = cursor.fetchall()
    return {"blogposts": blogposts}

@app.get("/blogposts/{blogpost_id}")
async def get_blogpost(blogpost_id: int):
    cursor.execute("SELECT * FROM blog_posts WHERE id = ?", (blogpost_id,))
    blogpost = cursor.fetchone()
    if blogpost:
        return {"blogpost": blogpost}
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.put("/blogposts/{blogpost_id}")
async def update_blogpost(blogpost_id: int, blogpost: BlogPost):
    cursor.execute("UPDATE blog_posts SET title = ?, content = ?, author = ? WHERE id = ?", 
                   (blogpost.title, blogpost.content, blogpost.author, blogpost_id))
    conn.commit()
    return {"message": "Blog post updated successfully"}

@app.delete("/blogposts/{blogpost_id}")
async def delete_blogpost(blogpost_id: int):
    cursor.execute("DELETE FROM blog_posts WHERE id = ?", (blogpost_id,))
    conn.commit()
    return {"message": "Blog post deleted successfully"}

# CRUD for Contacts
@app.post("/contacts/")
async def add_contact(contact: Contact):
    cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", 
                   (contact.name, contact.email, contact.message))
    conn.commit()
    return {"message": "Contact added successfully"}

@app.get("/contacts/")
async def get_contacts():
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    return {"contacts": contacts}

@app.get("/contacts/{contact_id}")
async def get_contact(contact_id: int):
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()
    if contact:
        return {"contact": contact}
    raise HTTPException(status_code=404, detail="Contact not found")

@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: Contact):
    cursor.execute("UPDATE contacts SET name = ?, email = ?, message = ? WHERE id = ?", 
                   (contact.name, contact.email, contact.message, contact_id))
    conn.commit()
    return {"message": "Contact updated successfully"}

@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    return {"message": "Contact deleted successfully"}
