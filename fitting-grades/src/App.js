import "./index.css";
import React, { useState, useEffect } from "react";
import Plot from "./Plot";

const DeleteButton = () => {
    const handleDeleteRow = (e) => {
        const row = e.target.closest("tr");
        if (row) {
            row.remove();
        }
    };

    return (
        <td>
            <button type="button" onClick={handleDeleteRow}>
                delete
            </button>
        </td>
    );
};

const App = () => {
    const [parameters, setParameters] = useState(false);
    const [inputValues, setInputValues] = useState({ quantiles: {} });
    const [summaryTableExpanded, setSummaryTableExpanded] = useState(false);
    const [parametersTableExpanded, setParametersTableExpanded] = useState(false);

    const handleChange = (event) => {
        if (isNaN(event.target.id)) {
            setInputValues({
                ...inputValues,
                [event.target.id]: event.target.value,
            });
        } else if (event.target.value !== "" && !isNaN(event.target.value)) {
            // remember to check whether inputvalue is >= than min and <= than max
            const quantiles = { ...inputValues["quantiles"], [event.target.id]: event.target.value };

            setInputValues({
                ...inputValues,
                quantiles: quantiles,
            });
        }
    };

    useEffect(() => {
        if (Object.keys(inputValues["quantiles"]).length <= 1) {
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

    const toggleDisplaySummaryTable = () => {
        setSummaryTableExpanded(!summaryTableExpanded);
    };

    const toggleDisplayParametersTable = () => {
        setParametersTableExpanded(!parametersTableExpanded);
    };

    return (
        <>
            <h2>Fitting Grades</h2>
            <div className="statistics">
                <div>
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
                                <td>Min Possible</td>
                                <td>
                                    <input id="minGrade" type="text" onChange={handleChange} />
                                </td>
                            </tr>
                            <tr>
                                <td>Max Possible</td>
                                <td>
                                    <input id="maxGrade" type="text" onChange={handleChange} />
                                </td>
                            </tr>
                            <tr>
                                <td>0.25</td>
                                <td>
                                    <input id="0.25" type="text" onChange={handleChange} />
                                </td>
                                <DeleteButton />
                            </tr>
                            <tr>
                                <td>0.50</td>
                                <td>
                                    <input id="0.50" type="text" onChange={handleChange} />
                                </td>
                                <DeleteButton />
                            </tr>
                            <tr>
                                <td>0.75</td>
                                <td>
                                    <input id="0.75" type="text" onChange={handleChange} />
                                </td>
                                <DeleteButton />
                            </tr>
                            <tr>
                                <td>x</td>
                                <td>
                                    <input id="cumulative" type="text" value={inputValues.cumulative} onChange={handleChange} />
                                </td>
                            </tr>
                            <tr>
                                <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                                    &nbsp;
                                </td>
                            </tr>
                            <tr>
                                <td colSpan="2">
                                    <b>Summary Statistics</b>
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
                                    <button type="button" onClick={toggleDisplaySummaryTable}>
                                        {summaryTableExpanded ? "collapse" : "expand"}
                                    </button>
                                </td>
                            </tr>
                            <tr>
                                <td>Mean</td>
                                <td>{summaryTableExpanded ? parameters?.mean : parameters?.mean?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>P(X ≤ x)</td>
                                <td></td>
                            </tr>
                            <tr>
                                <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                                    &nbsp;
                                </td>
                            </tr>
                            <tr>
                                <td colSpan="2">
                                    <b>Performance Metrics</b>
                                </td>
                                <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
                                    <button type="button" onClick={toggleDisplaySummaryTable}>
                                        {summaryTableExpanded ? "collapse" : "expand"}
                                    </button>
                                </td>
                            </tr>
                            <tr>
                                <td>RMSE</td>
                                <td>{summaryTableExpanded ? parameters?.rmse : parameters?.rmse?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>MAE</td>
                                <td>{summaryTableExpanded ? parameters?.mae : parameters?.mae?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>R^2</td>
                                <td>{summaryTableExpanded ? parameters?.r_square : parameters?.r_square?.toFixed(2)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div>
                    <Plot parameters={parameters} />
                    <div>
                        <table>
                            <colgroup>
                                <col style={{ width: "40%" }} />
                                <col style={{ width: "40%" }} />
                                <col style={{ width: "20%" }} />
                            </colgroup>
                            <tbody>
                                <tr>
                                    <td colSpan="2">
                                        <b>Logit-Normal Parameters</b>
                                    </td>
                                    <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
                                        <button type="button" onClick={toggleDisplayParametersTable}>
                                            {parametersTableExpanded ? "collapse" : "expand"}
                                        </button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Mean</td>
                                    <td>{parametersTableExpanded ? parameters?.mean_logit_norm : parameters?.mean_logit_norm?.toFixed(2)}</td>
                                </tr>
                                <tr>
                                    <td>Standard Deviation</td>
                                    <td>{parametersTableExpanded ? parameters?.std_logit_norm : parameters?.std_logit_norm?.toFixed(2)}</td>
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
