const express = require("express");
const router = express.Router();

const { analyzePriority } = require("../controllers/priorityController");

router.post("/", analyzePriority);

module.exports = router;