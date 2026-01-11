import { useCompany } from "../hooks/useCompany";

export default function CompanyBadge() {
    const { company, loading } = useCompany();

    if (loading) {
        return <li className="company-badge muted">Loading…</li>;
    }

    if (!company) {
        return null;
    }

    return (
        <li className="company-badge">
            <span className="company-label">Company:</span>{" "}
            <strong>{company.tenant_name}</strong>
        </li>
    );
}