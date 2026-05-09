const express = require("express");
const router = express.Router();
const axios = require("axios");

// ✅ SINGLE FLASK SERVER
const ML_BASE = "http://127.0.0.1:5001";

// 🔥 FULL DATA (UNCHANGED)
const manualDisasterData = [
  { location: "Delhi", tweet: "Severe flood in Delhi, people stuck on rooftops need rescue boats and food" },
  { location: "Mumbai", tweet: "Heavy flooding in Mumbai, urgent need for clean drinking water and shelter" },
  { location: "Chennai", tweet: "Heatwave in Chennai, people need water and medical help immediately" },
  { location: "Kolkata", tweet: "Cyclone approaching Kolkata, evacuation and food supplies needed urgently" },
  { location: "Bangalore", tweet: "Massive fire in building, injured people need medical assistance" },

  { location: "Delhi", tweet: "Waterlogging everywhere, families need food and shelter" },
  { location: "Mumbai", tweet: "People trapped due to flood, urgent rescue and food required" },
  { location: "Chennai", tweet: "Extreme heat causing illness, medical camps needed" },
  { location: "Kolkata", tweet: "Cyclone damage, homes destroyed, people need shelter and water" },
  { location: "Bangalore", tweet: "Firefighters rescuing people, medical help required" },

  { location: "Delhi", tweet: "Flood relief needed urgently, no electricity or water" },
  { location: "Mumbai", tweet: "Flood water rising, rescue teams required immediately" },
  { location: "Chennai", tweet: "People suffering from dehydration, need water supply" },
  { location: "Kolkata", tweet: "Strong winds destroyed houses, families need shelter" },
  { location: "Bangalore", tweet: "Fire accident, people injured need hospital support" },

  { location: "Hyderabad", tweet: "Heavy rain but situation normal" },
  { location: "Delhi", tweet: "Emergency situation, rescue teams needed urgently" },
  { location: "Mumbai", tweet: "Flood continues, people need food and water" },
  { location: "Chennai", tweet: "Heatwave alert, elderly need medical support" },
  { location: "Kolkata", tweet: "Cyclone alert issued, evacuation needed" },

  { location: "Delhi", tweet: "Families stuck due to flood, urgent help required" },
  { location: "Mumbai", tweet: "Rescue operations ongoing, people need shelter" },
  { location: "Chennai", tweet: "Medical camps required due to heatwave" },
  { location: "Kolkata", tweet: "Cyclone caused damage, food supplies needed" },
  { location: "Bangalore", tweet: "Fire under control, situation stable" },

  { location: "Hyderabad", tweet: "Normal weather, no issues" },
  { location: "Delhi", tweet: "Flood relief camps needed urgently" },
  { location: "Mumbai", tweet: "Severe flood, people trapped need rescue" },
  { location: "Chennai", tweet: "People need clean drinking water" },
  { location: "Kolkata", tweet: "Cyclone warning, stay safe" }
];



router.get("/", async (req, res) => {
  try {

    const tweets = manualDisasterData.map(item => item.tweet);

    // =========================
    // 🔥 PRIORITY + DISASTER (PER TWEET)
    // =========================
    const promises = tweets.map(tweet =>
      axios.post(`${ML_BASE}/analyze`, {
        tweets: [tweet],
        city: "India"
      })
    );

    const results = await Promise.all(promises);

    // ✅ PRIORITY COUNT
    const priorityStats = { HIGH: 0, MEDIUM: 0, LOW: 0 };

    results.forEach(r => {
      const p = r.data.priority;
      if (priorityStats[p] !== undefined) {
        priorityStats[p]++;
      }
    });

    // =========================
    // 🌪️ DISASTER TYPE (ML)
    // =========================
    const disasterData = manualDisasterData.map((item, index) => ({
      location: item.location,
      disaster: results[index].data.predictions[0], // ✅ FIX
      tweet: item.tweet
    }));

    // =========================
    // 🧑 NEEDS (ML)
    // =========================
    const needResponses = await Promise.all(
      tweets.map(tweet =>
        axios.post(`${ML_BASE}/predict`, { text: tweet })
      )
    );

    const allNeeds = new Set();

    needResponses.forEach(res => {
      (res.data.needs || []).forEach(n => allNeeds.add(n));
    });

    const needsList = Array.from(allNeeds);

    // =========================
    // 📍 TOP LOCATIONS
    // =========================
    const locationCounts = {};

    manualDisasterData.forEach(item => {
      locationCounts[item.location] =
        (locationCounts[item.location] || 0) + 1;
    });

    // =========================
    // ✅ FINAL RESPONSE
    // =========================
    res.json({
      disaster: disasterData,
      priority: priorityStats,
      needs: needsList
    });

  } catch (err) {
    console.error("Dashboard error:", err.message);
    res.status(500).json({ error: "Dashboard error" });
  }
});

module.exports = router;