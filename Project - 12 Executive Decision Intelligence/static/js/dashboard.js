/**
 * Hindustan Unilever Limited - Executive Decision Intelligence System
 * Dashboard Client Engine (Project - 12)
 */

document.addEventListener("DOMContentLoaded", () => {
    initParadoxChart();
    initAttributionChart();
    initWaterfallChart();
    initSimulator();
    initTerminal();
    loadProtocols();
});

// Global chart references
let chartParadoxInstance = null;
let chartAttributionInstance = null;
let chartWaterfallInstance = null;

/* --------------------------------------------------------------------------
   Chart 1: The FMCG KPI Paradox
   -------------------------------------------------------------------------- */
function initParadoxChart() {
    const ctx = document.getElementById("chartParadox").getContext("2d");
    chartParadoxInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Plant OEE\n(Mfg Claim)', 'Direct Reach\n(Sales Claim)', 'Media SOV\n(Mktg Claim)', 'Focus SKU\nAvailability', 'Distributor\nCredit Health', 'EBITDA Margin\n(Realized)'],
            datasets: [{
                label: 'Department Metric Score (%)',
                data: [86.5, 92.0, 88.0, 68.2, 54.0, 64.5],
                backgroundColor: [
                    'rgba(0, 114, 206, 0.85)',
                    'rgba(0, 114, 206, 0.85)',
                    'rgba(0, 114, 206, 0.85)',
                    'rgba(239, 68, 68, 0.85)',
                    'rgba(245, 158, 11, 0.85)',
                    'rgba(220, 38, 38, 0.95)'
                ],
                borderColor: [
                    '#0072CE', '#0072CE', '#0072CE', '#EF4444', '#F59E0B', '#DC2626'
                ],
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 105,
                    grid: { color: 'rgba(255, 255, 255, 0.06)' },
                    ticks: { color: '#94A3B8', font: { size: 11 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#CBD5E1', font: { size: 11, weight: 'bold' } }
                }
            }
        }
    });
}

/* --------------------------------------------------------------------------
   Chart 2: AI Causal Attribution & Vital Drivers
   -------------------------------------------------------------------------- */
function initAttributionChart() {
    const ctx = document.getElementById("chartAttribution").getContext("2d");
    chartAttributionInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Focus SKU Stockout Rate',
                'Commodity Hedging Coverage',
                'Secondary OTIF Delivery',
                'Distributor Working Capital',
                'Trade Scheme Discount Depth',
                'Shikhar B2B App Share',
                'Batch Changeover Latency',
                'Plant OEE (Vanity Noise)'
            ],
            datasets: [{
                label: 'Decomposed EBITDA Variance Explained (%)',
                data: [28.4, 18.2, 14.6, 12.1, 9.8, 6.2, 5.4, 1.4],
                backgroundColor: [
                    '#001F60',
                    '#00439C',
                    '#0072CE',
                    '#009BE5',
                    '#0D9488',
                    '#10B981',
                    '#F59E0B',
                    '#EF4444'
                ],
                borderWidth: 1,
                borderColor: 'rgba(255, 255, 255, 0.2)',
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.parsed.x}% of financial variance`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    min: 0,
                    max: 32,
                    grid: { color: 'rgba(255, 255, 255, 0.06)' },
                    ticks: { color: '#94A3B8', font: { size: 11 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#CBD5E1', font: { size: 11 } }
                }
            }
        }
    });
}

/* --------------------------------------------------------------------------
   Chart 3: Financial Friction Waterfall
   -------------------------------------------------------------------------- */
function initWaterfallChart() {
    const ctx = document.getElementById("chartWaterfall").getContext("2d");
    
    // Waterfall representation: Base potential -> Negative leakages -> Realized
    chartWaterfallInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Potential EBITDA',
                'Commodity Unhedged',
                'Focus Stockouts',
                'Distributor Credit',
                'Trade Discounts',
                'Realized EBITDA'
            ],
            datasets: [
                {
                    label: 'Base Offset',
                    data: [0, 3805, 3591, 3423, 3305, 0],
                    backgroundColor: 'transparent',
                    borderWidth: 0
                },
                {
                    label: 'Magnitude (₹ Cr)',
                    data: [3950, 145, 214, 168, 118, 3305],
                    backgroundColor: [
                        '#10B981',
                        '#EF4444',
                        '#EF4444',
                        '#F59E0B',
                        '#F59E0B',
                        '#0072CE'
                    ],
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    filter: function(item) {
                        return item.datasetIndex === 1;
                    },
                    callbacks: {
                        label: function(context) {
                            const val = context.parsed.y;
                            const idx = context.dataIndex;
                            if (idx === 0 || idx === 5) {
                                return ` Level: ₹${val} Cr`;
                            }
                            return ` Leakage: -₹${val} Cr`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    stacked: true,
                    min: 0,
                    max: 4500,
                    grid: { color: 'rgba(255, 255, 255, 0.06)' },
                    ticks: { color: '#94A3B8', font: { size: 11 } }
                },
                x: {
                    stacked: true,
                    grid: { display: false },
                    ticks: { color: '#CBD5E1', font: { size: 11 } }
                }
            }
        }
    });
}

/* --------------------------------------------------------------------------
   Real-Time Scenario Simulator
   -------------------------------------------------------------------------- */
function initSimulator() {
    const sliders = [
        { id: "slider-stockout", valId: "val-stockout", unit: "%" },
        { id: "slider-otif", valId: "val-otif", unit: "%" },
        { id: "slider-hedging", valId: "val-hedging", unit: "%" },
        { id: "slider-wc", valId: "val-wc", unit: " d" },
        { id: "slider-shikhar", valId: "val-shikhar", unit: "%" },
        { id: "slider-discount", valId: "val-discount", unit: "%" }
    ];

    sliders.forEach(s => {
        const el = document.getElementById(s.id);
        const valEl = document.getElementById(s.valId);
        el.addEventListener("input", (e) => {
            valEl.textContent = `${parseFloat(e.target.value).toFixed(1)}${s.unit}`;
            debounceSimulate();
        });
    });

    const resetBtn = document.getElementById("btnResetSimulator");
    resetBtn.addEventListener("click", () => {
        document.getElementById("slider-stockout").value = 6.5;
        document.getElementById("val-stockout").textContent = "6.5%";

        document.getElementById("slider-otif").value = 89.2;
        document.getElementById("val-otif").textContent = "89.2%";

        document.getElementById("slider-hedging").value = 62.0;
        document.getElementById("val-hedging").textContent = "62.0%";

        document.getElementById("slider-wc").value = 21.8;
        document.getElementById("val-wc").textContent = "21.8 d";

        document.getElementById("slider-shikhar").value = 34.0;
        document.getElementById("val-shikhar").textContent = "34.0%";

        document.getElementById("slider-discount").value = 7.8;
        document.getElementById("val-discount").textContent = "7.8%";

        triggerSimulation();
    });
}

let debounceTimer = null;
function debounceSimulate() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(triggerSimulation, 120);
}

function triggerSimulation() {
    const payload = {
        focus_sku_stockout_rate: parseFloat(document.getElementById("slider-stockout").value),
        otif_secondary_pct: parseFloat(document.getElementById("slider-otif").value),
        commodity_hedging_coverage_pct: parseFloat(document.getElementById("slider-hedging").value),
        distributor_wc_days: parseFloat(document.getElementById("slider-wc").value),
        shikhar_app_order_share_pct: parseFloat(document.getElementById("slider-shikhar").value),
        trade_scheme_discount_depth_pct: parseFloat(document.getElementById("slider-discount").value)
    };

    fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        updateSimulationUI(data);
    })
    .catch(err => console.error("Simulation error:", err));
}

function updateSimulationUI(data) {
    const proj = data.projected;
    const deltas = data.deltas;

    document.getElementById("sim-proj-revenue").textContent = `₹${proj.net_revenue_cr.toLocaleString()} Cr`;
    document.getElementById("sim-proj-ebitda").textContent = `${proj.ebitda_margin_pct.toFixed(2)}%`;
    document.getElementById("sim-proj-ebitda-cr").textContent = `₹${proj.ebitda_cr.toLocaleString()} Cr`;
    document.getElementById("sim-proj-fcf").textContent = `₹${proj.free_cash_flow_cr.toLocaleString()} Cr`;

    // Deltas formatting
    formatDelta("sim-delta-revenue", deltas.revenue_cr, "₹", " Cr");
    formatDelta("sim-delta-ebitda", deltas.ebitda_bps, "", " bps");
    formatDelta("sim-delta-ebitda-cr", deltas.ebitda_cr, "₹", " Cr");
    formatDelta("sim-delta-fcf", deltas.free_cash_flow_cr, "₹", " Cr");

    // Strategic tone & memo
    const statusBadge = document.getElementById("sim-status-badge");
    statusBadge.textContent = data.strategic_tone;
    if (deltas.ebitda_cr > 60) {
        statusBadge.style.color = "#10B981";
        statusBadge.style.borderColor = "#10B981";
        statusBadge.style.background = "rgba(16, 185, 129, 0.15)";
    } else if (deltas.ebitda_cr < -60) {
        statusBadge.style.color = "#EF4444";
        statusBadge.style.borderColor = "#EF4444";
        statusBadge.style.background = "rgba(239, 68, 68, 0.15)";
    } else {
        statusBadge.style.color = "#009BE5";
        statusBadge.style.borderColor = "#009BE5";
        statusBadge.style.background = "rgba(0, 155, 229, 0.15)";
    }

    document.getElementById("sim-memo-text").textContent = data.summary_memo;
}

function formatDelta(elementId, val, prefix, suffix) {
    const el = document.getElementById(elementId);
    const sign = val > 0 ? "+" : (val < 0 ? "-" : "±");
    const absVal = Math.abs(val).toFixed(1);
    el.textContent = `${sign}${prefix}${absVal}${suffix}`;
    if (val > 0.1) {
        el.style.color = "#10B981";
    } else if (val < -0.1) {
        el.style.color = "#EF4444";
    } else {
        el.style.color = "#94A3B8";
    }
}

/* --------------------------------------------------------------------------
   LLM-Powered Executive Terminal
   -------------------------------------------------------------------------- */
function initTerminal() {
    const inputEl = document.getElementById("terminalInput");
    const askBtn = document.getElementById("btnAskAgent");

    // Quick questions
    document.querySelectorAll(".pill-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const query = btn.getAttribute("data-query");
            inputEl.value = query;
            submitQuery(query);
        });
    });

    askBtn.addEventListener("click", () => {
        const query = inputEl.value.trim();
        if (query) submitQuery(query);
    });

    inputEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const query = inputEl.value.trim();
            if (query) submitQuery(query);
        }
    });
}

function submitQuery(query) {
    const outputWindow = document.getElementById("terminalOutput");
    outputWindow.innerHTML = `
        <div class="terminal-placeholder">
            <div class="pulse-indicator"></div>
            <div>Analyzing 720 operational telemetry records and synthesizing grounded econometric response for: <i>"${query}"</i>...</div>
        </div>
    `;

    fetch("/api/agent_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    })
    .then(res => res.json())
    .then(data => {
        renderAgentResponse(data);
    })
    .catch(err => {
        outputWindow.innerHTML = `<div style="color: #EF4444;">Error communicating with AI Decision Agent: ${err.message}</div>`;
    });
}

function renderAgentResponse(data) {
    const outputWindow = document.getElementById("terminalOutput");
    
    let metricsHtml = "";
    if (data.supporting_metrics) {
        metricsHtml = `<div class="agent-metrics-row">`;
        for (const [k, v] of Object.entries(data.supporting_metrics)) {
            const label = k.replace(/_/g, " ").toUpperCase();
            metricsHtml += `<div class="agent-metric-chip"><b>${label}:</b> ${v}</div>`;
        }
        metricsHtml += `</div>`;
    }

    // Convert markdown bold to html bold
    let formattedText = data.executive_answer
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/•/g, '&bull;');

    outputWindow.innerHTML = `
        <div class="agent-response-box">
            <div class="agent-badge-row">
                <span class="agent-category">${data.category || 'Executive Decision Synthesis'}</span>
                <span class="badge-tag">Grounded Evidence</span>
            </div>
            <div class="agent-content">${formattedText}</div>
            ${metricsHtml}
        </div>
    `;
}

/* --------------------------------------------------------------------------
   Load Prescriptive Protocols
   -------------------------------------------------------------------------- */
function loadProtocols() {
    fetch("/api/protocols")
    .then(res => res.json())
    .then(protocols => {
        const grid = document.getElementById("protocolsGrid");
        grid.innerHTML = "";
        protocols.forEach(p => {
            const card = document.createElement("div");
            card.className = "protocol-card";
            card.innerHTML = `
                <div class="proto-id">${p.protocol_id}</div>
                <div class="proto-name">${p.name}</div>
                <div class="proto-target">${p.operational_target}</div>
                <div class="proto-financials">
                    <div class="proto-gain">+₹${p.annual_financial_gain_cr} Cr / yr</div>
                    <div class="proto-meta">+${p.ebitda_margin_gain_bps} bps EBITDA | ${p.payback_months} Mo Payback</div>
                    <div class="proto-meta" style="color: #94A3B8;">Capex: ₹${p.capital_investment_cr} Cr | ${p.lead_executive}</div>
                </div>
            `;
            grid.appendChild(card);
        });
    })
    .catch(err => console.error("Error loading protocols:", err));
}

