const dotenv = require('dotenv');
const connectDB = require('./config/db');
const User = require('./models/User');
const Company = require('./models/Company');
const Job = require('./models/Job');
const Application = require('./models/Application');
const SavedJob = require('./models/SavedJob');

dotenv.config();

const seedData = async () => {
  try {
    await connectDB();

    await Promise.all([
      User.deleteMany({}),
      Company.deleteMany({}),
      Job.deleteMany({}),
      Application.deleteMany({}),
      SavedJob.deleteMany({}),
    ]);

    const recruiter = await User.create({
      name: 'Priya Nair',
      email: 'recruiter@demo.com',
      password: 'Password123!',
      role: 'recruiter',
      headline: 'Senior Engineering Recruiter at FinStack',
      location: 'Bengaluru, India',
    });

    const company = await Company.create({
      name: 'FinStack Technologies',
      website: 'https://finstack.example.com',
      location: 'Bengaluru, India',
      description: 'Building next-generation payment and developer infrastructure.',
      owner: recruiter._id,
    });

    recruiter.company = company._id;
    await recruiter.save();

    const candidate = await User.create({
      name: 'Anuj Kumar',
      email: 'candidate@demo.com',
      password: 'Password123!',
      role: 'candidate',
      headline: 'Full-Stack Software Engineer | MERN & Python',
      location: 'Bengaluru, India',
      skills: ['JavaScript', 'React', 'Node.js', 'Express', 'MongoDB', 'Python'],
      resumeUrl: 'https://linkedin.com/in/anuj-kumar-836680298',
    });

    const jobs = await Job.insertMany([
      {
        title: 'Full-Stack Software Engineer (MERN)',
        companyName: 'FinStack Technologies',
        company: company._id,
        location: 'Bengaluru, India',
        jobType: 'Full-Time',
        salaryRange: '₹12,00,000 - ₹16,00,000',
        description:
          'Design, build, and scale full-stack web applications using MongoDB, Express.js, React, and Node.js. Own end-to-end feature delivery, REST API architecture, and automated testing.',
        skillsRequired: ['React', 'Node.js', 'Express', 'MongoDB', 'REST APIs'],
        postedBy: recruiter._id,
      },
      {
        title: 'Backend Node.js Engineer',
        companyName: 'FinStack Technologies',
        company: company._id,
        location: 'Remote',
        jobType: 'Remote',
        salaryRange: '₹10,00,000 - ₹14,00,000',
        description:
          'Build low-latency microservices, webhook ingestion pipelines, and secure authentication layers in Node.js and Express.',
        skillsRequired: ['Node.js', 'Express', 'MongoDB', 'Docker', 'JWT'],
        postedBy: recruiter._id,
      },
      {
        title: 'SDE Intern - Product Engineering',
        companyName: 'FinStack Technologies',
        company: company._id,
        location: 'Bengaluru, India',
        jobType: 'Internship',
        salaryRange: '₹45,000 / month',
        description:
          'Work alongside senior engineers to build responsive React dashboards and integrate backend APIs.',
        skillsRequired: ['JavaScript', 'React', 'Tailwind CSS', 'Git'],
        postedBy: recruiter._id,
      },
    ]);

    await Application.create({
      job: jobs[0]._id,
      candidate: candidate._id,
      resumeUrl: candidate.resumeUrl,
      coverLetter: 'Excited to contribute full-stack MERN and API engineering skills to FinStack.',
      status: 'Shortlisted',
    });

    await SavedJob.create({
      user: candidate._id,
      job: jobs[1]._id,
    });

    console.log('Database seeded successfully!');
    console.log('Candidate login -> candidate@demo.com / Password123!');
    console.log('Recruiter login -> recruiter@demo.com / Password123!');
    process.exit(0);
  } catch (error) {
    console.error('Seed failed:', error);
    process.exit(1);
  }
};

seedData();
