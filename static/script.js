let timeChart, topChart, pieChart, userTrendChart, funnelChart, segmentPieChart, categoryCompareChartVar, categoryChart, 
    recommendationChart, alsoViewedList, trafficAnomaliesList, purchaseAnomaliesList, unusualUsersList, anomalyChart;

const path = window.location.pathname;

// CLOCK
setInterval(() => {
    if (document.getElementById("datetime"))
        document.getElementById("datetime").innerText = new Date().toLocaleString();
}, 1000);

// LOAD DATA ONLY WHEN NEEDED
if (["/", "/products", "/funnel", "/segmentation"].includes(path)) {
    setInterval(loadDashboard, 5000);
    loadDashboard();
}

// MAIN DATA FUNCTION
function loadDashboard() {
    fetch("/api/dashboard")
        .then(res => res.json())
        .then(data => {

            // KPI
            if (document.getElementById("views"))
                document.getElementById("views").innerText = data.kpi.views;

            if (document.getElementById("purchases"))
                document.getElementById("purchases").innerText = data.kpi.purchases;

            if (document.getElementById("revenue"))
                document.getElementById("revenue").innerText = data.kpi.revenue;

            if (document.getElementById("purchase_rate"))
                document.getElementById("purchase_rate").innerText = data.kpi.purchase_rate;

            // TIME CHART
            if (document.getElementById("timeChart")) {
                if (timeChart) timeChart.destroy();
                timeChart = new Chart(document.getElementById("timeChart"), {
                    type: "line",
                    data: {
                        labels: Object.keys(data.time_series),
                        datasets: [{
                            data: Object.values(data.time_series)
                        }]
                    },
                    options: {
                        animation: false,
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }

            // TOP PRODUCTS
            if (document.getElementById("topChart")) {
                if (topChart) topChart.destroy();
                topChart = new Chart(document.getElementById("topChart"), {
                    type: "bar",
                    data: {
                        labels: data.top_products.map(p => p.product_id),
                        datasets: [{
                            data: data.top_products.map(p => p.views)
                        }]
                    },
                    options: {
                        animation: false,
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }

            // PIE
            if (document.getElementById("pieChart")) {
                if (pieChart) pieChart.destroy();
                pieChart = new Chart(document.getElementById("pieChart"), {
                    type: "bar",
                    data: {
                        labels: data.top_purchased.map(p => p.product_id),
                        datasets: [{
                            data: data.top_purchased.map(p => p.purchases)
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }

            // FUNNEL
            if (document.getElementById("funnelChart")) {
                if (funnelChart) funnelChart.destroy();
                funnelChart = new Chart(document.getElementById("funnelChart"), {
                    type: "bar",
                    data: {
                        labels: ["Views", "Cart", "Purchases"],
                        datasets: [{
                            data: [
                                data.funnel.views,
                                data.funnel.add_to_cart,
                                data.funnel.purchases
                            ],
                            backgroundColor: ["#3b82f6", "#f59e0b", "#10b981"]
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }

            // SEGMENT PIE
            if (document.getElementById("segmentPieChart")) {
                if (segmentPieChart) segmentPieChart.destroy();
                segmentPieChart = new Chart(document.getElementById("segmentPieChart"), {
                    type: "pie",
                    data: {
                        labels: Object.keys(data.user_segments),
                        datasets: [{
                            data: Object.values(data.user_segments)
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                display: true,
                                position: 'right'
                            }
                        }
                    }
                });
            }

            // User trend 
            const segData = data.user_trend;

            const allDates = new Set();
            Object.values(segData).forEach(seg => {
                Object.keys(seg).forEach(d => allDates.add(d));
            });
            const labels = Array.from(allDates).sort();

            const datasets = Object.keys(segData).map(segment => ({
                label: segment,
                data: labels.map(d => segData[segment][d] || 0),
                fill: false
            }));

            if (userTrendChart) userTrendChart.destroy();
            userTrendChart = new Chart(document.getElementById("userTrendChart"), {
                type: "line",
                data: { labels: labels, datasets: datasets },
                options: { animation: false }
            });

            // CATEGORY COMPARISON (Problem vs Best Categories)
            let categoryCompareChartVar;
            if (document.getElementById("categoryCompareChart")) {
                const problem = data.problem_categories || {};
                const best = data.best_categories || {};

                // Get all unique categories
                const categories = Array.from(new Set([
                    ...Object.keys(problem),
                    ...Object.keys(best)
                ]));

                // Prepare datasets
                const problemData = categories.map(cat => problem[cat] || 0);
                const bestData = categories.map(cat => best[cat] || 0);

                if (categoryCompareChartVar) categoryCompareChartVar.destroy();
                categoryCompareChartVar = new Chart(document.getElementById("categoryCompareChart"), {
                    type: 'bar',
                    data: {
                        labels: categories,
                        datasets: [
                            {
                                label: 'Problem Products (High Views, Low Purchases)',
                                data: problemData,
                                backgroundColor: 'rgba(255, 99, 132, 0.6)'
                            },
                            {
                                label: 'Good Products (Top Purchases)',
                                data: bestData,
                                backgroundColor: 'rgba(54, 162, 235, 0.6)'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Category Comparison: Problem vs Best'
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        },
                        interaction: {
                            mode: 'nearest',
                            axis: 'x',
                            intersect: false
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Counts'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Categories'
                                }
                            }
                        }
                    }
                });
            }

            // Categories
            if (document.getElementById("categoryChart")) {
                const cat = data.categories;

                new Chart(document.getElementById("categoryChart"), {
                    type: "pie",
                    data: {
                        labels: Object.keys(cat),
                        datasets: [{
                            data: Object.values(cat)
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        plugins: {
                            legend: {
                                display: true,
                                position: 'right'
                            }
                        }
                    }
                });
            }

            ///// INSIGHT PAGE

            // Also Viewed Recommendations
            if (document.getElementById("recommendationChart")) {
                const alsoViewedRaw = data.also_viewed || [];
                const alsoViewed = {};

                alsoViewedRaw.forEach(item => {
                    if (!alsoViewed[item.base_product]) alsoViewed[item.base_product] = [];
                    alsoViewed[item.base_product].push(item.recommended_product);
                });

                // Populate the list
                if (document.getElementById("alsoViewedList")) {
                    const list = document.getElementById("alsoViewedList");
                    list.innerHTML = "";
                    Object.entries(alsoViewed).forEach(([base, recs]) => {
                        recs.forEach(rec => {
                            list.innerHTML += `<li>${base} → ${rec}</li>`;
                        });
                    });
                }

                // Populate the chart
                const recCount = {};
                Object.values(alsoViewed).forEach(recs => {
                    recs.forEach(rec => {
                        recCount[rec] = (recCount[rec] || 0) + 1;
                    });
                });

                if (recommendationChartVar) recommendationChartVar.destroy();
                recommendationChartVar = new Chart(document.getElementById("recommendationChart"), {
                    type: 'bar',
                    data: {
                        labels: Object.keys(recCount),
                        datasets: [{
                            label: "Times Recommended",
                            data: Object.values(recCount),
                            backgroundColor: 'rgba(75, 192, 192, 0.6)'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // ---- ANOMALY DETECTION ----
            if (document.getElementById("trafficAnomaliesList")) {
                const trafficList = document.getElementById("trafficAnomaliesList");
                trafficList.innerHTML = "";
                (data.anomalies.traffic_spikes || []).forEach(a => {
                    trafficList.innerHTML += `<li>${a.date}: ${a.value} views (z=${a.z_score})</li>`;
                });
            }

            if (document.getElementById("purchaseAnomaliesList")) {
                const purchaseList = document.getElementById("purchaseAnomaliesList");
                purchaseList.innerHTML = "";
                (data.anomalies.purchase_drops || []).forEach(a => {
                    purchaseList.innerHTML += `<li>${a.date}: ${a.value} purchases (z=${a.z_score})</li>`;
                });
            }

            if (document.getElementById("unusualUsersList")) {
                const userList = document.getElementById("unusualUsersList");
                userList.innerHTML = "";
                (data.anomalies.unusual_users || []).forEach(u => {
                    userList.innerHTML += `<li>${u.user_id} (last activity: ${u.last_activity})</li>`;
                });
            }

            // Optional: Chart for Traffic & Purchases anomalies
            if (document.getElementById("anomalyChart")) {
                const anomalyLabels = [];
                const trafficValues = [];
                const purchaseValues = [];

                const allAnomalies = new Set();
                (data.anomalies.traffic_spikes || []).forEach(a => allAnomalies.add(a.date));
                (data.anomalies.purchase_drops || []).forEach(a => allAnomalies.add(a.date));

                Array.from(allAnomalies).sort().forEach(date => {
                    anomalyLabels.push(date);
                    const t = data.anomalies.traffic_spikes.find(a => a.date === date);
                    const p = data.anomalies.purchase_drops.find(a => a.date === date);
                    trafficValues.push(t ? t.value : 0);
                    purchaseValues.push(p ? p.value : 0);
                });

                if (window.anomalyChartVar) window.anomalyChartVar.destroy();
                window.anomalyChartVar = new Chart(document.getElementById("anomalyChart"), {
                    type: 'bar',
                    data: {
                        labels: anomalyLabels,
                        datasets: [
                            {
                                label: 'Traffic Spikes',
                                data: trafficValues,
                                backgroundColor: 'rgba(255, 99, 132, 0.6)'
                            },
                            {
                                label: 'Purchase Drops',
                                data: purchaseValues,
                                backgroundColor: 'rgba(54, 162, 235, 0.6)'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'top' } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

        });
}
