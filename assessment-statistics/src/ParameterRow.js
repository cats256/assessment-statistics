import React from "react";

const ParameterRow = ({ name, value, isExpanded }) => (
    <tr>
        <td>{name}</td>
        <td>{isExpanded ? value : value?.toFixed(2)}</td>
    </tr>
);

export default ParameterRow;
