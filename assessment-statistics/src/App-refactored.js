import React, { useState, useEffect } from "react";
import "./index.css";
import Plot from "./Plot";
import QuantileInput from "./QuantileInput";
import SummaryStatistics from "./SummaryStatistics";
import ModelPerformance from "./ModelPerformance";
import LogitNormalParameters from "./LogitNormalParameters";
import References from "./References";

const App = () => {
    const [inputValues, setInputValues] = useState({
        minGrade: "0",
        maxGrade: "100",
        quantiles: { 0.25: "66", "0.50": "80", 0.75: "89" },
        cumulative: "",
        probability: "",
        quantile: "",
        value: "",
    });
    const [parameters, setParameters] = useState(null);
    const [summaryTableExpanded, setSummaryTableExpanded] = useState(false);
    const [parametersTableExpanded, setParametersTableExpanded] = useState(false);

    useEffect(() => {
        const { minGrade, maxGrade, quantiles } = inputValues;
        if (!minGrade || !maxGrade || Object.keys(quantiles).length <= 1) {
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

    const handleChange = (event) => {
        const { id, value } = event.target;
        if (isNaN(id)) {
            setInputValues({ ...inputValues, [id]: value });
        } else if (value === "") {
            const quantiles = { ...inputValues.quantiles };
            delete quantiles[id];
            setInputValues({ ...inputValues, quantiles });
        } else if (!isNaN(value)) {
            const quantiles = { ...inputValues.quantiles, [id]: value };
            setInputValues({ ...inputValues, quantiles });
        }
    };

    const handleAddRow = () => {
        if (inputValues.quantile) {
            const quantiles = { ...inputValues.quantiles, [inputValues.quantile]: inputValues.value };
            setInputValues({ ...inputValues, quantiles, quantile: "", value: "" });
        }
    };

    const handleDeleteRow = (quantile) => {
        const quantiles = { ...inputValues.quantiles };
        delete quantiles[quantile];
        setInputValues({ ...inputValues, quantiles });
    };

    return (
        <>
            <h2>Assessment Statistics</h2>
            <div className="statistics">
                <div>
                    <table>
                        <tbody>
                            <QuantileInput label="Min Possible" id="minGrade" value={inputValues.minGrade} onChange={handleChange} />
                            <QuantileInput label="Max Possible" id="maxGrade" value={inputValues.maxGrade} onChange={handleChange} />
                            {Object.entries(inputValues.quantiles).map(([quantile, value]) => (
                                <QuantileInput
                                    key={quantile}
                                    label={quantile}
                                    id={quantile}
                                    value={value}
                                    onChange={handleChange}
                                    onDelete={() => handleDeleteRow(quantile)}
                                />
                            ))}
                            <QuantileInput label="x" id="cumulative" value={inputValues.cumulative} onChange={handleChange} />
                            <QuantileInput label="P(x)" id="probability" value={inputValues.probability} onChange={handleChange} />
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
                        </tbody>
                    </table>
                </div>
                <div>
                    <Plot parameters={parameters} />
                    <SummaryStatistics parameters={parameters} isExpanded={summaryTableExpanded} onToggle={setSummaryTableExpanded} />
                    <ModelPerformance parameters={parameters} isExpanded={summaryTableExpanded} onToggle={setSummaryTableExpanded} />
                    <LogitNormalParameters parameters={parameters} isExpanded={parametersTableExpanded} onToggle={setParametersTableExpanded} />
                    <References />
                </div>
            </div>
        </>
    );
};

export default App;
