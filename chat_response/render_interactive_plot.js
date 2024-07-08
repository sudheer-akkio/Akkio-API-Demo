document.addEventListener('DOMContentLoaded', () => {
    loadData('project_YxPegaOhKUCqsRLfzNtN_taskid_1006bf11-6285-4d01-8a80-71e8a63db1a9.txt');
});

async function loadData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.messages?.[1]?.table) {
            processTableData(data.messages[1].table);
        } else {
            processImageData(data);
        }
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function processTableData(tableData) {
    const headers = Object.keys(tableData[0]);
    const tableDataFormatted = [{
        type: 'table',
        header: {
            values: headers,
            align: "center",
            line: { width: 1, color: 'black' },
            fill: { color: "grey" },
            font: { family: "Arial", size: 12, color: "white" }
        },
        cells: {
            values: headers.map(header => tableData.map(row => row[header])),
            align: "center",
            line: { color: "black", width: 1 },
            fill: { color: ["white", "lightgrey"] },
            font: { family: "Arial", size: 11, color: ["black"] }
        }
    }];
    Plotly.newPlot('myDiv', tableDataFormatted);
}

function processImageData(data) {
    const imageDataOrJson = data.messages?.[1]?.images?.[0];
    if (imageDataOrJson.startsWith('data:image/png;base64,')) {
        displayImage(imageDataOrJson.split(',')[1]);
    } else {
        const plotData = JSON.parse(imageDataOrJson);
        renderPlotlyChart(plotData);
    }
}

function displayImage(base64Image) {
    const img = new Image();
    img.src = 'data:image/png;base64,' + base64Image;

    img.onload = () => {
        const layout = setupLayout(img.naturalWidth, img.naturalHeight, base64Image);
        const trace = setupTrace(img.naturalWidth, img.naturalHeight);
        renderPlot(trace, layout);
    };

    img.onerror = () => {
        console.error('Error loading image');
    };
}

function setupLayout(width, height, base64Image) {
    return {
        xaxis: { showgrid: false, zeroline: false, visible: false },
        yaxis: { showgrid: false, zeroline: false, visible: false, scaleanchor: 'x', scaleratio: 1 },
        images: [{
            x: 0, y: height, xref: "x", yref: "y", sizex: width, sizey: height, sizing: "stretch", opacity: 1, layer: "below", source: 'data:image/png;base64,' + base64Image
        }],
        width: 800,
        height: 600,
        margin: { l: 10, r: 10, b: 10, t: 10 },
    };
}

function setupTrace(width, height) {
    return {
        x: [0, width],
        y: [0, height],
        mode: 'markers',
        marker: { opacity: 0 },
        hoverinfo: 'none'
    };
}

function renderPlot(trace, layout) {
    Plotly.newPlot('myDiv', [trace], layout);
}

function renderPlotlyChart(plotData) {

    const { data, layout } = plotData;

    // Initialize data and layout properties based on Plotly docs
    // layout.title.text = "My Chart";
    layout.width = 800;
    layout.height = 600;
    layout.plot_bgcolor = 'white'; // Sets the background color to white
    layout.paper_bgcolor = 'white'; // Sets the surrounding paper color to white

     // Configure x and y grid lines (uncomment or adjust as needed)
     layout.xaxis = {
        ...layout.xaxis,
        showgrid: true, // Ensure grid lines are shown
        gridcolor: '#ccc', // Light grey grid lines
        zeroline: false // Disable the zero line if not needed
    };

    layout.yaxis = {
        ...layout.yaxis,
        showgrid: true,
        gridcolor: '#ccc',
        zeroline: false
    };

    // Render the chart with Plotly
    Plotly.newPlot('myDiv', data, layout);
}
