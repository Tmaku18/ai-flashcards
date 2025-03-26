// models/quiz.model.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const quizSchema = new Schema({
  user_id: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  quiz_title: { type: String, required: true },
  created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Quiz', quizSchema);
