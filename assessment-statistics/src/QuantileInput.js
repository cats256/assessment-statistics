import React from "react";

const QuantileInput = ({ label, id, value, onChange, onDelete }) => {
    const placeholders = {
        "Min Possible": "0",
        "Max Possible": "100",
    };

    return (
        <tr>
            <td>{label}</td>
            <td>
                <input id={id} type="text" value={value} onChange={onChange} placeholder={placeholders[label] || ""} />
            </td>
            {onDelete && (
                <td>
                    <button type="button" onClick={onDelete}>
                        delete
                    </button>
                </td>
            )}
        </tr>
    );
};

export default QuantileInput;
