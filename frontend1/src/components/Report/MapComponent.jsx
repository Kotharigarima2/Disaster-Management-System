import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Tooltip, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { disasterColors } from "../../utils/colors";

// Create custom pin
const createPinIcon = (color) =>
  new L.DivIcon({
    className: "custom-pin",
    html: `<div style="
      width:18px;
      height:18px;
      background:${color};
      border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);
      border:2px solid white;
    "></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 18],
  });

// MapType normalizer
const normalize = (v) => (v || "").toString().toLowerCase().replace(/_/g, " ").trim();
const mapType = (type) => {
  const t = normalize(type);
  if (t.includes("earth") || t.includes("quake")) return "earthquake";
  if (t.includes("flood")) return "flood";
  if (t.includes("fire") || t.includes("wild")) return "fire";
  if (t.includes("storm")) return "storm";
  if (t.includes("cyclone") || t.includes("hurricane") || t.includes("typhoon")) return "cyclone";
  if (t.includes("landslide") || t.includes("land slide") || t.includes("mudslide")) return "landslide";
  return null;
};

// 🔹 Component to programmatically move map
function MapController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.setView(center, zoom || 10, { animate: true }); // zoom in on new report
    }
  }, [center, zoom, map]);
  return null;
}

export default function MapComponent({ reports, highlightReport }) {
  // highlightReport = {lat, lng} of the newly submitted report
  const defaultCenter = [22.9734, 78.6569]; // default India center

  return (
    <MapContainer center={defaultCenter} zoom={5} className="map">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {highlightReport && <MapController center={[highlightReport.lat, highlightReport.lng]} zoom={10} />}

      {reports?.map((r, i) => {
        const type = mapType(r.disaster_type || r.type);
        if (!r.lat || !r.lng || !type) return null;

        return (
          <Marker
            key={i}
            position={[Number(r.lat), Number(r.lng)]}
            icon={createPinIcon(disasterColors[type] || "gray")}
          >
            <Tooltip>
              <b>{type.toUpperCase()}</b>
              <br />
              {r.description}
            </Tooltip>
          </Marker>
        );
      })}
    </MapContainer>
  );
}