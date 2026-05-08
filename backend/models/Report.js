const mongoose = require("mongoose");

const ReportSchema = new mongoose.Schema({
  date: String,
  time: String,
  lat: Number,
  lng: Number,
  type: String,
  location: String,
  description: String,
  timestamp: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model("Report", ReportSchema);