const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const AIAnalysis = require("./models/AIAnalysis");

const router = express.Router();

router.post("/analyze", (req, res) => {
    try {
        const inputData = req.body;

        if (!inputData || typeof inputData !== "object") {
            return res.status(400).json({
                success: false,
                message: "Invalid AI input. JSON object required."
            });
        }

        console.log("=================================");
        console.log("AI ANALYSIS REQUEST RECEIVED");
        console.log("=================================");

        const aiPath = path.join(
            __dirname,
            "../ai/run_ai.py"
        );

        console.log("AI script:", aiPath);

        const python = spawn("py", [aiPath]);

        let output = "";
        let errorOutput = "";

        python.stdin.write(
            JSON.stringify(inputData)
        );

        python.stdin.end();

        python.stdout.on("data", (data) => {
            output += data.toString();
        });

        python.stderr.on("data", (data) => {
            errorOutput += data.toString();
        });

        python.on("close", async (code) => {

            console.log(
                "AI process exited with code:",
                code
            );

            if (code !== 0) {

                console.error(
                    "AI execution error:",
                    errorOutput
                );

                return res.status(500).json({
                    success: false,
                    message: "AI execution failed",
                    error:
                        errorOutput ||
                        "Unknown Python error"
                });
            }

            try {

                const trimmedOutput =
                    output.trim();

                if (!trimmedOutput) {
                    throw new Error(
                        "AI returned an empty response."
                    );
                }

                const aiResult =
                    JSON.parse(
                        trimmedOutput
                    );

                console.log(
                    "AI result received successfully."
                );


                /* =========================================
                   SAVE AI RESULT TO MONGODB
                   ========================================= */

                const analysis =
                    new AIAnalysis({

                        disaster_id:
                            aiResult.disaster_id ||
                            inputData.disaster?.disaster_id ||
                            "UNKNOWN",

                        prioritized_zones:
                            aiResult.prioritized_zones ||
                            [],

                        allocations:
                            aiResult.allocations ||
                            [],

                        alerts:
                            aiResult.alerts ||
                            [],

                        reallocation_needed:
                            aiResult.reallocation_needed ||
                            false,

                        reallocations:
                            aiResult.reallocations ||
                            [],

                        duplicate_efforts:
                            aiResult.duplicate_efforts ||
                            [],

                        explanation:
                            aiResult.explanation ||
                            {},

                        input_data:
                            inputData
                    });


                const savedAnalysis =
                    await analysis.save();


                console.log(
                    "AI analysis saved to MongoDB."
                );

                console.log(
                    "Analysis ID:",
                    savedAnalysis._id.toString()
                );


                /* =========================================
                   SEND RESULT BACK TO FRONTEND
                   ========================================= */

                return res.json({

                    success: true,

                    result: aiResult,

                    analysis_id:
                        savedAnalysis._id

                });

            } catch (error) {

                console.error(
                    "AI result / MongoDB error:",
                    error
                );

                return res.status(500).json({

                    success: false,

                    message:
                        "Failed to process or save AI result",

                    error:
                        error.message,

                    rawOutput:
                        output
                });
            }
        });


        python.on("error", (error) => {

            console.error(
                "Failed to start Python AI process:",
                error
            );

            return res.status(500).json({

                success: false,

                message:
                    "Failed to start AI process",

                error:
                    error.message

            });
        });

    } catch (error) {

        console.error(
            "AI route error:",
            error
        );

        return res.status(500).json({

            success: false,

            message:
                "Unexpected AI route error",

            error:
                error.message

        });
    }
});

module.exports = router;