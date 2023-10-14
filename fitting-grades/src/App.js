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
                                <td>
                                    <b>&nbsp;</b>
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
                                <td colspan="3">&nbsp;</td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <b>Summary Statistics</b>
                                </td>
                                <td>&nbsp;</td>
                            </tr>
                            <tr>
                                <td>Mean</td>
                                <td>{parameters && parameters.mean.toFixed(2)}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>SD</td>
                                <td>{parameters && parameters.std}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>MSE</td>
                                <td>{parameters && parameters.mse_logit_norm}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                            <tr>
                                <td>MAE</td>
                                <td>{parameters && parameters.mae_logit_norm}</td>
                                <td>
                                    <button type="button">expand</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <Plot parameters={parameters} />
            </div>
        </>
    );
};

export default App;
