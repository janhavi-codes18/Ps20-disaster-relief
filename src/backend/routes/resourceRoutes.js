const express = require("express");
const Resource = require("../models/Resource");

const router = express.Router();

// Create a new resource
router.post("/", async (req, res) => {
    try {
        const resource = await Resource.create(req.body);

        res.status(201).json({
            success: true,
            message: "Resource created successfully",
            resource: resource
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create resource",
            error: error.message
        });
    }
});

// Get all resources
router.get("/", async (req, res) => {
    try {
        const resources = await Resource.find().sort({ createdAt: -1 });

        res.json({
            success: true,
            resources: resources
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch resources",
            error: error.message
        });
    }
});

// Get one resource
router.get("/:id", async (req, res) => {
    try {
        const resource = await Resource.findById(req.params.id);

        if (!resource) {
            return res.status(404).json({
                success: false,
                message: "Resource not found"
            });
        }

        res.json({
            success: true,
            resource: resource
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch resource",
            error: error.message
        });
    }
});

module.exports = router;