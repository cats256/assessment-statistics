import React from "react";

import ParameterRow from "./ParameterRow";
import ExpandableHeader from "./ExpandableHeader";

const LogitNormalRow = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <>
            <ExpandableHeader
                title="Logit-Normal Parameters"
                isExpanded={isExpanded}
                toggleTableExpand={toggleTableExpand}
            />
            <ParameterRow name="Mean" value={parameters?.mean_logit_norm} isExpanded={isExpanded} />
            <ParameterRow name="Standard Deviation" value={parameters?.std_logit_norm} isExpanded={isExpanded} />
        </>
    );
};

export default LogitNormalRow;
