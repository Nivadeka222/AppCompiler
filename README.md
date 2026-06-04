# 🚀 AI App Compiler

Transform natural language application ideas into structured software architecture using Large Language Models.

AI App Compiler is a multi-stage AI pipeline that converts a simple application description into:

* 📋 Intent Specification
* 🏗️ System Design
* 🗄️ Database Schema
* 🔌 API Schema
* 🎨 UI Schema
* 🔐 Authentication Schema
* ✅ Validation Reports

---

## Example

### Input

```text
Build an e-commerce platform with products,
carts, orders, payments and an admin dashboard.
```

### Generated Output

```text
intent.json
design.json
db_schema.json
api_schema.json
ui_schema.json
auth_schema.json
app_config.json
```

---

# Architecture

```text
Natural Language Prompt
          │
          ▼
Stage 1: Intent Extraction
          │
          ▼
Stage 2: System Design
          │
          ▼
Stage 3A: Database Schema
Stage 3B: API Schema
Stage 3C: UI Schema
Stage 3D: Auth Schema
          │
          ▼
Stage 4: Validation
          │
          ▼
Stage 5: Repair Engine
          │
          ▼
Final App Configuration
```

---

# Features

## Stage 1 — Intent Extraction

Extracts:

* Application type
* Entities
* Features
* User roles
* Integrations
* Assumptions

### Example

```json
{
  "app_name": "CRM Application",
  "app_type": "Customer Relationship Management",
  "features": [
    "Authentication",
    "Contact Management",
    "Analytics Dashboard"
  ]
}
```

---

## Stage 2 — System Design

Generates:

* Core entities
* Relationships
* Pages
* API groups
* User flows

---

## Stage 3 — Schema Generation

### Database Schema

Generates:

* Tables
* Fields
* Relationships
* Indexes

### API Schema

Generates:

* Endpoints
* Methods
* Request models
* Response models
* Authorization rules

### UI Schema

Generates:

* Pages
* Components
* Forms
* Navigation structure

### Auth Schema

Generates:

* Roles
* Permissions
* Public routes
* Access control policies

---

## Stage 4 — Validation

Validates:

* Schema consistency
* Cross-layer dependencies
* Structural correctness

---

## Stage 5 — Repair Engine

Automatically repairs malformed AI outputs and validation failures.

---

# Project Structure

```text
app-compiler/
│
├── pipeline.py
│
├── stages/
│   ├── stage1_intent.py
│   ├── stage2_system_design.py
│   ├── stage3_db_schema.py
│   ├── stage3_api_schema.py
│   ├── stage3_ui_schema.py
│   ├── stage3_auth_schema.py
│   ├── stage4_validator.py
│   └── stage5_repair.py
│
├── prompts/
│
├── schemas/
│   └── models.py
│
├── utils/
│
└── outputs/
```

---

# Tech Stack

* Python
* Pydantic
* Groq API
* Gemini API
* JSON
* Multi-Stage LLM Pipelines

---

# Running Locally

## Clone Repository

```bash
git clone <repo-url>
cd app-compiler
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
```

## Run

```bash
python pipeline.py
```

---

# Motivation

Software projects typically begin with vague requirements written in natural language.

This project explores whether LLMs can be orchestrated as a compiler pipeline that progressively transforms human intent into machine-readable software architecture.

Instead of generating code directly, the system first generates structured specifications that can later be used for code generation, deployment planning, or system design automation.

---

# Future Roadmap

* React Frontend
* FastAPI Backend
* OpenAPI Generation
* SQL Migration Generation
* Code Generation
* Multi-Agent Validation
* Deployment Blueprint Generation
* Visual Architecture Diagrams

---

# Author

Built by Niva Deka as an exploration of AI-powered software architecture generation and compiler-inspired LLM systems.
