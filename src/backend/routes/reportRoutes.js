const express = require("express");
const Report = require("../models/Report");

const router = express.Router();

// Create a new report
router.post("/", async (req, res) => {
    try {
        const report = await Report.create(req.body);

        res.status(201).json({
            success: true,
            message: "Report created successfully",
            report: report
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create report",
            error: error.message
        });
    }
});

// Get all reports
router.get("/", async (req, res) => {
    try {
        const reports = await Report.find().sort({ createdAt: -1 });

        res.json({
            success: true,
            reports: reports
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch reports",
            error: error.message
        });
    }
});

module.exports = router;