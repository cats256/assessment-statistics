import React from "react";
import ParameterRow from "./ParameterRow";
import ExpandableHeader from "./ExpandableHeader";
import TransparentRow from "./TransparentRow";

const ModelPerformance = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <>
            <TransparentRow />
            <ExpandableHeader title="Model Performance" isExpanded={isExpanded} toggleTableExpand={toggleTableExpand} />
            <ParameterRow name="RMSE" value={parameters?.rmse} isExpanded={isExpanded} />
            <ParameterRow name="MAE" value={parameters?.mae} isExpanded={isExpanded} />
            <ParameterRow name="R^2" value={parameters?.r_square} isExpanded={isExpanded} />
        </>
    );
};

export default ModelPerformance;
