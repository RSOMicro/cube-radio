import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./App.css";

// Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";

// ✅ Bootstrap JS BUNDLE (includes Modal + Popper)
import "bootstrap/dist/js/bootstrap.bundle.min.js";

import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <App />
    </StrictMode>
);
