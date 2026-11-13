import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-14">
      <div className="bg-white p-8 rounded-xl border border-slate-200">
        <h1 className="text-2xl font-bold mb-2">Welcome Back</h1>
        <p className="text-sm text-slate-500 mb-6">Sign in to your JOBSEEKER workspace.</p>

        {error && <div className="mb-4 p-3 bg-rose-50 text-rose-700 text-xs rounded-lg">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <input
            type="email"
            required
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />
          <input
            type="password"
            required
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2.5 border border-slate-300 rounded-lg"
          />
          <button
            type="submit"
            className="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700"
          >
            Log In
          </button>
        </form>

        <div className="mt-5 pt-4 border-t border-slate-100 flex gap-2">
          <button
            type="button"
            onClick={() => {
              setEmail('candidate@demo.com');
              setPassword('Password123!');
            }}
            className="flex-1 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50"
          >
            Fill Demo Candidate
          </button>
          <button
            type="button"
            onClick={() => {
              setEmail('recruiter@demo.com');
              setPassword('Password123!');
            }}
            className="flex-1 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50"
          >
            Fill Demo Recruiter
          </button>
        </div>

        <p className="mt-5 text-xs text-center text-slate-500">
          New here?{' '}
          <Link to="/register" className="text-indigo-600 font-semibold">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}
