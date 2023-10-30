import React from "react";
import ParameterRow from "./ParameterRow";
import TransparentRow from "./TransparentRow";

const QuantileValues = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <>
            <TransparentRow />
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
