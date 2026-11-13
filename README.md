# JOBSEEKER — Full-Stack MERN Job Portal & ATS

A full-stack MERN (MongoDB, Express.js, React, Node.js) job aggregation and applicant tracking platform converted from the original Python/Flask `JOBSEEKER` architecture.

## Features
- **Role-Based Authentication (JWT):** Separate workflows for **Candidates** and **Recruiters** with `bcrypt` password hashing and protected API routes.
- **Hybrid Job Board:** Browse internal recruiter-posted jobs stored in MongoDB alongside live external job search integration (JSearch / RapidAPI with smart fallback).
- **Candidate Workflow:** Search & filter jobs by keyword, location, and job type; bookmark/save jobs; apply with a resume URL or uploaded PDF file; track application statuses (`Applied`, `Shortlisted`, `Interview`, `Rejected`).
- **Recruiter Workflow:** Post new job openings, manage active listings, review candidate applications, inspect resumes, and update candidate hiring stages.

## Project Structure
```text
JOBSEEKER-MERN/
├── client/                 # React + Vite + Tailwind CSS frontend
│   └── src/
│       ├── api/            # Axios client with JWT interceptors
│       ├── components/     # Navbar, JobCard, ProtectedRoute
│       ├── context/        # AuthContext (user & token state)
│       └── pages/          # Home, Jobs, JobDetail, SavedJobs, Dashboard, Login, Register
└── server/                 # Node.js + Express + MongoDB backend
    ├── config/             # MongoDB connection
    ├── controllers/        # Auth, Job, Application, SavedJob controllers
    ├── middleware/         # JWT auth, role guard, Multer PDF upload, error handler
    ├── models/             # User, Company, Job, Application, SavedJob schemas
    ├── routes/             # Express REST API routers
    ├── services/           # External RapidAPI job aggregator service
    └── seed.js             # Database seeder with demo accounts & sample jobs
```

## Quick Start

### 1. Backend Setup (`server/`)
```bash
cd server
npm install
cp .env.example .env
# Edit .env with your MONGO_URI and JWT_SECRET
npm run seed    # Optional: populates demo users & jobs
npm run dev     # Starts Express API on http://localhost:5000
```

### 2. Frontend Setup (`client/`)
```bash
cd client
npm install
npm run dev     # Starts React app on http://localhost:5173
```

## Demo Credentials (after running `npm run seed`)
- **Candidate:** `candidate@demo.com` / `Password123!`
- **Recruiter:** `recruiter@demo.com` / `Password123!`
