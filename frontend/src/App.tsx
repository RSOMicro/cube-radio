import SuperTokens, { SuperTokensWrapper } from "supertokens-auth-react";
import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui";
import { SessionAuth } from "supertokens-auth-react/recipe/session";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import * as ReactRouter from "react-router-dom";
import Dashboard from "./Dashboard";
import { PreBuiltUIList, SuperTokensConfig, ComponentWrapper } from "./config";
import CompanyBadge from "./components/CompanyBadge";
import Home from "./Home";

// Initialize SuperTokens - ideally in the global scope
SuperTokens.init(SuperTokensConfig);

function App() {
    return (
        <SuperTokensWrapper>
            <BrowserRouter>
                <main className="App app-container">
                    <header>
                        <nav className="header-container">
                            <Link to="/">
                                <img src="/Radio.svg" alt="Radio" />
                            </Link>
							<SessionAuth>
                                <div className="station-actions">
                                    <button className="btn btn-success" data-bs-toggle="modal" data-bs-target="#addStationModal">
                                        Add Station
                                    </button>
                                    <button className="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editStationModal">
                                        Edit Station
                                    </button>
                                    <button className="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeStationModal">
                                        Remove Station
                                    </button>
                                </div>
							</SessionAuth>
                            <ul className="header-container-right">
                                    <SessionAuth>
                                         <CompanyBadge />
                                    </SessionAuth>
                            </ul>
                        </nav>
                    </header>
                    <div className="fill" id="home-container">
                        <ComponentWrapper>
                            <Routes>
                                <Route path="/" element={<Home />} />
                                {/* This shows the login UI on "/auth" route */}
                                {getSuperTokensRoutesForReactRouterDom(ReactRouter, PreBuiltUIList)}

                                {/* This protects the "/dashboard" route so that it shows
                                <Dashboard /> only if the user is logged in.
                                Else it redirects the user to "/auth" */}
                                <Route
                                    path="/dashboard"
                                    element={
                                        <SessionAuth>
                                            <Dashboard />
                                        </SessionAuth>
                                    }
                                />
                            </Routes>
                        </ComponentWrapper>
                        <footer>
                            Built with 💔 by Mitja with the help of 😈
                        </footer>
                        <img className="separator-line" src="/assets/images/separator-line.svg" alt="separator" />
                    </div>
                </main>
            </BrowserRouter>
        </SuperTokensWrapper>
    );
}

export default App;
