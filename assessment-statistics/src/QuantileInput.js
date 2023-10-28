import React from "react";

const QuantileInput = ({ label, id, value, onChange, onDelete }) => {
    const getPlaceholder = () => {
        const placeholders = {
            "Min Possible": "0",
            "Max Possible": "100",
            // 0.25: "66",
            // "0.50": "80",
            // 0.75: "89",
        };
        return placeholders[label] || placeholders[id] || "";
    };

    return (
        <tr>
            <td>{label}</td>
            <td>
                <input id={id} type="text" value={value} onChange={onChange} placeholder={getPlaceholder()} />
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
