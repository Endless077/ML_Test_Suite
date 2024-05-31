import React from "react";
import Navbar from "../components/header";
import Footer from "../components/footer";

import "../styles/homepage.css";

let pageTitle = "Adversarial Robustness Toolbox";

function HomePage() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <h1 className="title">ML Test Suite</h1>
        <p className="description">
          A test suite for Machine Learning models based on{" "}
          <a href="https://github.com/Trusted-AI/adversarial-robustness-toolbox">
            Adversarial Robustness Toolbox (ART)
          </a>
          , a Python library for Machine Learning security.
        </p>
        <hr />
        <div className="features">
          <div className="feature">
            <div className="feature-title">Upload</div>
            <div className="feature-description">
              You can upload your own model and a personal dataset or you can
              use standard predefined datasets such as MNIST, CIFAR-10, and
              CIFAR-100.
            </div>
          </div>
          <div className="feature">
            <div className="feature-title">Test</div>
            <div className="feature-description">
              Apply various attacks to test the robustness of your model.
              Optionally, apply associated defenses to mitigate the impact of
              attacks.
            </div>
          </div>
          <div className="feature">
            <div className="feature-title">Results</div>
            <div className="feature-description">
              View test results like accuracy, loss, precision and any other
              percentage, logs generated, and any plotting based on the test
              chosen.
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default HomePage;
