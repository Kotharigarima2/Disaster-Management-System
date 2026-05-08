import { useNavigate } from "react-router-dom";
import "./BackButton.css";

function BackButton() {

  const navigate = useNavigate();

  return (

    <button
      className="back-btn"
      onClick={() => navigate("/")}
    >
      ←
    </button>

  );
}

export default BackButton;