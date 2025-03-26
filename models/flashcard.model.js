// models/flashcard.model.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const flashcardSchema = new Schema({
  user_id: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  question: { type: String, required: true },
  answer:   { type: String, required: true },
  created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Flashcard', flashcardSchema);
