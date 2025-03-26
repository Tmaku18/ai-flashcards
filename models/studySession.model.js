// models/studySession.model.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const studySessionSchema = new Schema({
  user_id: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  session_name: { type: String, required: true },
  start_time: { type: Date, default: Date.now },
  end_time:   { type: Date }
});

module.exports = mongoose.model('StudySession', studySessionSchema);
