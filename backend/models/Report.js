const mongoose = require("mongoose");

const reportSchema = new mongoose.Schema(
    {
        reportId: {
            type: String,
            required: true,
            unique: true
        },

        zoneId: {
            type: String,
            required: true
        },

        reportType: {
            type: String,
            required: true
        },

        message: {
            type: String,
            required: true
        },

        severity: {
            type: String,
            enum: ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default: "MEDIUM"
        },

        peopleAffected: {
            type: Number,
            default: 0,
            min: 0
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Report", reportSchema);