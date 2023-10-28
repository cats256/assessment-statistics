import "./index.css";
import React, { useState, useEffect } from "react";
import QuantileInput from "./QuantileInput";
import SummaryStatistics from "./SummaryStatistics";
import ModelPerformance from "./ModelPerformance";
import Plot from "./Plot";
import LogitNormalParameters from "./LogitNormalParameters";
import References from "./References";

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
    const [inputValues, setInputValues] = useState({
        minGrade: "0",
        maxGrade: "100",
        quantiles: { 0.25: "66", "0.50": "80", 0.75: "89" },
        cumulative: "",
        probability: "",
        quantile: "",
        value: "",
    });
    const [summaryTableExpanded, setSummaryTableExpanded] = useState(false);
    const [parametersTableExpanded, setParametersTableExpanded] = useState(false);
    const [rows, setRows] = useState([]);

    const handleAddRow = () => {
        if (inputValues.quantile) {
            // setRows([...rows, [inputValues.quantile, inputValues.value]]);
            // setInputValues({ ...inputValues, quantile: "", value: "" });
            const updatedInputValues = { ...inputValues };
            updatedInputValues["quantiles"][inputValues.quantile] = inputValues.value;
            setInputValues(updatedInputValues);
        }
    };

    const handleDeleteRowIndex = (index) => {
        const updatedRows = [...rows];
        updatedRows.splice(index, 1);
        setRows(updatedRows);
    };

    const handleDeleteQuantile = (quantile) => {
        const updatedInputValues = { ...inputValues };
        delete updatedInputValues["quantiles"][quantile];
        setInputValues(updatedInputValues);
        console.log(inputValues);
    };

    const handleChange = (event) => {
        if (isNaN(event.target.id)) {
            setInputValues({
                ...inputValues,
                [event.target.id]: event.target.value,
            });
        } else if (event.target.value === "") {
            const quantiles = { ...inputValues["quantiles"] };
            quantiles[event.target.id] = "";

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

        fetch("http://willb256.pythonanywhere.com/parameters", {
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
            <h2>Assessment Statistics</h2>
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
                            <QuantileInput label="Min Possible" id="minGrade" onChange={handleChange} />
                            <QuantileInput label="Max Possible" id="maxGrade" onChange={handleChange} />
                            {Object.entries(inputValues.quantiles).map(([quantile]) => (
                                <QuantileInput
                                    key={quantile}
                                    label={quantile}
                                    id={quantile}
                                    onChange={handleChange}
                                    onDelete={() => handleDeleteQuantile(quantile)}
                                />
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
                            <SummaryStatistics
                                parameters={parameters}
                                summaryTableExpanded={summaryTableExpanded}
                                toggleDisplaySummaryTable={toggleDisplaySummaryTable}
                            />
                            <ModelPerformance
                                parameters={parameters}
                                summaryTableExpanded={summaryTableExpanded}
                                toggleDisplaySummaryTable={toggleDisplaySummaryTable}
                            />
                        </tbody>
                    </table>
                </div>
                <div>
                    <Plot parameters={parameters} />
                    <LogitNormalParameters parameters={parameters} isExpanded={parametersTableExpanded} onToggle={setParametersTableExpanded} />
                    <br></br>
                    <br></br>
                    <References />
                </div>
            </div>
        </>
    );
};

export default App;
