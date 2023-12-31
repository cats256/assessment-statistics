import { default as PlotlyPlot } from "react-plotly.js";

const Plot = ({ parameters, width }) => {
    const layout = {
        title: "Estimated Grade Distribution",
        xaxis: {
            title: "Grade",
        },
        yaxis: {
            title: "Probability Density Function",
        },
        responsive: true,
        useResizeHandler: true,
        autosize: true,
        font: {
            family: "Inter",
            size: width / 128,
        },
    };

    const config = { responsive: true };

    let data = [];

    if (parameters) {
        const trace1 = {
            x: parameters.x_values,
            y: parameters.y_values,
            mode: "lines",
            name: "Scaled Logit-Normal",
            showlegend: false,
        };

        const trace2 = {
            x: parameters.observed_values,
            y: parameters.observed_y_values,
            mode: "markers",
            name: "Observed Quantiles",
            showlegend: true,
            marker: {
                size: 6,
            },
        };

        const trace3 = {
            x: parameters.expected_values,
            y: parameters.expected_y_values,
            mode: "markers",
            name: "Expected Quantiles",
            showlegend: true,
            marker: {
                size: 6,
            },
        };

        data = [trace1, trace2, trace3];
    }

    return <PlotlyPlot data={data} layout={layout} config={config} style={{ width: "100%", aspectRatio: "1.61803" }} />;
};

export default Plot;
