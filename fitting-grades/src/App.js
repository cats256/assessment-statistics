import "./index.css";
import React, { useState, useEffect } from "react";
import Plot from "./Plot";

const handleDeleteRow = (event) => {
    const row = event.target.closest("tr");
    if (row) {
        row.remove();
    }
};

const DeleteButton = () => {
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
    const [rows, setRows] = useState([]);

    const handleAddRow = () => {
        if (inputValues.quantile) {
            setRows([...rows, [inputValues.quantile, inputValues.value]]);
            setInputValues({ ...inputValues, quantile: "", value: "" });
        }
    };

    const handleDeleteRowIndex = (index) => {
        const updatedRows = [...rows];
        updatedRows.splice(index, 1);
        setRows(updatedRows);
    };

    const handleChange = (event) => {
        if (isNaN(event.target.id)) {
            setInputValues({
                ...inputValues,
                [event.target.id]: event.target.value,
            });
        } else if (event.target.value === "") {
            const quantiles = { ...inputValues["quantiles"] };
            delete quantiles[event.target.id];

            setInputValues({
                ...inputValues,
                quantiles: quantiles,
            });
        } else if (!isNaN(event.target.value)) {
            const quantiles = { ...inputValues["quantiles"], [event.target.id]: event.target.value };

            setInputValues({
                ...inputValues,
                quantiles: quantiles,
            });
        }
    };

    useEffect(() => {
        if (!inputValues["minGrade"] || !inputValues["maxGrade"] || Object.keys(inputValues["quantiles"]).length <= 1) {
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
                            {rows.map((row, index) => (
                                <tr key={index}>
                                    <td>{row[0]}</td>
                                    <td>
                                        <input id={row[0]} type="text" onChange={handleChange} />
                                    </td>
                                    <td>
                                        <button type="button" onClick={() => handleDeleteRowIndex(index)}>
                                            delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            <tr>
                                <td>x</td>
                                <td>
                                    <input id="cumulative" type="text" value={inputValues.cumulative} onChange={handleChange} />
                                </td>
                            </tr>
                            <tr>
                                <td>P(x)</td>
                                <td>
                                    <input id="probability" type="text" value={inputValues.probabillity} onChange={handleChange} />
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <input id="quantile" type="text" value={inputValues.quantile} onChange={handleChange} />
                                </td>
                                <td>
                                    <input id="value" type="text" value={inputValues.value} onChange={handleChange} />
                                </td>
                                <td>
                                    <button type="button" onClick={handleAddRow}>
                                        add
                                    </button>
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
                                <td>{summaryTableExpanded ? parameters?.cumulative : parameters?.cumulative?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>x</td>
                                <td>{summaryTableExpanded ? parameters?.probability : parameters?.probability?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                                    &nbsp;
                                </td>
                            </tr>
                            <tr>
                                <td colSpan="2">
                                    <b>Model Performance</b>
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
