import { default as PlotlyPlot } from "react-plotly.js";

const Plot = ({ parameters }) => {
    const layout = {
        title: "Estimated Grade Distribution",
        xaxis: {
            title: "Grade",
        },
        yaxis: {
            title: "Probability Density Function",
        },
        width: 800,
        height: 500,
    };

    const config = { responsive: true };

    let data = [];

    if (parameters) {
        const trace1 = {
            x: parameters.x_values,
            y: parameters.y_values,
            mode: "lines",
            name: "Scaled Logit-Normal",
            showlegend: true,
        };

        const trace2 = {
            x: parameters.observed_values,
            y: parameters.observed_y_values,
            mode: "markers",
            name: "Observed Quantiles",
            showlegend: true,
        };

        const trace3 = {
            x: parameters.expected_values,
            y: parameters.expected_y_values,
            mode: "markers",
            name: "Expected Quantiles",
            showlegend: true,
        };

        data = [trace1, trace2, trace3];
    }

    return <PlotlyPlot data={data} layout={layout} config={config} />;
};

export default Plot;
