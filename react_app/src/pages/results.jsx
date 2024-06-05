import React from "react";
import Navbar from "../components/header";
import Footer from "../components/footer";

import "../styles/results.css";

let pageTitle = "Adversarial Robustness Toolbox";

function Results(props) {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <h1 className="title">Results</h1>
        <p className="description">
        Here your test results about: {props.previousTest}
        </p>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default Results;
