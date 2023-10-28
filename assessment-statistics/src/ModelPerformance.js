import React from "react";
import ParameterRow from "./ParameterRow";

const ModelPerformance = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <>
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
                    <button type="button" onClick={() => toggleTableExpand(!isExpanded)}>
                        {isExpanded ? "collapse" : "expand"}
                    </button>
                </td>
            </tr>
            <ParameterRow name="RMSE" value={parameters?.rmse} isExpanded={isExpanded} />
            <ParameterRow name="MAE" value={parameters?.mae} isExpanded={isExpanded} />
            <ParameterRow name="R^2" value={parameters?.r_square} isExpanded={isExpanded} />
        </>
    );
};

export default ModelPerformance;
