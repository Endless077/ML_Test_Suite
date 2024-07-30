// Results
import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import Navbar from "../components/header";
import Footer from "../components/footer";

import "../styles/results.css";

let pageTitle = "Adversarial Robustness Toolbox";

function Results() {
  const location = useLocation();
  const { latestTest, latestResult } = location.state || {};

  const [results, setResults] = useState();

  useEffect(() => {
    console.log(`Latest Test: ${latestTest}`);
    console.log(`Latest Result:\n${JSON.stringify(latestResult, null, 2)}`);

    const jsonString = JSON.stringify(latestResult, null, 2);
    setResults(JSON.parse(jsonString));
  }, [latestTest, latestResult]);

  const renderLayerInfo = (layers) => {
    return layers.map((layer, index) => (
      <li key={index}>
        <strong>{layer.name}</strong>
        <ul>
          <li>
            <strong>Output Shape:</strong> {JSON.stringify(layer.output_shape)}
          </li>
          <li>
            <strong>Num Params:</strong> {layer.num_params}
          </li>
          <li>
            <strong>Trainable:</strong> {layer.trainable ? "Yes" : "No"}
          </li>
        </ul>
      </li>
    ));
  };

  const renderNestedObject = (obj) => {
    return (
      <ul>
        {Object.keys(obj).map((key, index) => (
          <li key={index} className="test-summary-list">
            <strong>{key}:</strong>
            {typeof obj[key] === "object" && obj[key] !== null
              ? renderNestedObject(obj[key])
              : ` ${obj[key]}`}
          </li>
        ))}
      </ul>
    );
  };

  const excludeSummary = (obj) => {
    const { summary, ...rest } = obj;
    return rest;
  };

  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          For more detailed results, please refer to the summary folder on the
          server storage or the test logs located in the logs folder.
          <br />
          Here your test results about: {latestTest}
        </p>
        <hr />
        <div className="results-container">
          <div className="results-section">
            <h2 className="section-title">Test Results</h2>
            <div className="section-content">
              { results && renderNestedObject(excludeSummary(results)) }
            </div>
          </div>
          <div className="results-section">
            <h2 className="section-title">Model Summary</h2>
            {results && (
              <div className="section-content">
                <p>
                  <strong>Layers Count:</strong> {results.summary.layers_count}
                </p>
                <p>
                  <strong>Layers:</strong>
                </p>
                <ul>{renderLayerInfo(results.summary.layers)}</ul>
                <p>
                  <strong>Total Params:</strong> {results.summary.total_params}
                </p>
                <p>
                  <strong>Trainable Params:</strong>{" "}
                  {results.summary.trainable_params}
                </p>
                <p>
                  <strong>Non-trainable Params:</strong>{" "}
                  {results.summary.non_trainable_params}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Results;
