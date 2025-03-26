// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 1. CONNECT TO MONGODB
// Replace the URI with your local or MongoDB Atlas connection string
mongoose.connect("mongodb+srv://tmaku18:Atlanta12345!@project.ksr54.mongodb.net/Cluster0?retryWrites=true&w=majority"); {
};


// 2. CHECK CONNECTION
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

// 3. DEFINE ROUTES (we’ll create them later)
// const userRoutes = require('./routes/user.routes');
// const flashcardRoutes = require('./routes/flashcard.routes');
// app.use('/api/users', userRoutes);
// app.use('/api/flashcards', flashcardRoutes);

// 4. START SERVER
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

const userRoutes = require('./routes/user.routes');
app.use('/api/users', userRoutes);


