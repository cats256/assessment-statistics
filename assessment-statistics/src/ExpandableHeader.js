import React from "react";

const ExpandableHeader = ({ title, isExpanded, toggleTableExpand }) => (
    <tr>
        <td colSpan="2">
            <b>{title}</b>
        </td>
        <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
            <button type="button" onClick={() => toggleTableExpand(!isExpanded)}>
                {isExpanded ? "collapse" : "expand"}
            </button>
        </td>
    </tr>
);

export default ExpandableHeader;
