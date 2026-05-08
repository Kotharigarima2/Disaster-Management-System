const express = require("express");
const router = express.Router();
const axios = require("axios");

// 🔥 STRONG REALISTIC DATA (30 tweets)
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
    // 🔥 PRIORITY API
    // =========================
    const priorityRes = await axios.post("http://127.0.0.1:5002/analyze", {
      tweets,
      city: "India"
    });

    const priorityStats = {
      HIGH: priorityRes.data.priority === "HIGH" ? 1 : 0,
      MEDIUM: priorityRes.data.priority === "MEDIUM" ? 1 : 0,
      LOW: priorityRes.data.priority === "LOW" ? 1 : 0
    };

    // =========================
    // 🔥 NEEDS API
    // =========================
    const allNeeds = new Set();
    for (let tweet of tweets) {
      const resNeed = await axios.post("http://127.0.0.1:8000/predict", { text: tweet });
      (resNeed.data.needs || []).forEach(n => allNeeds.add(n));
    }
    const needsList = Array.from(allNeeds);

    // =========================
    // 🔥 DISASTER TYPES
    // =========================
    const disasterData = manualDisasterData.map(item => {
      const t = item.tweet.toLowerCase();
      let disaster = "Other";
      if (t.includes("flood")) disaster = "Flood";
      else if (t.includes("fire")) disaster = "Fire";
      else if (t.includes("cyclone")) disaster = "Cyclone";
      else if (t.includes("heatwave")) disaster = "Heatwave";
      return { location: item.location, disaster, tweet: item.tweet };
    });

    // =========================
    res.json({ disaster: disasterData, priority: priorityStats, needs: needsList });

  } catch (err) {
    console.error("Dashboard error:", err.message);
    res.status(500).json({ error: "Dashboard error" });
  }
});

module.exports = router;