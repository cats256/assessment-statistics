import React from "react";
import ParameterRow from "./ParameterRow";

const QuantileValues = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <>
            <tr>
                <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                    &nbsp;
                </td>
            </tr>
            <tr>
                <td colSpan="1">
                    <b>Observed</b>
                </td>
                <td>
                    <b>Predicted</b>
                </td>
                <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
                    <button type="button" onClick={() => toggleTableExpand(!isExpanded)}>
                        {isExpanded ? "collapse" : "expand"}
                    </button>
                </td>
            </tr>
            {parameters &&
                parameters["observed_values"].map((value, index) => (
                    <ParameterRow name={value} value={parameters["expected_values"][index]} isExpanded={isExpanded} />
                ))}
        </>
    );
};

export default QuantileValues;
