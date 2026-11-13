import { Link } from 'react-router-dom';
import { MapPin, Building2, Clock, Bookmark, ExternalLink } from 'lucide-react';

export default function JobCard({ job, isSaved, onToggleSave, showSaveButton }) {
  const isExternal = job.source === 'external';

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-md transition flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-3">
          <div>
            <span className="inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 mb-2">
              {job.jobType}
            </span>
            {isExternal && (
              <span className="ml-2 inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 mb-2">
                External Partner
              </span>
            )}
            <h3 className="text-lg font-semibold text-slate-900">{job.title}</h3>
            <div className="flex items-center gap-2 text-sm text-slate-600 mt-1">
              <Building2 className="w-4 h-4 text-slate-400" />
              <span>{job.companyName}</span>
            </div>
          </div>

          {showSaveButton && !isExternal && (
            <button
              onClick={() => onToggleSave(job._id)}
              title={isSaved ? 'Remove from saved' : 'Save job'}
              className={`p-2 rounded-lg border transition ${
                isSaved
                  ? 'bg-indigo-50 border-indigo-200 text-indigo-600'
                  : 'border-slate-200 text-slate-400 hover:text-slate-600'
              }`}
            >
              <Bookmark className="w-4 h-4 fill-current" />
            </button>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-3">
          <span className="flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5" />
            {job.location}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            {job.salaryRange}
          </span>
        </div>

        <p className="text-sm text-slate-600 mt-3 line-clamp-2">{job.description}</p>

        {job.skillsRequired?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-4">
            {job.skillsRequired.slice(0, 5).map((skill, idx) => (
              <span
                key={idx}
                className="text-xs px-2 py-0.5 bg-slate-100 text-slate-700 rounded-md font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
        <span className="text-xs text-slate-400">
          Posted {new Date(job.createdAt).toLocaleDateString()}
        </span>

        {isExternal ? (
          <a
            href={job.externalApplyUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-sm font-semibold text-indigo-600 hover:text-indigo-700"
          >
            Apply Externally <ExternalLink className="w-4 h-4" />
          </a>
        ) : (
          <Link
            to={`/jobs/${job._id}`}
            className="text-sm font-semibold text-indigo-600 hover:text-indigo-700"
          >
            View & Apply →
          </Link>
        )}
      </div>
    </div>
  );
}
