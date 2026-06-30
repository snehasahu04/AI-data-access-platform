🔐 AI Data Access Provisioning Platform
📌 Overview

The AI Data Access Provisioning Platform is an enterprise-grade governance system that automates and manages data access requests using AI-driven validation, approval workflows, and policy-based governance.

It provides a centralized system for:

Requesting data access
Automated AI-based validation
Multi-level approval workflows
Audit tracking and governance
Dashboard-based monitoring


🚀 Key Features

👤 User and role-based access management
📩 Data access request lifecycle management
🤖 AI-powered request intent analysis
✅ Multi-level approval workflow system
📊 Dataset catalog management
🔍 Governance and compliance enforcement
📈 Analytics dashboard for insights
🧾 Audit logging for all actions
🔁 Workflow automation using n8n


🏗️ System Architecture

Frontend (Streamlit Dashboard)
        ↓
Backend (FastAPI)
        ↓
Service Layer (Business Logic)
        ↓
AI Request Engine (Intent + Validation)
        ↓
Database Layer (ORM Models + SQL)
        ↓
External Automation (n8n Workflows)


📁 Project Structure

data-access-platform/
│
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/          # API Routes (users, requests, approvals, catalog, AI)
│   │   ├── models/       # ORM database models
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # Business logic layer
│   │   ├── database/     # DB connection & migrations
│   │   ├── config.py
│   │   ├── main.py
│   │   └── utils.py
│
├── dashboard/            # Streamlit UI
│   ├── pages/            # UI pages (requests, approvals, analytics)
│   └── app.py
│
├── docs/                 # System documentation
├── n8n-workflows/        # Automation workflows (JSON)
├── scripts/              # DB scripts & seed data
├── sample-data/
├── backend/requirements.txt
├── .github/workflows/ci.yml


🛠️ Tech Stack

Backend
FastAPI
Python
SQLAlchemy
Pydantic
Uvicorn
Frontend
Streamlit
AI & Automation
AI request intent engine
n8n workflow automation
Database
SQL-based ORM architecture
DevOps


GitHub Actions (CI pipeline)

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/data-access-platform.git
cd data-access-platform

2️⃣ Setup backend environment
cd backend
pip install -r requirements.txt

3️⃣ Run backend server
uvicorn app.main:app --reload

4️⃣ Run dashboard
cd dashboard
streamlit run app.py

📡 API Endpoints
Module	Endpoint
Users	/users
Requests	/requests
Approvals	/approvals
Catalog	/catalog
AI Requests	/ai_requests
📊 Dashboard Modules
📋 Access Requests
✅ Approval Management
📈 Analytics & Insights
🔍 Governance Monitoring
🔁 Workflow Automation

The system integrates n8n workflows for:

Access request automation
Approval escalation flows
Enterprise governance workflows
Notification handling
🧠 AI Capabilities
Request intent classification
Automated validation of access requests
Smart routing to approvers
Governance rule enforcement
🧪 Testing

Run backend tests:

pytest backend/tests
📌 Use Case

This platform is designed for enterprises where:

Data access must be controlled
Compliance is critical
Approvals are required before granting access
Audit trails are mandatory

👨‍💻 Author
Sneha Sahu

🚀 Future Improvements
Role-Based Access Control (RBAC)
Snowflake / cloud data integration
Real-time audit dashboard
AI recommendation engine for approvals
Advanced security policies

