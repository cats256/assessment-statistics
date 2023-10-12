import { Plot as PlotlyPlot } from "react-plotly.js";

const Plot = ({ parameters }) => {
    const trace1 = parameters
        ? {
              x: parameters.x_values.map((value) => value * 84),
              y: parameters.y_values,
              mode: "lines",
              name: "Normal Distribution",
              showlegend: true,
          }
        : {};

    const layout = {
        title: "Estimated Grade Distribution",
        xaxis: {
            title: "Grade",
        },
        yaxis: {
            title: "Probability Density Function",
        },
    };

    const data = [trace1];

    return <PlotlyPlot />;
};

export default Plot;
