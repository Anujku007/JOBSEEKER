import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapPin, Building2, Briefcase, CheckCircle2 } from 'lucide-react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [job, setJob] = useState(null);
  const [resumeUrl, setResumeUrl] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [coverLetter, setCoverLetter] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [applied, setApplied] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`/jobs/${id}`).then(({ data }) => setJob(data)).catch(() => navigate('/jobs'));
  }, [id, navigate]);

  useEffect(() => {
    if (user?.resumeUrl) setResumeUrl(user.resumeUrl);
  }, [user]);

  const handleApply = async (e) => {
    e.preventDefault();
    if (!user) return navigate('/login');
    setSubmitting(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('jobId', id);
      formData.append('resumeUrl', resumeUrl);
      formData.append('coverLetter', coverLetter);
      if (resumeFile) {
        formData.append('resume', resumeFile);
      }

      await api.post('/applications', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setApplied(true);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit application');
    } finally {
      setSubmitting(false);
    }
  };

  if (!job) return <div className="p-10 text-center text-slate-500">Loading job details...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 grid md:grid-cols-3 gap-6">
      <div className="md:col-span-2 bg-white p-6 rounded-xl border border-slate-200">
        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700">
          {job.jobType}
        </span>
        <h1 className="text-2xl font-bold text-slate-900 mt-3">{job.title}</h1>
        <div className="flex flex-wrap gap-4 text-sm text-slate-600 mt-2">
          <span className="flex items-center gap-1">
            <Building2 className="w-4 h-4" /> {job.companyName}
          </span>
          <span className="flex items-center gap-1">
            <MapPin className="w-4 h-4" /> {job.location}
          </span>
          <span className="flex items-center gap-1">
            <Briefcase className="w-4 h-4" /> {job.salaryRange}
          </span>
        </div>

        <hr className="my-5 border-slate-200" />

        <h2 className="font-semibold text-slate-900 mb-2">Role Description</h2>
        <p className="text-sm text-slate-700 whitespace-pre-line leading-relaxed">{job.description}</p>

        {job.skillsRequired?.length > 0 && (
          <div className="mt-6">
            <h3 className="font-semibold text-slate-900 mb-2">Required Skills</h3>
            <div className="flex flex-wrap gap-2">
              {job.skillsRequired.map((s, idx) => (
                <span key={idx} className="text-xs px-2.5 py-1 bg-slate-100 rounded-md font-medium">
                  {s}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 h-fit">
        <h2 className="font-bold text-lg mb-3">Apply for this Role</h2>

        {applied ? (
          <div className="p-4 bg-emerald-50 text-emerald-800 rounded-lg text-sm flex items-start gap-2">
            <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Application Submitted!</p>
              <p className="mt-1">Track your status anytime from your Candidate Dashboard.</p>
            </div>
          </div>
        ) : user?.role === 'recruiter' ? (
          <p className="text-sm text-slate-500">
            You are logged in as a recruiter. Switch to a candidate account to apply.
          </p>
        ) : (
          <form onSubmit={handleApply} className="space-y-4">
            {error && <div className="p-2.5 bg-rose-50 text-rose-700 text-xs rounded-lg">{error}</div>}

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Resume Link (Drive / LinkedIn / Portfolio)
              </label>
              <input
                type="url"
                placeholder="https://..."
                value={resumeUrl}
                onChange={(e) => setResumeUrl(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Or Upload PDF/DOCX Resume
              </label>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(e) => setResumeFile(e.target.files[0])}
                className="w-full text-xs text-slate-600"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Cover Note (Optional)
              </label>
              <textarea
                rows="3"
                placeholder="Briefly highlight relevant projects or experience..."
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : user ? 'Submit Application' : 'Log In to Apply'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
