const express = require("express");
const router = express.Router();
const Report = require("../models/Report");

// GET all reports
router.get("/", async (req, res) => {
  try {
    const reports = await Report.find();
    res.json(reports);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: err.message });
  }
});

// POST new report
router.post("/", async (req, res) => {
  try {
    const newReport = new Report(req.body);
    const saved = await newReport.save();
    res.status(201).json(saved);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;