import { disasterColors } from "../../utils/colors";

export default function Legend() {
  return (
    <div className="legend">
      <b>Disaster Types</b>
      {Object.entries(disasterColors).map(([type, color]) => (
        <div key={type} className="legend-item">
          <span
            className="color-box"
            style={{ background: color }}
          ></span>
          {type}
        </div>
      ))}
    </div>
  );
}