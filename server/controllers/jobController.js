const Job = require('../models/Job');
const { fetchExternalJobs } = require('../services/externalJobService');

const getJobs = async (req, res, next) => {
  try {
    const { keyword, location, jobType, includeExternal, page = 1, limit = 12 } = req.query;
    const query = { isActive: true };

    if (keyword) {
      query.$or = [
        { title: { $regex: keyword, $options: 'i' } },
        { companyName: { $regex: keyword, $options: 'i' } },
        { skillsRequired: { $regex: keyword, $options: 'i' } },
      ];
    }

    if (location) {
      query.location = { $regex: location, $options: 'i' };
    }

    if (jobType && jobType !== 'All') {
      query.jobType = jobType;
    }

    const skip = (Number(page) - 1) * Number(limit);
    const [jobs, total] = await Promise.all([
      Job.find(query)
        .populate('postedBy', 'name email')
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(Number(limit)),
      Job.countDocuments(query),
    ]);

    let externalJobs = [];
    if (includeExternal === 'true') {
      externalJobs = await fetchExternalJobs({
        query: keyword || 'Software Engineer',
        location: location || 'India',
      });
    }

    res.json({
      jobs,
      externalJobs,
      total,
      page: Number(page),
      pages: Math.ceil(total / Number(limit)),
    });
  } catch (error) {
    next(error);
  }
};

const getJobById = async (req, res, next) => {
  try {
    const job = await Job.findById(req.params.id).populate('postedBy', 'name email').populate('company');
    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }
    res.json(job);
  } catch (error) {
    next(error);
  }
};

const createJob = async (req, res, next) => {
  try {
    const { title, companyName, location, jobType, salaryRange, description, skillsRequired } = req.body;

    if (!title || !companyName || !location || !description) {
      return res.status(400).json({ message: 'Title, company, location, and description are required' });
    }

    const skills = Array.isArray(skillsRequired)
      ? skillsRequired
      : typeof skillsRequired === 'string'
      ? skillsRequired
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean)
      : [];

    const job = await Job.create({
      title,
      companyName,
      company: req.user.company || undefined,
      location,
      jobType: jobType || 'Full-Time',
      salaryRange: salaryRange || 'Competitive',
      description,
      skillsRequired: skills,
      postedBy: req.user._id,
    });

    res.status(201).json(job);
  } catch (error) {
    next(error);
  }
};

const getRecruiterJobs = async (req, res, next) => {
  try {
    const jobs = await Job.find({ postedBy: req.user._id }).sort({ createdAt: -1 });
    res.json(jobs);
  } catch (error) {
    next(error);
  }
};

const deleteJob = async (req, res, next) => {
  try {
    const job = await Job.findById(req.params.id);
    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }
    if (job.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Not authorized to delete this job' });
    }
    await job.deleteOne();
    res.json({ message: 'Job removed' });
  } catch (error) {
    next(error);
  }
};

module.exports = { getJobs, getJobById, createJob, getRecruiterJobs, deleteJob };
