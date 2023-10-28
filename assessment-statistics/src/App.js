import "./index.css";
import React, { useState, useEffect } from "react";
import QuantileInput from "./QuantileInput";
import SummaryStatistics from "./SummaryStatistics";
import ModelPerformance from "./ModelPerformance";
import Plot from "./Plot";
import LogitNormalParameters from "./LogitNormalParameters";
import References from "./References";

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

    const handleAddQuantile = () => {
        if (inputValues.quantile) {
            const updatedInputValues = { ...inputValues };
            updatedInputValues["quantiles"][inputValues.quantile] = inputValues.value;
            setInputValues(updatedInputValues);
        }
    };

    const handleDeleteQuantile = (quantile) => {
        const updatedInputValues = { ...inputValues };

        delete updatedInputValues["quantiles"][quantile];
        setInputValues(updatedInputValues);
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
                            <QuantileInput
                                label="x"
                                id="cumulative"
                                value={inputValues.cumulative}
                                onChange={handleChange}
                            />
                            <QuantileInput
                                label="P(x)"
                                id="probability"
                                value={inputValues.probability}
                                onChange={handleChange}
                            />
                            <tr>
                                <td>
                                    <input id="quantile" type="text" value={inputValues.quantile} onChange={handleChange} />
                                </td>
                                <td>
                                    <input id="value" type="text" value={inputValues.value} onChange={handleChange} />
                                </td>
                                <td>
                                    <button type="button" onClick={handleAddQuantile}>
                                        add
                                    </button>
                                </td>
                            </tr>
                            <SummaryStatistics
                                parameters={parameters}
                                isExpanded={summaryTableExpanded}
                                toggleTableExpand={setSummaryTableExpanded}
                            />
                            <ModelPerformance
                                parameters={parameters}
                                isExpanded={summaryTableExpanded}
                                toggleTableExpand={setSummaryTableExpanded}
                            />
                        </tbody>
                    </table>
                </div>
                <div>
                    <Plot parameters={parameters} />
                    <LogitNormalParameters
                        parameters={parameters}
                        isExpanded={parametersTableExpanded}
                        toggleTableExpand={setParametersTableExpanded}
                    />
                    <br></br>
                    <br></br>
                    <References />
                </div>
            </div>
        </>
    );
};

export default App;
