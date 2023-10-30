import "./index.css";
import React, { useState, useEffect } from "react";
import QuantileInput from "./QuantileInput";
import SummaryStatistics from "./SummaryStatistics";
import ModelPerformance from "./ModelPerformance";
import QuantileValues from "./QuantileValues";
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
            updatedInputValues["quantile"] = "";
            updatedInputValues["value"] = "";

            setInputValues(updatedInputValues);
        }
    };

    const handleDeleteQuantile = (quantile) => {
        const updatedInputValues = { ...inputValues };

        delete updatedInputValues["quantiles"][quantile];
        setInputValues(updatedInputValues);
    };

    const handleChange = (event) => {
        const { id, value } = event.target;
        let updatedInputValues = { ...inputValues };

        if (isNaN(id)) {
            updatedInputValues[id] = value;
        } else {
            updatedInputValues.quantiles = { ...updatedInputValues.quantiles, [id]: value || "" };
        }

        setInputValues(updatedInputValues);
    };

    useEffect(() => {
        if (!inputValues["minGrade"] || !inputValues["maxGrade"] || Object.keys(inputValues["quantiles"]).length <= 1) {
            return;
        }

        fetch("https://willb256.pythonanywhere.com/parameters", {
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
                            {Object.entries(inputValues.quantiles).map(([quantile, value]) => (
                                <QuantileInput
                                    key={quantile}
                                    label={quantile}
                                    id={quantile}
                                    value={value}
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
                            <QuantileValues
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
                    <References />
                </div>
            </div>
        </>
    );
};

export default App;
