import { useState } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user, setUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [headline, setHeadline] = useState(user?.headline || '');
  const [location, setLocation] = useState(user?.location || '');
  const [skills, setSkills] = useState((user?.skills || []).join(', '));
  const [resumeUrl, setResumeUrl] = useState(user?.resumeUrl || '');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { data } = await api.put('/auth/profile', {
      name,
      headline,
      location,
      skills,
      resumeUrl,
    });
    setUser(data);
    setMessage('Profile updated successfully.');
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="bg-white p-6 rounded-xl border border-slate-200">
        <h1 className="text-xl font-bold mb-1">Profile Settings</h1>
        <p className="text-xs text-slate-500 mb-5 capitalize">Account Role: {user?.role}</p>

        {message && (
          <div className="mb-4 p-3 rounded-lg bg-emerald-50 text-emerald-700 text-sm">{message}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <div>
            <label className="block font-semibold mb-1">Full Name</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Professional Headline</label>
            <input
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              placeholder="e.g. Full-Stack MERN Developer"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Location</label>
            <input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Skills (comma-separated)</label>
            <input
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Default Resume URL</label>
            <input
              value={resumeUrl}
              onChange={(e) => setResumeUrl(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg"
            />
          </div>
          <button
            type="submit"
            className="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700"
          >
            Save Changes
          </button>
        </form>
      </div>
    </div>
  );
}
