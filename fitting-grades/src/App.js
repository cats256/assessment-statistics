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
            <div>
                <form>
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
                </form>
            </div>
            <Plot parameters={parameters} />
            <div>
                Mean = {parameters.mean}&nbsp;&nbsp;&nbsp;&nbsp;Sum Squared Error = {parameters.sse_norm}
            </div>
        </>
    );
};

export default App;
