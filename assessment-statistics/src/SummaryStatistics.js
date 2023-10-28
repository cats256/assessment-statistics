import React from "react";
import ExpandableHeader from "./ExpandableHeader";
import ParameterRow from "./ParameterRow";

function SummaryStatistics({ parameters, isExpanded, toggleTableExpand }) {
    return (
        <>
            <tr>
                <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                    &nbsp;
                </td>
            </tr>
            <ExpandableHeader title="Summary Statistics" isExpanded={isExpanded} toggleTableExpand={toggleTableExpand} />
            <ParameterRow name="Mean" value={parameters?.mean} isExpanded={isExpanded} />
            <ParameterRow name="P(X ≤ x)" value={parameters?.cumulative} isExpanded={isExpanded} />
            <ParameterRow name="x" value={parameters?.probability} isExpanded={isExpanded} />
        </>
    );
}

export default SummaryStatistics;
