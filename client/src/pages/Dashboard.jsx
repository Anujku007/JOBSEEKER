import { useEffect, useState } from 'react';
import { PlusCircle, Trash2, Users } from 'lucide-react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [myJobs, setMyJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [applicants, setApplicants] = useState([]);
  const [form, setForm] = useState({
    title: '',
    companyName: user?.company?.name || '',
    location: '',
    jobType: 'Full-Time',
    salaryRange: '',
    skillsRequired: '',
    description: '',
  });

  useEffect(() => {
    if (user?.role === 'candidate') {
      api.get('/applications/mine').then(({ data }) => setApplications(data));
    } else if (user?.role === 'recruiter') {
      api.get('/jobs/recruiter/mine').then(({ data }) => setMyJobs(data));
    }
  }, [user]);

  const handleCreateJob = async (e) => {
    e.preventDefault();
    const { data } = await api.post('/jobs', form);
    setMyJobs([data, ...myJobs]);
    setForm({
      title: '',
      companyName: user?.company?.name || '',
      location: '',
      jobType: 'Full-Time',
      salaryRange: '',
      skillsRequired: '',
      description: '',
    });
  };

  const handleDeleteJob = async (jobId) => {
    await api.delete(`/jobs/${jobId}`);
    setMyJobs(myJobs.filter((j) => j._id !== jobId));
    if (selectedJobId === jobId) {
      setSelectedJobId(null);
      setApplicants([]);
    }
  };

  const handleInspectApplicants = async (jobId) => {
    setSelectedJobId(jobId);
    const { data } = await api.get(`/applications/job/${jobId}`);
    setApplicants(data);
  };

  const handleStatusChange = async (appId, status) => {
    const { data } = await api.patch(`/applications/${appId}/status`, { status });
    setApplicants((prev) => prev.map((a) => (a._id === appId ? { ...a, status: data.status } : a)));
  };

  if (user?.role === 'candidate') {
    return (
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">My Applications ({applications.length})</h1>
        {applications.length === 0 ? (
          <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500">
            No applications submitted yet.
          </div>
        ) : (
          <div className="space-y-4">
            {applications.map((app) => (
              <div
                key={app._id}
                className="bg-white p-5 rounded-xl border border-slate-200 flex flex-wrap items-center justify-between gap-4"
              >
                <div>
                  <h3 className="font-bold text-slate-900">{app.job?.title || 'Role Removed'}</h3>
                  <p className="text-sm text-slate-600">
                    {app.job?.companyName} • {app.job?.location}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    Applied on {new Date(app.createdAt).toLocaleDateString()}
                  </p>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700">
                  {app.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 grid lg:grid-cols-3 gap-8">
      <div className="bg-white p-6 rounded-xl border border-slate-200 h-fit">
        <h2 className="font-bold text-lg flex items-center gap-2 mb-4">
          <PlusCircle className="w-5 h-5 text-indigo-600" /> Post New Opening
        </h2>
        <form onSubmit={handleCreateJob} className="space-y-3 text-sm">
          <input
            required
            placeholder="Job Title (e.g. Full-Stack Engineer)"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <input
            required
            placeholder="Company Name"
            value={form.companyName}
            onChange={(e) => setForm({ ...form, companyName: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <input
            required
            placeholder="Location (e.g. Bengaluru / Remote)"
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <select
            value={form.jobType}
            onChange={(e) => setForm({ ...form, jobType: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white"
          >
            <option value="Full-Time">Full-Time</option>
            <option value="Remote">Remote</option>
            <option value="Internship">Internship</option>
            <option value="Contract">Contract</option>
          </select>
          <input
            placeholder="Salary Range (e.g. ₹10L - ₹15L)"
            value={form.salaryRange}
            onChange={(e) => setForm({ ...form, salaryRange: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <input
            placeholder="Skills (comma-separated: React, Node, MongoDB)"
            value={form.skillsRequired}
            onChange={(e) => setForm({ ...form, skillsRequired: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <textarea
            required
            rows="4"
            placeholder="Job responsibilities and requirements..."
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg"
          />
          <button
            type="submit"
            className="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700"
          >
            Publish Job
          </button>
        </form>
      </div>

      <div className="lg:col-span-2 space-y-6">
        <div>
          <h2 className="text-xl font-bold mb-4">Your Posted Jobs ({myJobs.length})</h2>
          <div className="space-y-3">
            {myJobs.map((job) => (
              <div
                key={job._id}
                className="bg-white p-4 rounded-xl border border-slate-200 flex items-center justify-between gap-4"
              >
                <div>
                  <h3 className="font-bold text-slate-900">{job.title}</h3>
                  <p className="text-xs text-slate-500">
                    {job.location} • {job.jobType}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleInspectApplicants(job._id)}
                    className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-50 text-indigo-700 hover:bg-indigo-100"
                  >
                    <Users className="w-3.5 h-3.5" /> Applicants
                  </button>
                  <button
                    onClick={() => handleDeleteJob(job._id)}
                    className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {selectedJobId && (
          <div className="bg-white p-6 rounded-xl border border-slate-200">
            <h3 className="font-bold text-lg mb-4">Applicants ({applicants.length})</h3>
            {applicants.length === 0 ? (
              <p className="text-sm text-slate-500">No candidates have applied to this role yet.</p>
            ) : (
              <div className="space-y-4">
                {applicants.map((app) => (
                  <div
                    key={app._id}
                    className="p-4 border border-slate-200 rounded-lg flex flex-wrap items-center justify-between gap-4"
                  >
                    <div>
                      <p className="font-semibold text-slate-900">{app.candidate?.name}</p>
                      <p className="text-xs text-slate-500">{app.candidate?.email}</p>
                      <a
                        href={app.resumeUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-block mt-1 text-xs font-semibold text-indigo-600 underline"
                      >
                        Open Resume
                      </a>
                    </div>
                    <select
                      value={app.status}
                      onChange={(e) => handleStatusChange(app._id, e.target.value)}
                      className="px-3 py-1.5 border border-slate-300 rounded-lg text-xs font-semibold bg-white"
                    >
                      <option value="Applied">Applied</option>
                      <option value="Shortlisted">Shortlisted</option>
                      <option value="Interview">Interview</option>
                      <option value="Offered">Offered</option>
                      <option value="Rejected">Rejected</option>
                    </select>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
