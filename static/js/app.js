(function () {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem("smart-health-theme") || "light";
    root.setAttribute("data-bs-theme", savedTheme);

    function refreshIcons() {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    function chartDefaults() {
        if (!window.Chart) return;
        Chart.defaults.font.family = "Inter, system-ui, sans-serif";
        Chart.defaults.color = getComputedStyle(root).getPropertyValue("--muted").trim();
        Chart.defaults.borderColor = getComputedStyle(root).getPropertyValue("--line").trim();
    }

    document.addEventListener("DOMContentLoaded", function () {
        refreshIcons();
        chartDefaults();

        const toggle = document.getElementById("themeToggle");
        if (toggle) {
            toggle.addEventListener("click", function () {
                const next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
                root.setAttribute("data-bs-theme", next);
                localStorage.setItem("smart-health-theme", next);
                chartDefaults();
            });
        }

        renderScoreChart();
        renderDiseaseChart();
        renderTopPredictionChart();
        renderTrainingChart();
        wireChat();
    });

    function palette() {
        return ["#2563eb", "#0f9f8f", "#16a34a", "#d97706", "#dc2626", "#7c3aed", "#0891b2", "#be123c", "#4f46e5"];
    }

    function renderScoreChart() {
        const el = document.getElementById("scoreChart");
        if (!el || !window.Chart) return;
        const labels = JSON.parse(el.dataset.labels || "[]");
        const values = JSON.parse(el.dataset.values || "[]");
        new Chart(el, {
            type: "line",
            data: {
                labels: labels.length ? labels : ["Start"],
                datasets: [{
                    label: "Health score",
                    data: values.length ? values : [86],
                    borderColor: "#0f9f8f",
                    backgroundColor: "rgba(15, 159, 143, 0.12)",
                    tension: 0.35,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { min: 0, max: 100 } }
            }
        });
    }

    function renderDiseaseChart() {
        const el = document.getElementById("diseaseChart");
        if (!el || !window.Chart) return;
        const counts = JSON.parse(el.dataset.counts || "{}");
        const labels = Object.keys(counts);
        new Chart(el, {
            type: "doughnut",
            data: {
                labels: labels.length ? labels : ["No data"],
                datasets: [{
                    data: labels.length ? Object.values(counts) : [1],
                    backgroundColor: palette()
                }]
            },
            options: { responsive: true, plugins: { legend: { position: "bottom" } } }
        });
    }

    function renderTopPredictionChart() {
        const el = document.getElementById("topPredictionChart");
        if (!el || !window.Chart) return;
        const items = JSON.parse(el.dataset.items || "[]");
        new Chart(el, {
            type: "bar",
            data: {
                labels: items.map(item => item.disease),
                datasets: [{
                    label: "Probability",
                    data: items.map(item => item.probability),
                    backgroundColor: palette()
                }]
            },
            options: {
                indexAxis: "y",
                plugins: { legend: { display: false } },
                scales: { x: { min: 0, max: 100 } }
            }
        });
    }

    function renderTrainingChart() {
        const el = document.getElementById("trainingChart");
        if (!el || !window.Chart) return;
        const items = JSON.parse(el.dataset.items || "[]");
        new Chart(el, {
            type: "bar",
            data: {
                labels: items.map(item => item.algorithm),
                datasets: [{
                    label: "Accuracy",
                    data: items.map(item => Math.round(item.accuracy * 10000) / 100),
                    backgroundColor: palette()
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: { y: { min: 0, max: 100 } }
            }
        });
    }

    function wireChat() {
        const form = document.getElementById("chatForm");
        if (!form) return;
        const input = document.getElementById("chatMessage");
        const windowEl = document.getElementById("chatWindow");
        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            const message = input.value.trim();
            if (!message) return;
            addBubble(windowEl, message, "user");
            input.value = "";
            const response = await fetch(form.dataset.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            addBubble(windowEl, data.reply || "I could not answer that yet.", "bot");
        });
    }

    function addBubble(container, text, type) {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${type}`;
        bubble.textContent = text;
        container.appendChild(bubble);
        container.scrollTop = container.scrollHeight;
    }
})();
