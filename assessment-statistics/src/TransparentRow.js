import React from "react";

const TransparentRow = () => {
    return (
        <tr>
            <td colSpan="3" style={{ border: "none", backgroundColor: "transparent" }}>
                &nbsp;
            </td>
        </tr>
    );
};

export default TransparentRow;
