import { useEffect, useState } from 'react';
import { Search } from 'lucide-react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import JobCard from '../components/JobCard';

export default function Jobs() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [externalJobs, setExternalJobs] = useState([]);
  const [savedIds, setSavedIds] = useState(new Set());
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [jobType, setJobType] = useState('All');
  const [includeExternal, setIncludeExternal] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/jobs', {
        params: { keyword, location, jobType, includeExternal },
      });
      setJobs(data.jobs);
      setExternalJobs(data.externalJobs || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSaved = async () => {
    if (user?.role !== 'candidate') return;
    try {
      const { data } = await api.get('/saved');
      setSavedIds(new Set(data.map((s) => s.job._id)));
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchJobs();
    fetchSaved();
  }, [user]);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchJobs();
  };

  const handleToggleSave = async (jobId) => {
    try {
      const { data } = await api.post(`/saved/${jobId}`);
      setSavedIds((prev) => {
        const next = new Set(prev);
        if (data.saved) next.add(jobId);
        else next.delete(jobId);
        return next;
      });
    } catch (err) {
      alert(err.response?.data?.message || 'Unable to save job');
    }
  };

  const allJobs = [...jobs, ...externalJobs];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <form
        onSubmit={handleSearch}
        className="bg-white p-4 rounded-xl border border-slate-200 grid md:grid-cols-4 gap-3 mb-8"
      >
        <input
          type="text"
          placeholder="Title, skill, or company..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          className="px-3 py-2 border border-slate-300 rounded-lg text-sm"
        />
        <input
          type="text"
          placeholder="Location (e.g. Bengaluru, Remote)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="px-3 py-2 border border-slate-300 rounded-lg text-sm"
        />
        <select
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
          className="px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white"
        >
          <option value="All">All Job Types</option>
          <option value="Full-Time">Full-Time</option>
          <option value="Remote">Remote</option>
          <option value="Internship">Internship</option>
          <option value="Contract">Contract</option>
        </select>
        <button
          type="submit"
          className="flex items-center justify-center gap-2 bg-indigo-600 text-white rounded-lg px-4 py-2 text-sm font-semibold hover:bg-indigo-700"
        >
          <Search className="w-4 h-4" /> Search
        </button>

        <label className="md:col-span-4 flex items-center gap-2 text-xs text-slate-600 pt-1">
          <input
            type="checkbox"
            checked={includeExternal}
            onChange={(e) => setIncludeExternal(e.target.checked)}
          />
          Include aggregated external partner listings (RapidAPI feed)
        </label>
      </form>

      {loading ? (
        <div className="text-center py-12 text-slate-500">Loading opportunities...</div>
      ) : allJobs.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl border border-slate-200 text-slate-500">
          No jobs matched your filters.
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-5">
          {allJobs.map((job) => (
            <JobCard
              key={job._id}
              job={job}
              isSaved={savedIds.has(job._id)}
              onToggleSave={handleToggleSave}
              showSaveButton={user?.role === 'candidate'}
            />
          ))}
        </div>
      )}
    </div>
  );
}
