# 🔍 AI-Powered Plagiarism Detection System

An intelligent, full-stack plagiarism detection platform that combines **lexical similarity** and **semantic similarity** to identify potentially copied content in text and documents.

The system supports **TXT, PDF, and DOCX files**, provides sentence-level matching, and uses AI-powered sentence embeddings to detect plagiarism even when the wording has been changed.

---

## 🚀 Features

### 📄 Multiple Input Formats

* Paste text directly into the application
* Upload `.txt` files
* Upload `.pdf` documents
* Upload `.docx` documents

### 🤖 AI-Based Semantic Detection

Uses **Sentence Transformers** to understand the meaning of sentences rather than relying only on exact word matching.

This allows the system to identify cases such as:

> "Artificial intelligence is transforming modern healthcare."

and

> "AI is changing the way healthcare is delivered."

even though the wording is different.

### 📊 Hybrid Similarity Analysis

The plagiarism score combines:

* **Semantic similarity — 65%**
* **Lexical similarity — 35%**

This provides a more reliable result than using only keyword or string matching.

### 🔎 Sentence-Level Matching

The system identifies potentially similar sentences and displays matching content to help users understand where similarity occurs.

### 🗂️ Corpus-Wide Detection

Documents can be compared against a stored document corpus using vector similarity search.

### 👤 User Authentication

The application provides:

* User registration
* Login
* JWT-based authentication
* Protected plagiarism analysis
* Analysis history

### 📈 Analysis Dashboard

The dashboard displays:

* Overall plagiarism score
* Semantic similarity
* Lexical similarity
* Matching sentences
* Risk level
* Document information
* Previous analysis history

### 🐳 Dockerized Architecture

The complete application can be started using Docker Compose.

The project consists of:

* React frontend
* Spring Boot backend
* FastAPI AI service
* PostgreSQL + pgvector database

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │     Vite Frontend    │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │   Spring Boot API    │
                         │      Backend         │
                         └───────┬────────┬─────┘
                                 │        │
                       Database  │        │ AI Requests
                                 │        │
                                 ▼        ▼
                    ┌───────────────┐  ┌─────────────────┐
                    │ PostgreSQL +  │  │ FastAPI AI      │
                    │   pgvector    │  │ Microservice    │
                    └───────────────┘  └────────┬────────┘
                                                │
                                                ▼
                                     ┌────────────────────┐
                                     │ Sentence           │
                                     │ Transformers      │
                                     │ all-MiniLM-L6-v2   │
                                     └────────────────────┘
```

---

# 🛠️ Tech Stack

## Frontend

* React.js
* Vite
* JavaScript
* HTML5
* CSS3
* Axios

## Backend

* Java 21
* Spring Boot
* Spring Web
* Spring Data JPA
* Spring Security
* JWT Authentication
* Maven

## AI / Machine Learning

* Python
* FastAPI
* Sentence Transformers
* `all-MiniLM-L6-v2`
* Scikit-learn
* TF-IDF
* Cosine Similarity
* Vector Embeddings
* NLP

## Database

* PostgreSQL
* pgvector
* SQL

## Document Processing

* PyMuPDF
* python-docx
* TXT processing

## DevOps

* Docker
* Docker Compose
* GitHub Actions

---

# 🧠 How Plagiarism Detection Works

The system uses a hybrid approach combining **lexical** and **semantic** similarity.

## 1. Document Upload

The user either:

* pastes text into the application, or
* uploads a TXT, PDF, or DOCX document.

---

## 2. Text Extraction

The AI service extracts readable text from the uploaded document.

```text
PDF / DOCX / TXT
       ↓
Text Extraction
       ↓
Clean Text
```

---

## 3. Text Preprocessing

The extracted text is cleaned and divided into sentences.

Typical preprocessing includes:

* Removing unnecessary whitespace
* Sentence segmentation
* Normalization
* Preparing text for similarity analysis

---

## 4. Lexical Similarity

TF-IDF is used to represent the text based on word importance.

Cosine similarity is then calculated between documents/sentences.

```text
Text
 ↓
TF-IDF
 ↓
Vector Representation
 ↓
Cosine Similarity
 ↓
Lexical Similarity Score
```

Lexical similarity is useful when copied content contains similar or identical wording.

---

## 5. Semantic Similarity

The system uses the Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

Sentences are converted into numerical vectors called **embeddings**.

```text
Sentence
   ↓
Sentence Transformer
   ↓
Embedding Vector
   ↓
Vector Similarity
   ↓
Semantic Similarity Score
```

This allows the system to detect similarity even when the wording has been changed.

---

## 6. Combined Plagiarism Score

The final score uses a weighted combination of the two approaches:

```text
Final Score =
    (Semantic Similarity × 0.65)
  + (Lexical Similarity × 0.35)
```

The resulting score is used to determine the potential plagiarism/risk level.

---

# 📂 Project Structure

```text
plagiarism-detector/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── ai-service/
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── similarity.py
│   │   ├── text_extraction.py
│   │   └── vector_store.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── backend/
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       └── resources/
│   │
│   ├── pom.xml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
│
├── db/
│   └── init.sql
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# ⚙️ Prerequisites

Before running the project, install:

* Git
* Docker Desktop
* Docker Compose

You do **not** need to install Java, Python, Node.js, or PostgreSQL separately when running the complete application through Docker Compose.

---

# 🐳 Running the Application with Docker

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/plagiarism-detector.git
```

Move into the project directory:

```bash
cd plagiarism-detector
```

---

## 2. Configure Environment Variables

Create your environment file from the example:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Update the `.env` file with your local configuration.

**Never commit `.env` to GitHub.**

---

## 3. Start the Application

Run:

```bash
docker compose up --build
```

Docker Compose will start:

```text
PostgreSQL + pgvector
        ↓
FastAPI AI Service
        ↓
Spring Boot Backend
        ↓
React Frontend
```

---

## 4. Access the Application

Once all containers are running:

| Service         | URL                        |
| --------------- | -------------------------- |
| Frontend        | http://localhost:5173      |
| Backend         | http://localhost:8080      |
| AI Service      | http://localhost:8000      |
| FastAPI Swagger | http://localhost:8000/docs |

Open the frontend:

```text
http://localhost:5173
```

---

# 🔧 Useful Docker Commands

### Check running containers

```bash
docker compose ps
```

### View all logs

```bash
docker compose logs
```

### View AI service logs

```bash
docker compose logs ai-service
```

### View backend logs

```bash
docker compose logs backend
```

### View database logs

```bash
docker compose logs db
```

### Stop the application

```bash
docker compose down
```

### Rebuild containers

```bash
docker compose up --build
```

### Stop and remove database volume

⚠️ This deletes the PostgreSQL data stored in the Docker volume.

```bash
docker compose down -v
```

---

# 🔌 API Overview

## Authentication

### Register

```http
POST /api/auth/register
```

Creates a new user account.

### Login

```http
POST /api/auth/login
```

Authenticates the user and returns a JWT token.

---

## Plagiarism Analysis

### Analyze Text

```http
POST /api/plagiarism/analyze
```

Analyzes submitted content and returns similarity information.

### Analyze File

```http
POST /api/plagiarism/analyze-file
```

Accepts supported document formats such as:

```text
.txt
.pdf
.docx
```

### Analysis History

```http
GET /api/plagiarism/history
```

Returns previous plagiarism analyses for the authenticated user.

---

# 🤖 AI Service

The FastAPI service handles the machine-learning operations.

Main responsibilities include:

```text
Document
   ↓
Text Extraction
   ↓
Sentence Processing
   ↓
TF-IDF Analysis
   +
Sentence Embeddings
   ↓
Similarity Calculation
   ↓
Plagiarism Result
```

The AI service uses:

```text
Sentence Transformers
        +
Scikit-learn
        +
PostgreSQL / pgvector
```

---

# 🗄️ Database

The project uses **PostgreSQL with pgvector**.

PostgreSQL stores application data such as:

* Users
* Documents
* Analysis results
* Similarity information
* Analysis history

The `pgvector` extension enables vector storage and similarity search for document embeddings.

---

# 🔐 Security

The application uses:

* JWT authentication
* Environment variables for configuration
* Password hashing
* Protected backend APIs
* Docker network isolation between services

### Important

Never commit secrets such as:

```text
.env
JWT secrets
Database passwords
API keys
Access tokens
```

The repository should contain:

```text
.env.example
```

instead of your real `.env`.

---

# 🧪 Testing

Run the application using Docker Compose:

```bash
docker compose up --build
```

Verify that all services are running:

```bash
docker compose ps
```

Test the FastAPI documentation:

```text
http://localhost:8000/docs
```

Then test the complete flow from the frontend:

```text
Register
   ↓
Login
   ↓
Upload / Enter Text
   ↓
Run Analysis
   ↓
Calculate Similarity
   ↓
Display Plagiarism Report
   ↓
Save Analysis History
```

---

# 📊 Example Result

A plagiarism analysis can provide information such as:

```text
---------------------------------------
        PLAGIARISM ANALYSIS
---------------------------------------

Overall Similarity : 78%

Semantic Similarity : 82%
Lexical Similarity  : 71%

Risk Level          : High

Matching Sentences  : 12
---------------------------------------
```

> The similarity score is an automated indication of textual similarity and should not be treated as definitive proof of plagiarism.

---

# 🎯 Use Cases

This system can be used for:

* Academic assignments
* Student submissions
* Research documents
* Articles
* Technical documentation
* Content verification
* Internal document comparison
* Duplicate-content detection

---

# 🌟 Why This Project Is Different

Traditional plagiarism checkers often rely heavily on exact word or phrase matching.

This project combines:

```text
Lexical Similarity
        +
Semantic Similarity
        +
Sentence-Level Matching
        +
Vector Search
```

This makes the system capable of detecting **meaning-level similarity**, including content that has been rephrased.

---

# 🚧 Future Improvements

Potential improvements include:

* 🌐 Web-wide plagiarism detection
* 📚 Larger document corpus
* 🔗 Source URL identification
* 📑 Side-by-side document comparison
* 📈 Advanced analytics dashboard
* 🌍 Multilingual plagiarism detection
* 🧠 Fine-tuned transformer models
* ⚡ Asynchronous document processing
* ☁️ Cloud deployment
* 📦 Redis-based caching
* 🔄 Kafka-based processing pipeline
* 📊 Advanced reporting and PDF export

---

# 👩‍💻 Author

**Vanshika Srivastava**


---

# 📜 License

This project is intended for educational and portfolio purposes.

Add an appropriate open-source license before distributing the project publicly.
