import { Link } from 'react-router-dom';
import { Search, ShieldCheck, Layers } from 'lucide-react';

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-16">
      <div className="text-center max-w-3xl mx-auto">
        <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold uppercase tracking-wide">
          MERN Stack Career & ATS Platform
        </span>
        <h1 className="mt-4 text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
          Find Your Next Engineering Role or Hire Top Talent
        </h1>
        <p className="mt-4 text-lg text-slate-600">
          Search curated full-stack opportunities, aggregate external listings, and track every stage
          of your application pipeline in real time.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          <Link
            to="/jobs"
            className="px-6 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition"
          >
            Explore Open Roles
          </Link>
          <Link
            to="/register"
            className="px-6 py-3 rounded-xl bg-white border border-slate-300 text-slate-800 font-semibold hover:bg-slate-50 transition"
          >
            Create Account
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mt-20">
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <Search className="w-8 h-8 text-indigo-600 mb-3" />
          <h3 className="font-bold text-lg">Hybrid Job Discovery</h3>
          <p className="text-sm text-slate-600 mt-1">
            Filter direct recruiter postings alongside aggregated external tech openings in one unified feed.
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <Layers className="w-8 h-8 text-indigo-600 mb-3" />
          <h3 className="font-bold text-lg">Live Application Tracking</h3>
          <p className="text-sm text-slate-600 mt-1">
            Apply with a resume link or PDF upload and monitor real-time status updates from recruiters.
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <ShieldCheck className="w-8 h-8 text-indigo-600 mb-3" />
          <h3 className="font-bold text-lg">Recruiter ATS Pipeline</h3>
          <p className="text-sm text-slate-600 mt-1">
            Post openings, inspect candidate profiles and resumes, and advance applicants through interview stages.
          </p>
        </div>
      </div>
    </div>
  );
}
