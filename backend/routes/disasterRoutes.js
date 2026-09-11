const express = require("express");
const Disaster = require("../models/Disaster");

const router = express.Router();

// Create a new disaster
router.post("/", async (req, res) => {
    try {
        const disaster = await Disaster.create(req.body);

        res.status(201).json({
            success: true,
            message: "Disaster created successfully",
            disaster: disaster
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create disaster",
            error: error.message
        });
    }
});

// Get all disasters
router.get("/", async (req, res) => {
    try {
        const disasters = await Disaster.find().sort({ createdAt: -1 });

        res.json({
            success: true,
            disasters: disasters
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch disasters",
            error: error.message
        });
    }
});

// Get one disaster
router.get("/:id", async (req, res) => {
    try {
        const disaster = await Disaster.findById(req.params.id);

        if (!disaster) {
            return res.status(404).json({
                success: false,
                message: "Disaster not found"
            });
        }

        res.json({
            success: true,
            disaster: disaster
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch disaster",
            error: error.message
        });
    }
});

module.exports = router;