// Results
import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

import Navbar from "../components/header";
import Footer from "../components/footer";

import "../styles/results.css";

let pageTitle = "Results";

function Results(props) {
  const location = useLocation();
  const { latestTest, latestResult } = location.state || {};

  useEffect(() => {
    console.log(`Latest Test: ${latestTest}`);
    console.log(`Latest Result:\n${JSON.stringify(latestResult, null, 2)}`);
  }, [latestTest, latestResult]);

  return (
    <div id="root">
      <Navbar pageTitle="" />
      <div className="page-content">
        <h1 className="title">Results</h1>
        <p className="description">
          Here your test results about: {latestTest}
        </p>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default Results;
