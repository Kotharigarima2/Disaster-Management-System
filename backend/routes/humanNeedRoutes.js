const express = require("express");
const router = express.Router();

const { getNeeds } = require("../controllers/humanNeedController");

router.post("/", getNeeds);

module.exports = router;