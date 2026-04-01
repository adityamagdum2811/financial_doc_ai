#  Financial Document AI (FastAPI + RAG + JWT Auth)

##  Overview
This project is a FastAPI-based Financial Document Management System with Semantic Search and Role-Based Access Control (RBAC).

It allows users to:
- Register and login using JWT authentication
- Upload financial documents (PDF, DOCX, TXT)
- Store document metadata in a database
- Search documents using metadata filters
- Perform semantic search using embeddings (RAG)
- Retrieve relevant document content using AI-based similarity

---

##  Tech Stack
- FastAPI (Backend API)
- SQLAlchemy (ORM)
- SQLite (Relational Database)
- JWT Authentication
- ChromaDB (Vector Database)
- Sentence Transformers (Embeddings)
- Python

---

##  Features
-  User Authentication (JWT)
-  Role-Based Access Control (Admin, Financial Analyst, Auditor, Client)
-  Document Upload & Management
-  Metadata Search (title, company, type)
-  Text Extraction (PDF, DOCX, TXT)
-  Semantic Search (RAG Pipeline)
-  FastAPI with Swagger UI

---
##  How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run server:
uvicorn app.main:app --reload

3. Open browser:
http://127.0.0.1:8000/docs
