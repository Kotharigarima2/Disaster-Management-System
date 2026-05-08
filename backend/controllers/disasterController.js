const axios = require("axios");

exports.getDisasterData = async (req, res) => {
  try {
    const response = await axios.get("http://127.0.0.1:5003/disaster-data");
    res.json(response.data);
  } catch (err) {
    console.error("ERROR:", err.message);
    res.status(500).json({ error: "Disaster ML error" });
  }
};