// routes/user.routes.js
const express = require('express');
const router = express.Router();
const User = require('../models/user.model');

// GET all users
router.get('/', async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// CREATE a new user
router.post('/', async (req, res) => {
  try {
    const { username, email, password_hash } = req.body;
    const newUser = new User({ username, email, password_hash });
    await newUser.save();
    res.status(201).json(newUser);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;

