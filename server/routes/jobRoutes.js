const express = require('express');
const router = express.Router();
const {
  getJobs,
  getJobById,
  createJob,
  getRecruiterJobs,
  deleteJob,
} = require('../controllers/jobController');
const { protect, authorize } = require('../middleware/authMiddleware');

router.get('/', getJobs);
router.get('/recruiter/mine', protect, authorize('recruiter'), getRecruiterJobs);
router.get('/:id', getJobById);
router.post('/', protect, authorize('recruiter'), createJob);
router.delete('/:id', protect, authorize('recruiter'), deleteJob);

module.exports = router;
