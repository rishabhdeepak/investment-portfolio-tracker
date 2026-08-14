// ============================================================
// Dashboard Chart Data
// ============================================================

const assetLabels = JSON.parse(
    document.getElementById(
        "dashboard-asset-labels"
    ).textContent
);

const assetValues = JSON.parse(
    document.getElementById(
        "dashboard-asset-values"
    ).textContent
);


const sectorLabels = JSON.parse(
    document.getElementById(
        "dashboard-sector-labels"
    ).textContent
);

const sectorValues = JSON.parse(
    document.getElementById(
        "dashboard-sector-values"
    ).textContent
);


// ============================================================
// Shared Chart Settings
// ============================================================

const chartColors = [
    "#5B8DEF",
    "#22C55E",
    "#F59E0B",
    "#EF4444",
    "#06B6D4",
    "#8B5CF6",
    "#14B8A6",
    "#EC4899"
];


// ============================================================
// Asset Allocation Chart
// ============================================================

const assetCanvas = document.getElementById(
    "dashboardAssetAllocationChart"
);

if (assetCanvas) {

    new Chart(assetCanvas, {

        type: "doughnut",

        data: {

            labels: assetLabels,

            datasets: [{

                data: assetValues,

                backgroundColor: chartColors,

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "65%",

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#F8FAFC",

                        padding: 16

                    }

                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            return `${context.label}: ${context.raw.toFixed(2)}%`;

                        }

                    }

                }

            }

        }

    });

}


// ============================================================
// Sector Allocation Chart
// ============================================================

const sectorCanvas = document.getElementById(
    "dashboardSectorAllocationChart"
);

if (sectorCanvas) {

    new Chart(sectorCanvas, {

        type: "pie",

        data: {

            labels: sectorLabels,

            datasets: [{

                data: sectorValues,

                backgroundColor: chartColors,

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#F8FAFC",

                        padding: 16

                    }

                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            return `${context.label}: ${context.raw.toFixed(2)}%`;

                        }

                    }

                }

            }

        }

    });

}