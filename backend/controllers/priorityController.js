const axios = require("axios");

exports.analyzePriority = async (req, res) => {
  try {
    const response = await axios.post("http://127.0.0.1:5002/analyze", {
      tweets: req.body.tweets,
      city: req.body.city,
    });

    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "Priority ML error" });
  }
};