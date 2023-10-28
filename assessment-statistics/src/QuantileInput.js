import React from "react";

const QuantileInput = ({ label, id, value, onChange, onDelete }) => {
    return (
        <tr>
            <td>{label}</td>
            <td>
                <input
                    id={id}
                    type="text"
                    value={value}
                    onChange={onChange}
                    placeholder={label === "Min Possible" ? "0" : label === "Max Possible" ? "100" : ""}
                />
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
