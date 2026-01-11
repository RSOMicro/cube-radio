import { useSessionContext, signOut } from "supertokens-auth-react/recipe/session";
import { useNavigate } from "react-router-dom";
import { getApiDomain, getRadioApiDomain, getRadioRmoteApiDomain } from "../config";
import { useEffect, useState } from "react";
import StationForm from "./StationForm"; 

export default function Dashboard() {
    const navigate = useNavigate();
    const sessionContext = useSessionContext();

    const [stations, setStations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
	const [jwt, setJwt] = useState<string>(""); 
	const [displayName, setDisplayName] = useState<string | null>(null);
	const [selectedStationId, setSelectedStationId] = useState<string>("");
	
	const [addError, setAddError] = useState<string | null>(null);
	const [editError, setEditError] = useState<string | null>(null);
	const [removeError, setRemoveError] = useState<string | null>(null);
	
	const [loadingMore, setLoadingMore] = useState(false);
	const [loadMoreError, setLoadMoreError] = useState<string | null>(null);
	const [remoteLoaded, setRemoteLoaded] = useState(false);

    useEffect(() => {
        async function init() {
            try {
                const sessionRes = await fetch(getApiDomain() + "/api/user/sessioninfo");
                if (!sessionRes.ok) throw new Error("Session fetch failed");

                const sessionData = await sessionRes.json();
                setJwt(sessionData.jwt);

                const decoded = decodeJwt(sessionData.jwt);
                if (decoded?.name && decoded?.lastname) {
                    setDisplayName(`${decoded.name} ${decoded.lastname}`);
                }

                await loadStations(sessionData.jwt);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        init();
    }, []);

    async function loadStations(token: string) {
        const res = await fetch(getRadioApiDomain() + "/api/radio/stations/", {
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error("Failed to load stations");

        setStations(await res.json());
    }
	
    async function loadRemoteStations() {
        setLoadingMore(true);
        setLoadMoreError(null);
    
        try {
            const res = await fetch(
                getRadioRmoteApiDomain() + "/api/radio/remote/", 
                { credentials: 'omit' } // no credentials
            );
    
            if (!res.ok) {
                throw new Error("Failed to load remote stations");
            }
    
            const remoteStations = await res.json();
    
            setStations((prev) => {
                const existingIds = new Set(prev.map((s: any) => s._id));
                const newStations = remoteStations.filter(
                    (s: any) => !existingIds.has(s._id)
                );
                return [...prev, ...newStations];
            });
    
            // Mark remote stations as loaded
            setRemoteLoaded(true);
        } catch (err: any) {
            setLoadMoreError(err.message || "Could not load more stations");
        } finally {
            setLoadingMore(false);
        }
    }

    function decodeJwt(token: string) {
        try {
            return JSON.parse(atob(token.split(".")[1]));
        } catch {
            return null;
        }
    }

    async function logoutClicked() {
        await signOut();
        navigate("/");
    }

    const selectedStation = stations.find((s) => s._id === selectedStationId);
	
	function decodeJwt(token: string) {
		try {
			const payload = token.split(".")[1];
			return JSON.parse(atob(payload));
		} catch {
			return null;
		}
	}

    return (
        <div className="main-container">
            <header className="dashboard-header">
                <h1>Stations for user:</h1>
                <span className="user-info">&nbsp;
                    <span className="user-id">{displayName ?? sessionContext.userId}</span>
                    <button onClick={logoutClicked}>Logout</button>
                </span>
            </header>

            {loading && (
                <div className="spinner-container">
                    <img src="/assets/images/spinner.gif" alt="Loading..." />
                </div>
            )}

            {!loading && error && (
                <div className="spinner-container">
                    <img src="/assets/images/spinner.gif" alt="Error loading" />
                </div>
            )}

            {!loading && !error && (
            <>
                <div className="stations-grid">
                    {stations.map((station) => (
                        <div key={station._id} className="station-card">
                            <div className="logo-wrapper">
                                <img
                                    src={station.logo_url}
                                    alt={station.name}
                                    onError={(e: any) => {
                                        e.target.src = "/assets/images/radio-placeholder.png";
                                    }}
                                />
                            </div>
            
                            <h3>{station.name}</h3>
                            <p>{station.description}</p>
            
                            <a
                                href={station.stream_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="listen-btn"
                            >
                                ▶ Listen
                            </a>
                        </div>
                    ))}
                </div>
            
                {/* Load more button */}
                <div className="text-center mt-4">
                    {loadMoreError && (
                        <div className="alert alert-danger mb-2">
                            {loadMoreError}
                        </div>
                    )}
            
                    {!remoteLoaded && (
                         <button
                             className="btn btn-success"
                             onClick={loadRemoteStations}
                             disabled={loadingMore}
                         >
                             {loadingMore ? "Loading…" : "Load more stations"}
                         </button>
                     )}
                </div>
            </>
            )}
			
		{/* Add Edit Remote Radio station components */}
		
		{/* ADD */}
        <Modal id="addStationModal" title="Add Station">
		{addError && <div className="alert alert-danger">{addError}</div>}
            <StationForm
				onSubmit={async (data) => {
        				setAddError(null);
        				
        				try {
        				    const res = await fetch(getRadioApiDomain() + "/api/radio/stations/", {
        				        method: "PUT",
        				        headers: {
        				            "Content-Type": "application/json",
        				            Authorization: `Bearer ${jwt}`,
        				        },
        				        body: JSON.stringify(data),
        				    });
        				
        				    if (!res.ok) {
        				        throw new Error("Failed to add station");
        				    }
        				
        				    await loadStations(jwt);
        				    closeModal("addStationModal");
        				} catch (err: any) {
        				    setAddError(err.message || "Station could not be added");
        				}
				}}
            />
        </Modal>
		
		{/* EDIT */}
		<Modal id="editStationModal" title="Edit Station">
		{editError && (
		    <div className="alert alert-danger mb-3">
		        {editError}
		    </div>
		)}
		
		<select
		    className="form-select mb-3"
		    value={selectedStationId}
		    onChange={(e) => {
		        setEditError(null);
		        setSelectedStationId(e.target.value);
		    }}
		>
		    <option value="">Select station</option>
		    {stations.map((s) => (
		        <option key={s._id} value={s._id}>
		            {s.name}
		        </option>
		    ))}
		</select>
		
		{selectedStation && (
		    <StationForm
		        initialData={selectedStation}
		        onSubmit={async (data) => {
		            setEditError(null);
		
		            try {
		                const res = await fetch(
		                    getRadioApiDomain() + `/api/radio/stations/${selectedStation._id}`,
		                    {
		                        method: "PATCH",
		                        headers: {
		                            "Content-Type": "application/json",
		                            Authorization: `Bearer ${jwt}`,
		                        },
		                        body: JSON.stringify(data),
		                    }
		                );
		
		                if (!res.ok) {
		                    throw new Error("Station could not be updated");
		                }
		
		                await loadStations(jwt);
		                closeModal("editStationModal");
		            } catch (err: any) {
		                setEditError(err.message || "Failed to update station");
		            }
		        }}
		    />
		)}
</Modal>
		
		{/* REMOVE */}
        <Modal id="removeStationModal" title="Remove Station">
        {removeError && (
            <div className="alert alert-danger mb-3">
                {removeError}
            </div>
        )}
        
        <select
            className="form-select mb-3"
            value={selectedStationId}
            onChange={(e) => {
                setRemoveError(null);
                setSelectedStationId(e.target.value);
            }}
        >
            <option value="">Select station</option>
            {stations.map((s) => (
                <option key={s._id} value={s._id}>
                    {s.name}
                </option>
            ))}
        </select>
        
        <button
            className="btn btn-danger w-100"
            disabled={!selectedStationId}
            onClick={async () => {
                setRemoveError(null);
        
                try {
                    const res = await fetch(
                        getRadioApiDomain() + `/api/radio/stations/${selectedStationId}`,
                        {
                            method: "DELETE",
                            headers: {
                                Authorization: `Bearer ${jwt}`,
                            },
                        }
                    );
        
                    if (!res.ok) {
                        throw new Error("Station could not be removed");
                    }
        
                    setSelectedStationId("");
                    await loadStations(jwt);
                    closeModal("removeStationModal");
                } catch (err: any) {
                    setRemoveError(err.message || "Failed to remove station");
                }
            }}
        >
            Confirm Delete
        </button>
    </Modal>
			
        </div>
    );
}

/* Simple reusable modal */
function Modal({ id, title, children }: any) {
    return (
        <div className="modal fade" id={id} tabIndex={-1}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">{title}</h5>
                        <button className="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div className="modal-body">{children}</div>
                </div>
            </div>
        </div>
    );
}

function closeModal(modalId: string) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl) return;

    const modalInstance = (window as any).bootstrap.Modal.getOrCreateInstance(modalEl);
    modalInstance.hide();
}