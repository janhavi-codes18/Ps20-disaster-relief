const mongoose = require("mongoose");

const AIAnalysisSchema = new mongoose.Schema(
    {
        disaster_id: {
            type: String,
            required: true,
            index: true
        },

        prioritized_zones: {
            type: Array,
            default: []
        },

        allocations: {
            type: Array,
            default: []
        },

        alerts: {
            type: Array,
            default: []
        },

        reallocation_needed: {
            type: Boolean,
            default: false
        },

        reallocations: {
            type: Array,
            default: []
        },

        duplicate_efforts: {
            type: Array,
            default: []
        },

        explanation: {
            type: mongoose.Schema.Types.Mixed,
            default: {}
        },

        input_data: {
            type: mongoose.Schema.Types.Mixed,
            default: {}
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model(
    "AIAnalysis",
    AIAnalysisSchema
);