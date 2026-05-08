const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

// GET historical data
router.get("/", (req, res) => {
  const results = [];

  fs.createReadStream(
    path.join(__dirname, "../data/enriched_disaster_data.csv")
  )
    .pipe(csv())
    .on("data", (row) => {
      results.push({
        id: row.id || Math.random(),
        lat: Number(row.latitude),
        lng: Number(row.longitude),
        type: row.disastertype,
        description: "Historical Disaster Event",
        location: row.adm1,
        timestamp: row.year,
        source: "historical"
      });
    })
    .on("end", () => {
      res.json(results);
    });
});

module.exports = router;