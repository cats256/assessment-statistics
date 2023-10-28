import React from "react";

const LogitNormalParameters = ({ parameters, isExpanded, onToggle }) => {
    return (
        <div>
            <table>
                <colgroup>
                    <col style={{ width: "40%" }} />
                    <col style={{ width: "40%" }} />
                    <col style={{ width: "20%" }} />
                </colgroup>
                <tbody>
                    <tr>
                        <td colSpan="2">
                            <b>Logit-Normal Parameters</b>
                        </td>
                        <td style={{ border: "none", backgroundColor: "transparent", padding: "0px" }}>
                            <button type="button" onClick={() => onToggle(!isExpanded)}>
                                {isExpanded ? "collapse" : "expand"}
                            </button>
                        </td>
                    </tr>
                    {isExpanded && (
                        <>
                            <tr>
                                <td>Mean</td>
                                <td>{parameters?.mean_logit_norm}</td>
                            </tr>
                            <tr>
                                <td>Standard Deviation</td>
                                <td>{parameters?.std_logit_norm}</td>
                            </tr>
                        </>
                    )}
                    {!isExpanded && (
                        <>
                            <tr>
                                <td>Mean</td>
                                <td>{parameters?.mean_logit_norm?.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Standard Deviation</td>
                                <td>{parameters?.std_logit_norm?.toFixed(2)}</td>
                            </tr>
                        </>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default LogitNormalParameters;
