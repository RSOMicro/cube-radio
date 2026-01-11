import { useState } from "react";

type StationFormProps = {
    initialData?: {
        name?: string;
        description?: string;
        logo_url?: string;
        stream_url?: string;
    };
    onSubmit: (data: {
        name: string;
        description: string;
        logo_url: string;
        stream_url: string;
    }) => Promise<void>;
};

export default function StationForm({ initialData = {}, onSubmit }: StationFormProps) {
    const [form, setForm] = useState({
        name: initialData.name || "",
        description: initialData.description || "",
        logo_url: initialData.logo_url || "",
        stream_url: initialData.stream_url || "",
    });

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        await onSubmit(form);
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                className="form-control mb-2"
                name="name"
                placeholder="Station name"
                value={form.name}
                onChange={handleChange}
                required
            />
            <input
                className="form-control mb-2"
                name="description"
                placeholder="Description"
                value={form.description}
                onChange={handleChange}
                required
            />
            <input
                className="form-control mb-2"
                name="logo_url"
                placeholder="Logo URL"
                value={form.logo_url}
                onChange={handleChange}
                required
            />
            <input
                className="form-control mb-3"
                name="stream_url"
                placeholder="Stream URL"
                value={form.stream_url}
                onChange={handleChange}
                required
            />

            <button className="btn btn-primary w-100" type="submit">
                Save
            </button>
        </form>
    );
}