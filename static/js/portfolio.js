// Read Django JSON data
const sectorLabels = JSON.parse(
    document.getElementById("sector-labels").textContent
);

const sectorValues = JSON.parse(
    document.getElementById("sector-values").textContent
);

const assetLabels = JSON.parse(
    document.getElementById("asset-labels").textContent
);

const assetValues = JSON.parse(
    document.getElementById("asset-values").textContent
);

// ----------------------------
// Sector Allocation Chart
// ----------------------------

const sectorCanvas = document.getElementById("sectorAllocationChart");

if (sectorCanvas) {
    new Chart(sectorCanvas, {
        type: "pie",

        data: {
            labels: sectorLabels,
            datasets: [{
                data: sectorValues,
                backgroundColor: [
                    "#5B8DEF",
                    "#22C55E",
                    "#F59E0B",
                    "#EF4444",
                    "#06B6D4",
                    "#8B5CF6",
                    "#14B8A6",
                    "#EC4899"
                ],
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
                        color: "#F8FAFC"
                    }
                }
            }
        }
    });
}

// ----------------------------
// Asset Allocation Chart
// ----------------------------

const assetCanvas = document.getElementById("assetAllocationChart");

if (assetCanvas) {
    new Chart(assetCanvas, {
        type: "doughnut",

        data: {
            labels: assetLabels,
            datasets: [{
                data: assetValues,
                backgroundColor: [
                    "#5B8DEF",
                    "#22C55E",
                    "#F59E0B",
                    "#EF4444",
                    "#06B6D4",
                    "#8B5CF6",
                    "#14B8A6",
                    "#EC4899"
                ],
                borderWidth: 0
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: "#F8FAFC"
                    }
                }
            }
        }
    });
}