import "./index.css";
import React, { useState, useEffect } from "react";
import Plot from "./Plot";

const App = () => {
    const [parameters, setParameters] = useState(false);
    const [inputValues, setInputValues] = useState({ lowerQuartile: "", median: "", upperQuartile: "" });

    const handleChange = (event) => {
        setInputValues({
            ...inputValues,
            [event.target.id]: event.target.value,
        });
    };

    useEffect(() => {
        const { lowerQuartile, median, upperQuartile } = inputValues;

        if (!(lowerQuartile && median && upperQuartile)) {
            return;
        }

        fetch("/parameters", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(inputValues),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                setParameters(data);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }, [inputValues]);

    return (
        <>
            <h2>Fitting Grades</h2>
            <div className="statistics">
                {/* <form>
                    <div>
                        <label htmlFor="lowerQuartile">Lower Quartile:</label>
                        <input id="lowerQuartile" type="text" value={inputValues.lowerQuartile} onChange={handleChange} />
                    </div>
                    <div>
                        <label htmlFor="median">Median:</label>
                        <input id="median" type="text" value={inputValues.median} onChange={handleChange} />
                    </div>
                    <div>
                        <label htmlFor="upperQuartile">Upper Quartile:</label>
                        <input id="upperQuartile" type="text" value={inputValues.upperQuartile} onChange={handleChange} />
                    </div>
                </form> */}
                <div>
                    <form method="GET" id="data"></form>

                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <b>Quantile</b>
                                </td>
                                <td>
                                    <b>Grade</b>
                                </td>
                            </tr>
                            <tr>
                                <td>0.25</td>
                                <td>
                                    <input id="lowerQuartile" type="text" value={inputValues.lowerQuartile} onChange={handleChange} />
                                </td>
                                <td>
                                    <button type="button">delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td>0.50</td>
                                <td>
                                    <input id="median" type="text" value={inputValues.median} onChange={handleChange} />
                                </td>
                                <td>
                                    <button type="button">delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td>0.75</td>
                                <td>
                                    <input id="upperQuartile" type="text" value={inputValues.upperQuartile} onChange={handleChange} />
                                </td>
                                <td>
                                    <button type="button">delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <b>Summary Statistics</b>
                                </td>
                            </tr>
                            <tr>
                                <td>Mean</td>
                                <td>{parameters.mean}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>SSE</td>
                                <td>{parameters.sse_norm}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                {/* <div>
                    <div>Mean = {parameters.mean}</div>
                    <div>SSE = {parameters.sse_norm}</div>
                </div> */}

                <Plot parameters={parameters} />
                {/* <div>
                    <div>Mean = {parameters.mean}</div>
                    <div>SSE = {parameters.sse_norm}</div>
                </div> */}
            </div>
        </>
    );
};

export default App;
