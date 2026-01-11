import { useEffect, useState } from "react";
import { useSessionContext } from "supertokens-auth-react/recipe/session";
import { getApiDomain, getRadioApiDomain } from "../config";

type Company = {
    tenant_id: number;
    tenant_name: string;
    tenant_size?: number;
};

export function useCompany() {
    const sessionContext = useSessionContext();
    const [company, setCompany] = useState<Company | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // SuperTokens is still loading session state
        if (sessionContext.loading) {
            return;
        }

        // User is not logged in
        if (!sessionContext.doesSessionExist) {
            setLoading(false);
            return;
        }

        async function fetchCompany() {
            try {
                const response = await fetch(getApiDomain() + "/api/user/me/company", {
                    credentials: "include", // IMPORTANT for SuperTokens
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch company");
                }

                const data = await response.json();
                setCompany(data);
            } catch (err) {
                console.error("Failed to load company", err);
            } finally {
                setLoading(false);
            }
        }

        fetchCompany();
    }, [sessionContext.loading, sessionContext.doesSessionExist]);

    return { company, loading };
}