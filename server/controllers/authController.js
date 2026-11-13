const jwt = require('jsonwebtoken');
const User = require('../models/User');
const Company = require('../models/Company');

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  });
};

const registerUser = async (req, res, next) => {
  try {
    const { name, email, password, role, companyName, location, headline, skills } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ message: 'Name, email, and password are required' });
    }

    const exists = await User.findOne({ email });
    if (exists) {
      return res.status(400).json({ message: 'An account with this email already exists' });
    }

    const user = await User.create({
      name,
      email,
      password,
      role: role === 'recruiter' ? 'recruiter' : 'candidate',
      location: location || '',
      headline: headline || '',
      skills: Array.isArray(skills)
        ? skills
        : typeof skills === 'string' && skills.trim()
        ? skills.split(',').map((s) => s.trim())
        : [],
    });

    if (user.role === 'recruiter' && companyName) {
      const company = await Company.create({
        name: companyName,
        location: location || '',
        owner: user._id,
      });
      user.company = company._id;
      await user.save();
    }

    const populatedUser = await User.findById(user._id).select('-password').populate('company');

    res.status(201).json({
      user: populatedUser,
      token: generateToken(user._id),
    });
  } catch (error) {
    next(error);
  }
};

const loginUser = async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email }).populate('company');

    if (!user || !(await user.matchPassword(password))) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }

    const safeUser = user.toObject();
    delete safeUser.password;

    res.json({
      user: safeUser,
      token: generateToken(user._id),
    });
  } catch (error) {
    next(error);
  }
};

const getMe = async (req, res, next) => {
  try {
    const user = await User.findById(req.user._id).select('-password').populate('company');
    res.json(user);
  } catch (error) {
    next(error);
  }
};

const updateProfile = async (req, res, next) => {
  try {
    const { name, headline, location, skills, resumeUrl } = req.body;
    const user = await User.findById(req.user._id);

    if (name) user.name = name;
    if (headline !== undefined) user.headline = headline;
    if (location !== undefined) user.location = location;
    if (resumeUrl !== undefined) user.resumeUrl = resumeUrl;
    if (skills !== undefined) {
      user.skills = Array.isArray(skills)
        ? skills
        : skills
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean);
    }

    if (req.file) {
      user.resumeUrl = `/uploads/${req.file.filename}`;
    }

    await user.save();
    const updated = await User.findById(user._id).select('-password').populate('company');
    res.json(updated);
  } catch (error) {
    next(error);
  }
};

module.exports = { registerUser, loginUser, getMe, updateProfile };
