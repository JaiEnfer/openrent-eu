import React, { useEffect, useState } from "react";
import "./App.css";

function getRiskLabel(score) {
  if (score >= 35) return "High Risk";
  if (score >= 20) return "Medium Risk";
  return "Low Risk";
}

function ListingsPage() {
  const [listings, setListings] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [maxRent, setMaxRent] = useState("");

  const loadListings = async (filters = {}) => {
    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams();

      if (filters.city) params.append("city", filters.city);
      if (filters.country) params.append("country", filters.country);
      if (filters.maxRent) params.append("max_rent", filters.maxRent);

      const url = `/api/listings/${params.toString() ? `?${params.toString()}` : ""}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error("Failed to fetch listings");
      }

      const data = await response.json();
      setListings(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadListings();
  }, []);

  const handleSearch = (event) => {
    event.preventDefault();
    loadListings({
      city: city.trim(),
      country: country.trim(),
      maxRent: maxRent.trim(),
    });
  };

  const handleReset = () => {
    setCity("");
    setCountry("");
    setMaxRent("");
    setSelectedIds([]);
    loadListings({});
  };

  const toggleCompare = (id) => {
    setSelectedIds((prev) => {
      if (prev.includes(id)) return prev.filter((item) => item !== id);
      if (prev.length >= 3) return prev;
      return [...prev, id];
    });
  };

  const selectedListings = listings.filter((item) => selectedIds.includes(item.id));

  return (
    <div className="page-content">
      <h2>Search Listings</h2>

      <form onSubmit={handleSearch} className="search-form">
        <div>
          <label>City</label>
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Berlin"
            className="input"
          />
        </div>

        <div>
          <label>Country</label>
          <input
            type="text"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            placeholder="Germany"
            className="input"
          />
        </div>

        <div>
          <label>Max Monthly Rent (€)</label>
          <input
            type="number"
            value={maxRent}
            onChange={(e) => setMaxRent(e.target.value)}
            placeholder="1000"
            className="input"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            Search
          </button>
          <button type="button" onClick={handleReset} className="btn">
            Reset
          </button>
        </div>
      </form>

      {selectedListings.length > 0 && (
        <div className="compare-panel">
          <h3>Compare Listings</h3>
          <div className="compare-grid" style={{ gridTemplateColumns: `repeat(${selectedListings.length}, 1fr)` }}>
            {selectedListings.map((listing) => (
              <div key={listing.id} className="compare-card">
                <h4>{listing.title}</h4>
                <p>
                  <strong>Location:</strong> {listing.city}, {listing.country}
                </p>
                <p>
                  <strong>Monthly Rent:</strong> €{listing.monthly_rent}
                </p>
                <p>
                  <strong>Deposit:</strong> €{listing.deposit || 0}
                </p>
                <p>
                  <strong>Move-in Cost:</strong> €{(listing.monthly_rent || 0) + (listing.deposit || 0)}
                </p>
                <p>
                  <strong>Bedrooms:</strong> {listing.bedrooms ?? "-"}
                </p>
                <p>
                  <strong>Furnished:</strong> {listing.furnished ? "Yes" : "No"}
                </p>
                <p>
                  <strong>Risk:</strong>{" "}
                  <span className={`risk ${getRiskLabel(listing.scam_score || 0).toLowerCase().replace(/\s/g, "-")}`}>
                    {getRiskLabel(listing.scam_score || 0)}
                  </span>
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && <p className="muted">Loading listings...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="listings-list">
          <p className="muted">
            <strong>{listings.length}</strong> listing(s) found
          </p>

          <div className="listings-grid">
            {listings.map((listing) => (
              <div key={listing.id} className="listing-card">
                <img className="listing-thumb" src={listing.image_url || '/placeholder.png'} alt={listing.title} />
                <div className="listing-header">
                  <h3 className="listing-title">{listing.title}</h3>
                  <label className="compare-label">
                    <input type="checkbox" checked={selectedIds.includes(listing.id)} onChange={() => toggleCompare(listing.id)} />
                    <span>Compare</span>
                  </label>
                </div>

                <div className="listing-meta">
                  <div>
                    <strong>Location:</strong> {listing.city}, {listing.country}
                  </div>
                  <div>
                    <strong>Rent:</strong> €{listing.monthly_rent}
                  </div>
                  <div>
                    <strong>Deposit:</strong> €{listing.deposit || 0}
                  </div>
                  <div>
                    <strong>Total move-in:</strong> €{(listing.monthly_rent || 0) + (listing.deposit || 0)}
                  </div>
                </div>

                <div className="listing-details">
                  <div>
                    <strong>Bedrooms:</strong> {listing.bedrooms ?? "-"}
                  </div>
                  <div>
                    <strong>Bathrooms:</strong> {listing.bathrooms ?? "-"}
                  </div>
                  <div>
                    <strong>Size:</strong> {listing.size_m2 ? `${listing.size_m2} m²` : "-"}
                  </div>
                </div>

                <p className="listing-desc">{listing.description || "No description available"}</p>

                <div className="listing-footer">
                  <div className="source">Source: {listing.source_name}</div>
                  <div className="risk">
                    Scam Score:{" "}
                    <span className={`risk ${getRiskLabel(listing.scam_score || 0).toLowerCase().replace(/\s/g, "-")}`}>{listing.scam_score ?? 0}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function UploadPage({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please choose a CSV file");
      return;
    }

    setUploading(true);
    setMessage("");
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/ingest/csv-upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setMessage(`Upload completed. Imported: ${data.imported_count}, Skipped: ${data.skipped_count}`);
      setFile(null);

      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      setError(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="page-content">
      <h2>Upload Agency CSV</h2>
      <p>Upload rental listings in CSV format.</p>

      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />

        <div style={{ marginTop: "1rem" }}>
          <button type="submit" disabled={uploading} className="btn btn-primary">
            {uploading ? "Uploading..." : "Upload CSV"}
          </button>
        </div>

        {message && (
          <p className="muted" style={{ marginTop: "1rem", color: "#16a34a" }}>
            {message}
          </p>
        )}
        {error && (
          <p className="error" style={{ marginTop: "1rem" }}>
            {error}
          </p>
        )}
      </form>

      <div style={{ marginTop: "2rem" }}>
        <h3>Required CSV columns</h3>
        <pre className="pre">
{`external_id,title,description,country,city,postal_code,street,monthly_rent,deposit,fees,bedrooms,bathrooms,size_m2,furnished,utilities_included,listing_url,contact_name,contact_type`}
        </pre>
      </div>
    </div>
  );
}

function App() {
  const [page, setPage] = useState("listings");
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="app-container">
      <header className="site-header">
        <div style={{display:'flex',alignItems:'center',gap:12}}>
          <img src="/logo.svg" alt="logo" style={{width:48,height:48}} />
          <div>
            <h1 className="site-title">OpenRent EU</h1>
            <p className="site-sub">Rental aggregation platform for Europe</p>
          </div>
        </div>

        <nav className="nav">
          <button onClick={() => setPage("listings")} className={`nav-btn ${page === "listings" ? "active" : ""}`}>
            Listings
          </button>
          <button onClick={() => setPage("upload")} className={`nav-btn ${page === "upload" ? "active" : ""}`}>
            Upload CSV
          </button>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-inner">
          <h2>Find better rentals across Europe</h2>
          <p className="hero-sub">Aggregated listings, scam scoring, and easy CSV import for agencies.</p>
          <div className="hero-ctas">
            <button className="btn btn-primary" onClick={() => setPage("listings")}>Browse Listings</button>
            <button className="btn" onClick={() => setPage("upload")}>Upload CSV</button>
          </div>
        </div>
      </section>

      {page === "listings" ? (
        <ListingsPage key={refreshKey} />
      ) : (
        <UploadPage
          onUploadSuccess={() => {
            setRefreshKey((prev) => prev + 1);
          }}
        />
      )}
    </div>
  );
}

export default App;
