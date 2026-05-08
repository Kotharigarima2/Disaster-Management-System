const axios = require("axios");

exports.getNeeds = async (req, res) => {
  try {
    const response = await axios.post("http://localhost:8000/predict", {
      text: req.body.text,
    });

    res.json(response.data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "ML error" });
  }
};