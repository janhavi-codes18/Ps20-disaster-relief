const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const router = express.Router();

router.post("/analyze", (req, res) => {

    const inputData = req.body;

    console.log("Sending data to AI...");

    const aiPath = path.join(__dirname, "../../ai/run_ai.py");

    const python = spawn("py", [aiPath]);

    let output = "";
    let errorOutput = "";

    // Send JSON to Python
    python.stdin.write(JSON.stringify(inputData));
    python.stdin.end();

    // Receive AI output
    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    // Receive Python errors
    python.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    python.on("close", (code) => {

        if (code !== 0) {

            console.error("AI Error:", errorOutput);

            return res.status(500).json({
                success: false,
                message: "AI execution failed",
                error: errorOutput
            });
        }

        try {

            const aiResult = JSON.parse(output);

            console.log("AI result received successfully");

            res.json({
                success: true,
                result: aiResult
            });

        } catch (error) {

            console.error("Invalid AI JSON:", output);

            res.status(500).json({
                success: false,
                message: "AI returned invalid JSON",
                error: error.message,
                rawOutput: output
            });
        }
    });
});

module.exports = router;