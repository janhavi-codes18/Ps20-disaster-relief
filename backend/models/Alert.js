const mongoose = require("mongoose");

const alertSchema = new mongoose.Schema(
    {
        alertId: {
            type: String,
            required: true,
            unique: true
        },

        type: {
            type: String,
            required: true
        },

        severity: {
            type: String,
            enum: ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            required: true
        },

        zoneId: {
            type: String,
            required: true
        },

        message: {
            type: String,
            required: true
        },

        status: {
            type: String,
            enum: ["ACTIVE", "RESOLVED"],
            default: "ACTIVE"
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Alert", alertSchema);