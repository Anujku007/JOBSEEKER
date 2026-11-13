const Application = require('../models/Application');
const Job = require('../models/Job');

const applyToJob = async (req, res, next) => {
  try {
    const { jobId, resumeUrl, coverLetter } = req.body;
    const job = await Job.findById(jobId);

    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }

    const finalResumeUrl = req.file
      ? `/uploads/${req.file.filename}`
      : resumeUrl || req.user.resumeUrl;

    if (!finalResumeUrl) {
      return res.status(400).json({ message: 'Please provide a resume link or upload a PDF resume' });
    }

    const existing = await Application.findOne({ job: jobId, candidate: req.user._id });
    if (existing) {
      return res.status(400).json({ message: 'You have already applied to this job' });
    }

    const application = await Application.create({
      job: jobId,
      candidate: req.user._id,
      resumeUrl: finalResumeUrl,
      coverLetter: coverLetter || '',
    });

    res.status(201).json(application);
  } catch (error) {
    next(error);
  }
};

const getMyApplications = async (req, res, next) => {
  try {
    const applications = await Application.find({ candidate: req.user._id })
      .populate('job', 'title companyName location jobType salaryRange')
      .sort({ createdAt: -1 });
    res.json(applications);
  } catch (error) {
    next(error);
  }
};

const getJobApplications = async (req, res, next) => {
  try {
    const job = await Job.findById(req.params.jobId);
    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }
    if (job.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Not authorized to view applicants for this job' });
    }

    const applications = await Application.find({ job: req.params.jobId })
      .populate('candidate', 'name email headline skills location')
      .sort({ createdAt: -1 });

    res.json(applications);
  } catch (error) {
    next(error);
  }
};

const updateApplicationStatus = async (req, res, next) => {
  try {
    const { status } = req.body;
    const allowed = ['Applied', 'Shortlisted', 'Interview', 'Offered', 'Rejected'];
    if (!allowed.includes(status)) {
      return res.status(400).json({ message: 'Invalid application status' });
    }

    const application = await Application.findById(req.params.id).populate('job');
    if (!application) {
      return res.status(404).json({ message: 'Application not found' });
    }

    if (application.job.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Not authorized to update this application' });
    }

    application.status = status;
    await application.save();
    res.json(application);
  } catch (error) {
    next(error);
  }
};

module.exports = { applyToJob, getMyApplications, getJobApplications, updateApplicationStatus };
