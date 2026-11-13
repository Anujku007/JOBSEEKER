import { useEffect, useState } from 'react';
import api from '../api/axios';
import JobCard from '../components/JobCard';

export default function SavedJobs() {
  const [savedItems, setSavedItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadSaved = async () => {
    try {
      const { data } = await api.get('/saved');
      setSavedItems(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSaved();
  }, []);

  const handleUnsave = async (jobId) => {
    await api.post(`/saved/${jobId}`);
    setSavedItems((prev) => prev.filter((item) => item.job._id !== jobId));
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Saved Opportunities</h1>
      {loading ? (
        <p className="text-slate-500">Loading saved jobs...</p>
      ) : savedItems.length === 0 ? (
        <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500">
          You have not bookmarked any jobs yet.
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-5">
          {savedItems.map(({ job }) => (
            <JobCard
              key={job._id}
              job={job}
              isSaved={true}
              onToggleSave={handleUnsave}
              showSaveButton={true}
            />
          ))}
        </div>
      )}
    </div>
  );
}
