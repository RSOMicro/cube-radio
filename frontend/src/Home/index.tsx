import { Link } from "react-router-dom";
import { useSessionContext } from "supertokens-auth-react/recipe/session";

export default function Home() {
    const session = useSessionContext();

    if (session.loading) {
        return null;
    }

    return (
        <>
            <section className="main-container">
                <div className="inner-content">
                    <h1>
                        <strong>Radio Station Player made with Cubernetes </strong>
                    </h1>
                    <div>
                        {session.doesSessionExist ? (
                            <p>
                                You're signed in already, <br /> check out the Radio Stations! 👇
                            </p>
                        ) : (
                            <p>Sign-in to continue</p>
                        )}
                    </div>
                    <nav className="buttons">
                        {session.doesSessionExist ? (
                            <Link to="/dashboard" className="dashboard-button">
                                Dashboard
                            </Link>
                        ) : (
                            <Link to="/auth" className="dashboard-button">
                                Sign-up / Login
                            </Link>
                        )}
                    </nav>
                </div>
            </section>
        </>
    );
}
