import Hero from "../components/Hero/Hero";
import Features from "../components/Features/Features";
import "./Home.css";

function Home() {
  return (
    <div className="home">

      {/* background effects */}
      <div className="dots"></div>
      <div className="waves"></div>

      <Hero />
      <Features />

    </div>
  );
}

export default Home;