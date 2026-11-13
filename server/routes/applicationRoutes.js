const express = require('express');
const router = express.Router();
const {
  applyToJob,
  getMyApplications,
  getJobApplications,
  updateApplicationStatus,
} = require('../controllers/applicationController');
const { protect, authorize } = require('../middleware/authMiddleware');
const upload = require('../middleware/uploadMiddleware');

router.post('/', protect, authorize('candidate'), upload.single('resume'), applyToJob);
router.get('/mine', protect, authorize('candidate'), getMyApplications);
router.get('/job/:jobId', protect, authorize('recruiter'), getJobApplications);
router.patch('/:id/status', protect, authorize('recruiter'), updateApplicationStatus);

module.exports = router;
