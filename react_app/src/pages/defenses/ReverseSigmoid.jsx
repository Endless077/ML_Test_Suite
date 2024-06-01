// Reverse Sigmoid Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/defenses/ReverseSigmoid.css";

let pageTitle = "Reverse Sigmoid";

function ReverseSigmoid() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of a postprocessor based on adding the Reverse Sigmoid
          perturbation to classifier output.
        </p>
        <a href="https://en.wikipedia.org/wiki/Sigmoid_function">
          What is a Sigmoid function?
        </a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default ReverseSigmoid;
