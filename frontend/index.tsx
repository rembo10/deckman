import React from "react";
import ReactDOM from "react-dom";

import App from "./App";

const rootNodeId: string = "app";
const rootNode = document.getElementById(rootNodeId);

if (!rootNode) throw new Error(`Failed to find root element "${rootNodeId}"`);

const root = ReactDOM.createRoot(rootNode);

root.render(<App />);
