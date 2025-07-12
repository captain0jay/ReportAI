Here’s a `README.md` for your **Blood Report AI Agent** project in Markdown format:

---

````markdown
# 🧬 Blood Report AI Agent

The **Blood Report AI Agent** is a scalable and fast AI-powered assistant that analyzes uploaded blood report PDFs and presents the findings in a user-friendly blog format. It uses an LLM backend, Redis for job queuing, and PostgreSQL for structured storage.

---

## 🚀 Features

- Upload PDF blood reports
- Queued background analysis using Redis
- Structured data stored in PostgreSQL
- LLM-based insights using Gemini
- Blog-style output for users
- Scalable microservice design

---

## 📦 Installation

```bash
pip install -r requirements.txt
````

---

## ▶️ How to Run

There are **two apps** in this system:

### 1. 🖥️ Frontend API

Run using:

```bash
python main.py
```

Or use hot-reloading (recommended during development):

```bash
uvicorn main:app --reload
```

### 2. 🧠 Background Processor

This listens to Redis for queued jobs and populates PostgreSQL with analyzed data.

Run it separately:

```bash
python processor.py
```

---

## 🔐 Environment Variables

Set these environment variables before running the application:

| Variable          | Description                    | Example / Default         |
| ----------------- | ------------------------------ | ------------------------- |
| `SELF_PORT`       | Port for the API               | `8000`                    |
| `REDIS_HOST`      | Redis server hostname          | `localhost`               |
| `REDIS_PORT`      | Redis server port              | `6379`                    |
| `REDIS_DB`        | Redis database index           | `0`                       |
| `PG_DB_URL`       | PostgreSQL database connection | `postgresql://...`        |
| `GEMINI_API_KEY`  | API key for Gemini LLM         | `your-api-key-here`       |
| `LLM_MODEL`       | Gemini model name              | `gemini/gemini-2.0-flash` |
| `LLM_TEMPERATURE` | LLM response creativity        | `0.7`                     |

---

## 🧭 Flow Diagram

![Blood Report AI Flow](./assets/flow-diagram.png)

> *Above: End-to-end system overview — from PDF upload, to Redis queue, to LLM analysis, to PostgreSQL, and final blog rendering.*

---

## 🧑‍💻 Host It Yourself

Want to self-host? Clone the repo and set the environment variables. You’ll need:

* Python 3.10+
* Redis
* PostgreSQL
* Gemini API access

```bash
git clone https://github.com/your-username/blood-report-ai.git
cd blood-report-ai
cp .env.example .env  # Then edit as needed
```

Then run the app as shown above.

---

## 🐞 Bugs Faced & Fixes

| Issue                    | Solution Description                                                    |
| ------------------------ | ----------------------------------------------------------------------- |
| Dependency installation  | Resolved conflicts by pinning versions in `requirements.txt`            |
| Syntax bugs              | Cleaned up parsing logic and fixed async/await inconsistencies          |
| Unstructured PDF content | Introduced intermediate extraction + cleaning layer                     |
| Redis queueing problems  | Ensured background processor reconnects and acknowledges jobs correctly |
| PostgreSQL integration   | Used SQLAlchemy with async drivers for performance and reliability      |
| Unnecessary imports      | Performed full lint and removed unused imports/modules                  |

---

> Built with ❤️ to help interpret complex medical data faster and more accessibly.

```

Let me know if you’d like me to generate the **flow diagram image**, or add badges (e.g., build status, license) or make a web version of this README.
```
