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

    const handleDeleteRow = (e) => {
        const row = e.target.closest("tr");
        if (row) {
            row.remove();
        }
    };

    return (
        <>
            <h2>Fitting Grades</h2>
            <div className="statistics">
                <div>
                    <table style={{ border: "none" }}>
                        <tbody>
                            <tr>
                                <td>
                                    <b>Quantile</b>
                                </td>
                                <td>
                                    <b>Grade</b>
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <b>&nbsp;</b>
                                </td>
                            </tr>
                            <tr>
                                <td>Min Possible Grade</td>
                                <td>
                                    <input id="minGrade" type="text" value={inputValues.minGrade} onChange={handleChange} />
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>&nbsp;</td>
                            </tr>
                            <tr>
                                <td>Max Possible Grade</td>
                                <td>
                                    <input id="maxGrade" type="text" value={inputValues.maxGrade} onChange={handleChange} />
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>&nbsp;</td>
                            </tr>
                            <tr>
                                <td>0.25</td>
                                <td>
                                    <input id="lowerQuartile" type="text" value={inputValues.lowerQuartile} onChange={handleChange} />
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button">delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td>0.50</td>
                                <td>
                                    <input id="median" type="text" value={inputValues.median} onChange={handleChange} />
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button" onClick={handleDeleteRow}>
                                        delete
                                    </button>
                                </td>
                            </tr>
                            <tr>
                                <td>0.75</td>
                                <td>
                                    <input id="upperQuartile" type="text" value={inputValues.upperQuartile} onChange={handleChange} />
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button">delete</button>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                                    &nbsp;
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <b>Summary Statistics</b>
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>&nbsp;</td>
                            </tr>
                            <tr>
                                <td>Mean</td>
                                <td>{parameters && parameters.mean.toFixed(2)}</td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>Mean Squared Error</td>
                                <td>{parameters && parameters.mse.toFixed(2)}</td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>Mean Absolute Error</td>
                                <td>{parameters && parameters.mae.toFixed(2)}</td>
                                <td style={{ border: "none", backgroundColor: "transparent" }}>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div>
                    <Plot parameters={parameters} />
                    <div>
                        <table style={{ border: "none" }}>
                            <colgroup>
                                <col style={{ width: "40%" }} />
                                <col style={{ width: "40%" }} />
                                <col style={{ width: "20%" }} />
                            </colgroup>
                            <tbody>
                                <tr>
                                    <td colspan="2">
                                        <b>Logit-Normal Parameters</b>
                                    </td>
                                    <td style={{ border: "none", backgroundColor: "transparent" }}>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td>Mean</td>
                                    <td>{parameters && parameters.mean_logit_norm.toFixed(2)}</td>
                                    <td style={{ border: "none", backgroundColor: "transparent" }}>
                                        <button type="button">expand</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Standard Deviation</td>
                                    <td>{parameters && parameters.std_logit_norm.toFixed(2)}</td>
                                    <td style={{ border: "none", backgroundColor: "transparent" }}>
                                        <button type="button">expand</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </>
    );
};

export default App;
