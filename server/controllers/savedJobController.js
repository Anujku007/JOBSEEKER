const SavedJob = require('../models/SavedJob');

const toggleSaveJob = async (req, res, next) => {
  try {
    const { jobId } = req.params;
    const existing = await SavedJob.findOne({ user: req.user._id, job: jobId });

    if (existing) {
      await existing.deleteOne();
      return res.json({ saved: false, message: 'Removed from saved jobs' });
    }

    await SavedJob.create({ user: req.user._id, job: jobId });
    res.status(201).json({ saved: true, message: 'Job saved' });
  } catch (error) {
    next(error);
  }
};

const getSavedJobs = async (req, res, next) => {
  try {
    const saved = await SavedJob.find({ user: req.user._id })
      .populate('job')
      .sort({ createdAt: -1 });
    res.json(saved.filter((item) => item.job !== null));
  } catch (error) {
    next(error);
  }
};

module.exports = { toggleSaveJob, getSavedJobs };
