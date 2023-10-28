import React from "react";

function ModelPerformance({ parameters, summaryTableExpanded, toggleDisplaySummaryTable }) {
    const renderParameter = (name, value) => (
        <tr>
            <td>{name}</td>
            <td>{summaryTableExpanded ? value : value?.toFixed(2)}</td>
        </tr>
    );

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
                    <button type="button" onClick={toggleDisplaySummaryTable}>
                        {summaryTableExpanded ? "collapse" : "expand"}
                    </button>
                </td>
            </tr>
            {renderParameter("RMSE", parameters?.rmse)}
            {renderParameter("MAE", parameters?.mae)}
            {renderParameter("R^2", parameters?.r_square)}
        </>
    );
}

export default ModelPerformance;
