const result = document.querySelector("#result");
const resultCard = document.querySelector("#resultCard");

const stream = document.querySelector("#stream");

const approved = document.querySelector("#approved");
const review = document.querySelector("#review");
const blocked = document.querySelector("#blocked");
const health = document.querySelector("#health");

const sentimentLabel = document.querySelector("#sentimentLabel");
const confidenceLabel = document.querySelector("#confidenceLabel");
const fakeLabel = document.querySelector("#fakeLabel");
const spamLabel = document.querySelector("#spamLabel");

/* ========================================= */
/* CHART */
/* ========================================= */

const sentimentChart = new Chart(
    document.getElementById("sentimentChart"),
    {
        type: "doughnut",

        data: {
            labels: [
                "Positive",
                "Neutral",
                "Negative"
            ],

            datasets: [{
                data: [0, 0, 0]
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            }
        }
    }
);

let positiveCount = 0;
let neutralCount = 0;
let negativeCount = 0;

async function rebuildChartFromHistory() {

    try {

        const response =
            await fetch(
                "/admin/recent-predictions?limit=100"
            );

        const raw =
            await response.json();

        const predictions =
            raw
                .map(item => {

                    try {

                        return JSON.parse(item);

                    }

                    catch {

                        return null;

                    }

                })
                .filter(Boolean);

        positiveCount = 0;
        neutralCount = 0;
        negativeCount = 0;

        predictions.forEach(entry => {

            const sentiment =
                (
                    entry.result
                    ?.sentiment
                    || ""
                ).toLowerCase();

            if (
                sentiment.includes(
                    "positive"
                )
            ) {

                positiveCount++;

            }

            else if (
                sentiment.includes(
                    "negative"
                )
            ) {

                negativeCount++;

            }

            else {

                neutralCount++;

            }

        });

        sentimentChart.data.datasets[0].data = [

            positiveCount,

            neutralCount,

            negativeCount

        ];

        sentimentChart.update();

    }

    catch(error){

        console.error(
            "Chart history load failed",
            error
        );
    }
}

/* ========================================= */
/* METRICS */
/* ========================================= */

async function refreshMetrics() {

    try {

        const h = await fetch("/health")
            .then(r => r.json());

        health.textContent =
            h.status === "ok"
                ? "Ready"
                : "Check";

    } catch {

        health.textContent = "Offline";
    }

    try {

        const m = await fetch("/analytics/metrics")
            .then(r => r.json());

        approved.textContent =
            m["decision.approve"] || 0;

        review.textContent =
            m["decision.review"] || 0;

        blocked.textContent =
            m["decision.block"] || 0;

    } catch {

        console.error(
            "Metrics unavailable"
        );
    }
}

/* ========================================= */
/* RESULT CARD */
/* ========================================= */

function renderResult(data) {

    const sentiment =
        data.sentiment || "unknown";

    const decision =
        data.decision || "UNKNOWN";

    const confidence =
        data.legit_probability ??
        data.confidence ??
        data.sentiment_score ??
        0;

    const fakeScore =
        data.fake_score ?? 0;

    const spamScore =
        data.spam_score ?? 0;

    const reason =
        data.reason || "No reason provided";

    let emoji = "🤖";

    if (
        sentiment.toLowerCase()
            .includes("positive")
    ) {
        emoji = "😊";
    }

    if (
        sentiment.toLowerCase()
            .includes("negative")
    ) {
        emoji = "😞";
    }

    if (
        sentiment.toLowerCase()
            .includes("neutral")
    ) {
        emoji = "😐";
    }

    resultCard.innerHTML = `

        <div class="analysis-result">

            <div class="analysis-header">

                <div class="analysis-emoji">
                    ${emoji}
                </div>

                <div>

                    <h2>${sentiment}</h2>

                    <p>
                        Decision:
                        <strong>${decision}</strong>
                    </p>

                </div>

            </div>

            <div class="analysis-grid">

                <div class="mini-card">
                    <span>Confidence</span>
                    <strong>
                        ${(confidence * 100).toFixed(1)}%
                    </strong>
                </div>

                <div class="mini-card">
                    <span>Fake Review Risk</span>
                    <strong>
                        ${(fakeScore * 100).toFixed(1)}%
                    </strong>
                </div>

                <div class="mini-card">
                    <span>Spam Risk</span>
                    <strong>
                        ${(spamScore * 100).toFixed(1)}%
                    </strong>
                </div>

                <div class="mini-card">
                    <span>Recommendation</span>
                    <strong>
                        ${decision}
                    </strong>
                </div>

            </div>

            <div class="reason-box">

                <h3>Analysis Reason</h3>

                <p>${reason}</p>

            </div>

        </div>

    `;

    sentimentLabel.textContent =
        sentiment;

    confidenceLabel.textContent =
        `${(confidence * 100).toFixed(1)}%`;

    fakeLabel.textContent =
        `${(fakeScore * 100).toFixed(1)}%`;

    spamLabel.textContent =
        `${(spamScore * 100).toFixed(1)}%`;

    result.textContent =
        JSON.stringify(data, null, 2);
}

/* ========================================= */
/* CHART UPDATE */
/* ========================================= */

function updateChart(sentiment) {

    const s =
        String(sentiment || "")
            .toLowerCase();

    if (
        s.includes("positive")
    ) {

        positiveCount++;

    }

    else if (
        s.includes("negative")
    ) {

        negativeCount++;

    }

    else {

        neutralCount++;

    }

    sentimentChart.data.datasets[0].data = [

        positiveCount,

        neutralCount,

        negativeCount

    ];

    sentimentChart.update();
}

/* ========================================= */
/* STREAM HISTORY */
/* ========================================= */

async function rebuildStreamFromHistory() {

    try {

        const response =
            await fetch(
                "/admin/recent-predictions?limit=20"
            );

        const raw =
            await response.json();

        const predictions =
            raw
                .map(item => {

                    try {

                        return JSON.parse(item);

                    }

                    catch {

                        return null;

                    }

                })
                .filter(Boolean);

        stream.innerHTML = "";

        predictions
            .reverse()
            .forEach(entry => {

                addRow(
                    entry.result
                );

            });

    }

    catch(error){

        console.error(
            "Stream history load failed",
            error
        );
    }
}

/* ========================================= */
/* LIVE STREAM */
/* ========================================= */

function addRow(payload) {

    const row =
        document.createElement("tr");

    row.innerHTML = `

        <td class="${payload.decision}">
            ${payload.decision}
        </td>

        <td>
            ${payload.sentiment}
        </td>

        <td>
            ${((payload.fake_score ?? 0) * 100).toFixed(1)}%
        </td>

        <td>
            ${((payload.spam_score ?? 0) * 100).toFixed(1)}%
        </td>

        <td>
            ${payload.reason ?? ""}
        </td>

    `;

    stream.prepend(row);

    while (
        stream.children.length > 12
    ) {

        stream.lastElementChild.remove();

    }
}

/* ========================================= */
/* FORM */
/* ========================================= */

document
.querySelector("#reviewForm")
.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const form =
            new FormData(
                event.currentTarget
            );

        const payload = {

            review_id:
                crypto.randomUUID(),

            product_id:
                "dashboard-product",

            user_id:
                "dashboard-user",

            rating:
                Number(
                    form.get("rating")
                ),

            summary:
                String(
                    form.get("summary")
                ),

            text:
                String(
                    form.get("text")
                )
        };

        try {

            const response =
                await fetch(
                    "/reviews/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );

            const data =
                await response.json();

            renderResult(data);

            addRow(data);

            updateChart(
                data.sentiment || "neutral"
            );

            await refreshMetrics();

        } catch (error) {

            console.error(error);

            alert(
                "Analysis failed"
            );
        }
    }
);

/* ========================================= */
/* INIT */
/* ========================================= */

async function initializeDashboard(){

    await refreshMetrics();

    await rebuildChartFromHistory();

    await rebuildStreamFromHistory();

}

initializeDashboard();

setInterval(
    refreshMetrics,
    10000
);

setInterval(
    rebuildStreamFromHistory,
    15000
);

setInterval(
    rebuildChartFromHistory,
    15000
);