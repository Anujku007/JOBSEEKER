const express = require('express');
const router = express.Router();
const { toggleSaveJob, getSavedJobs } = require('../controllers/savedJobController');
const { protect, authorize } = require('../middleware/authMiddleware');

router.get('/', protect, authorize('candidate'), getSavedJobs);
router.post('/:jobId', protect, authorize('candidate'), toggleSaveJob);

module.exports = router;
