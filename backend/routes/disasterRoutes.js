const express = require("express");
const router = express.Router();

const { getDisasterData } = require("../controllers/disasterController");

router.get("/", getDisasterData);

module.exports = router;