import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    role: 'candidate',
    companyName: '',
    location: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await register(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-14">
      <div className="bg-white p-8 rounded-xl border border-slate-200">
        <h1 className="text-2xl font-bold mb-2">Create Your Account</h1>
        <p className="text-sm text-slate-500 mb-6">Join as a job seeker or hiring recruiter.</p>

        {error && <div className="mb-4 p-3 bg-rose-50 text-rose-700 text-xs rounded-lg">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 rounded-lg">
            {['candidate', 'recruiter'].map((role) => (
              <button
                type="button"
                key={role}
                onClick={() => setForm({ ...form, role })}
                className={`py-1.5 rounded-md font-semibold capitalize transition ${
                  form.role === role ? 'bg-white shadow text-indigo-600' : 'text-slate-600'
                }`}
              >
                {role}
              </button>
            ))}
          </div>

          <input
            required
            placeholder="Full Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />
          <input
            type="email"
            required
            placeholder="Email Address"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />
          <input
            type="password"
            required
            minLength={6}
            placeholder="Password (min 6 characters)"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />
          {form.role === 'recruiter' && (
            <input
              required
              placeholder="Company Name"
              value={form.companyName}
              onChange={(e) => setForm({ ...form, companyName: e.target.value })}
              className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
            />
          )}
          <input
            placeholder="City / Location"
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />

          <button
            type="submit"
            className="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700"
          >
            Sign Up
          </button>
        </form>

        <p className="mt-5 text-xs text-center text-slate-500">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-600 font-semibold">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
