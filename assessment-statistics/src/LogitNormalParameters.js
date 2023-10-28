import React from "react";
import ExpandableHeader from "./ExpandableHeader";
import ParameterRow from "./ParameterRow";

const LogitNormalParameters = ({ parameters, isExpanded, toggleTableExpand }) => {
    return (
        <div>
            <table>
                <colgroup>
                    <col style={{ width: "40%" }} />
                    <col style={{ width: "40%" }} />
                </colgroup>
                <tbody>
                    <ExpandableHeader
                        title="Logit-Normal Parameters"
                        isExpanded={isExpanded}
                        toggleTableExpand={toggleTableExpand}
                    />
                    <ParameterRow name="Mean" value={parameters?.mean_logit_norm} isExpanded={isExpanded} />
                    <ParameterRow name="Standard Deviation" value={parameters?.std_logit_norm} isExpanded={isExpanded} />
                </tbody>
            </table>
        </div>
    );
};

export default LogitNormalParameters;
