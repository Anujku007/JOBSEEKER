# JOBSEEKER — Full-Stack MERN Job Portal & ATS Platform

![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Express.js](https://img.shields.io/badge/Express.js-REST%20API-000000?style=for-the-badge&logo=express&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-Backend-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**JOBSEEKER** is a full-stack **MERN (MongoDB, Express.js, React, Node.js)** career discovery and Applicant Tracking System (ATS) engineered to unify direct recruiter hiring with external job aggregation.

---

## Key Features

### Candidate Experience
* **Hybrid Job Discovery:** Search and filter internal recruiter postings by keyword, location, and employment type (`Full-Time`, `Remote`, `Internship`, `Contract`), or toggle on the external partner feed (RapidAPI JSearch) to pull live openings into a single unified feed.
* **Bookmarking & Saved Jobs:** Save and manage bookmarked opportunities via a dedicated `SavedJobs` collection.
* **Flexible Application Flow:** Apply to roles using a hosted resume link (Google Drive, LinkedIn, Portfolio) or upload a `.pdf`, `.doc`, or `.docx` file handled via Multer.
* **Live Application Tracker:** Monitor real-time hiring stage updates (`Applied` → `Shortlisted` → `Interview` → `Offered` / `Rejected`) from a personal candidate dashboard.

### Recruiter Experience (ATS Pipeline)
* **Role-Based Access Control (RBAC):** Protected behind JWT authentication and `authorize('recruiter')` middleware so only recruiter accounts can publish or manage job openings.
* **Job & Applicant Management:** Publish new roles, inspect candidate profiles, open submitted resumes in one click, and advance applicants across hiring stages in real time.

### Security & Database Architecture
* **Authentication:** Stateless JWT authentication paired with `bcryptjs` password hashing and automatic Axios request interceptors.
* **Database Integrity:** Five Mongoose models (`User`, `Company`, `Job`, `Application`, `SavedJob`) featuring full-text search indexes on job listings and compound unique indexes (`{ job, candidate }`) to enforce idempotent applications at the database level.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, React Router v6, Tailwind CSS, Lucide Icons, Axios |
| **Backend** | Node.js, Express.js, JSON Web Tokens (JWT), Bcrypt.js, Multer |
| **Database** | MongoDB Atlas, Mongoose ODM |
| **External Integration** | RapidAPI JSearch API (with automatic fallback feed) |

---

## Project Structure

```text
JOBSEEKER-MERN/
├── client/                         # React + Vite + Tailwind CSS Frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js              # Dev server & /api + /uploads proxy
│   └── src/
│       ├── api/
│       │   └── axios.js            # Axios instance with JWT interceptor
│       ├── components/
│       │   ├── JobCard.jsx         # Job card with bookmark & external link support
│       │   ├── Navbar.jsx          # Role-aware navigation bar
│       │   └── ProtectedRoute.jsx  # Auth & role route guard
│       ├── context/
│       │   └── AuthContext.jsx     # Global auth state & token persistence
│       └── pages/
│           ├── Home.jsx            # Landing page
│           ├── Jobs.jsx            # Multi-filter job board + external toggle
│           ├── JobDetail.jsx       # Role details & URL/PDF application form
│           ├── SavedJobs.jsx       # Candidate bookmarked jobs
│           ├── Dashboard.jsx       # Candidate tracker & Recruiter ATS workspace
│           ├── Profile.jsx         # User profile & default resume settings
│           ├── Login.jsx           # Login with one-click demo credential fill
│           └── Register.jsx        # Candidate / Recruiter registration
│
└── server/                         # Node.js + Express + MongoDB Backend
    ├── config/
    │   └── db.js                   # MongoDB Atlas connection handler
    ├── controllers/
    │   ├── authController.js       # Register, login, profile updates
    │   ├── jobController.js        # Job CRUD, search/pagination, recruiter listings
    │   ├── applicationController.js# Apply, candidate history, ATS status updates
    │   └── savedJobController.js   # Toggle & fetch saved jobs
    ├── middleware/
    │   ├── authMiddleware.js       # JWT verification & role authorization
    │   └── uploadMiddleware.js     # Multer PDF/DOCX validation & disk storage
    ├── models/
    │   ├── User.js
    │   ├── Company.js
    │   ├── Job.js
    │   ├── Application.js
    │   └── SavedJob.js
    ├── routes/
    │   ├── authRoutes.js
    │   ├── jobRoutes.js
    │   ├── applicationRoutes.js
    │   └── savedRoutes.js
    ├── services/
    │   └── externalJobService.js   # RapidAPI JSearch client with fallback
    ├── seed.js                     # Database seeder for demo accounts & jobs
    ├── server.js                   # Express app entry point & error handler
    └── .env.example                # Environment variable template
```

---

## Local Setup & Installation

### Prerequisites
* Node.js (v18+ recommended)
* MongoDB Atlas cluster (or local MongoDB instance)

### 1. Clone the Repository
```bash
git clone [https://github.com/Anujku007/JOBSEEKER.git](https://github.com/Anujku007/JOBSEEKER.git)
cd JOBSEEKER
```

### 2. Backend Setup (`server/`)
```bash
cd server
npm install
cp .env.example .env
```

Update `server/.env` with your credentials:
```env
PORT=5000
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/jobseeker_mern?retryWrites=true&w=majority
JWT_SECRET=your_super_secret_jwt_key
JWT_EXPIRES_IN=7d
CLIENT_URL=http://localhost:5173
RAPIDAPI_KEY=your_rapidapi_jsearch_key_optional
RAPIDAPI_HOST=jsearch.p.rapidapi.com
```

Seed the database with demo users and sample jobs, then start the API server:
```bash
npm run seed
npm run dev
```
The Express API will run on `http://localhost:5000`.

### 3. Frontend Setup (`client/`)
Open a new terminal window:
```bash
cd client
npm install
npm run dev
```
The React application will run on `http://localhost:5173`.

---

## Demo Credentials

After running `npm run seed`, use either account (or click the **Fill Demo Candidate / Recruiter** buttons on the Login page):

| Role | Email | Password |
| :--- | :--- | :--- |
| **Candidate** | `candidate@demo.com` | `Password123!` |
| **Recruiter** | `recruiter@demo.com` | `Password123!` |

---

## REST API Endpoints

### Authentication & Profile (`/api/auth`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Public | Register a new Candidate or Recruiter |
| `POST` | `/api/auth/login` | Public | Authenticate user and return JWT |
| `GET` | `/api/auth/me` | Private | Get logged-in user profile |
| `PUT` | `/api/auth/profile` | Private | Update profile details & default resume |

### Jobs (`/api/jobs`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/jobs` | Public | Search & filter jobs (`keyword`, `location`, `jobType`, `includeExternal`) |
| `GET` | `/api/jobs/:id` | Public | Get single job details |
| `GET` | `/api/jobs/recruiter/mine` | Recruiter | List jobs posted by the logged-in recruiter |
| `POST` | `/api/jobs` | Recruiter | Publish a new job opening |
| `DELETE` | `/api/jobs/:id` | Recruiter | Delete a job opening |

### Applications (`/api/applications`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/applications` | Candidate | Submit job application (URL or PDF/DOCX file) |
| `GET` | `/api/applications/mine` | Candidate | View submitted applications and statuses |
| `GET` | `/api/applications/job/:jobId` | Recruiter | View all applicants for a specific job |
| `PATCH` | `/api/applications/:id/status` | Recruiter | Update candidate hiring stage |

### Saved Jobs (`/api/saved`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/saved` | Candidate | Retrieve all bookmarked jobs |
| `POST` | `/api/saved/:jobId` | Candidate | Bookmark or unbookmark a job |

---

## Author

**Anuj Kumar**
* LinkedIn: [linkedin.com/in/anuj-kumar-836680298](https://linkedin.com/in/anuj-kumar-836680298)
* GitHub: [github.com/Anujku007](https://github.com/Anujku007)
* LeetCode: [leetcode.com/u/Anuj_kumar0007](https://leetcode.com/u/Anuj_kumar0007/)