const mongoose = require('mongoose');

const jobSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, trim: true },
    companyName: { type: String, required: true, trim: true },
    company: { type: mongoose.Schema.Types.ObjectId, ref: 'Company' },
    location: { type: String, required: true, trim: true },
    jobType: {
      type: String,
      enum: ['Full-Time', 'Part-Time', 'Internship', 'Contract', 'Remote'],
      default: 'Full-Time',
    },
    salaryRange: { type: String, default: 'Competitive' },
    description: { type: String, required: true },
    skillsRequired: [{ type: String }],
    source: {
      type: String,
      enum: ['internal', 'external'],
      default: 'internal',
    },
    externalApplyUrl: { type: String, default: '' },
    postedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    isActive: { type: Boolean, default: true },
  },
  { timestamps: true }
);

jobSchema.index({ title: 'text', companyName: 'text', description: 'text', location: 'text' });

module.exports = mongoose.model('Job', jobSchema);
