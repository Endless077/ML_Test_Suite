// Reverse Sigmoid Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
import ReverseSigmoidInput from "../../components/input/defenses/reverseSigmoidInput";

import "../../styles/defenses/ReverseSigmoid.css";

let pageTitle = "Reverse Sigmoid";

function ReverseSigmoid() {
  const [vulnerableFileUploaded, setVulnerableFileUploaded] = useState(false);
  const [robustFileUploaded, setRobustFileUploaded] = useState(false);
  const [isCompiled, setIsCompiled] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [epochs, setEpochs] = useState("1");
  const [batchSize, setBatchSize] = useState("32");

  /* ******************************************************************************************* */

  const handleFileUploadVulnerable = (event) => {
    setVulnerableFileUploaded(event.target.files.length > 0);
  };

  const handleFileUploadModelRobust = (event) => {
    setRobustFileUploaded(event.target.files.length > 0);
  };

  const handleCheckboxChange = (event) => {
    if (vulnerableFileUploaded && robustFileUploaded) {
      setShowPersonalUpload(event.target.value === "personal");
      setDatasetSelected(true);
    }
  };

  const handleIsCompiledChange = (event) => {
    setIsCompiled(event.target.checked);
  };

  /* ******************************************************************************************* */

  const handleEpochsChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setEpochs(newValue);
    }
  };

  const handleBatchSizeChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setBatchSize(newValue);
    }
  };

  /* ******************************************************************************************* */

  const handleLaunchClick = () => {
    console.log("Launch");
  };

  /* ******************************************************************************************* */
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content container mt-3">
        {/* First Section */}
        <p className="description">
          Implementation of a postprocessor based on adding the Reverse Sigmoid
          perturbation to classifier output.
        </p>
        <a href="https://en.wikipedia.org/wiki/Sigmoid_function">
          What is a Sigmoid function?
        </a>
        {/* Horizontal Divider */}
        <hr />
        {/* Upload Section */}
        <div className="row">
          <div className="col-md-5">
            <UploadSection
              handleFileUploadVulnerable={handleFileUploadVulnerable}
              handleFileUploadModelRobust={handleFileUploadModelRobust}
              handleCheckboxChange={handleCheckboxChange}
              handleIsCompiledChange={handleIsCompiledChange}
              attackName={pageTitle}
              vulnerableFileUploaded={vulnerableFileUploaded}
              robustFileUploaded={robustFileUploaded}
              isCompiled={isCompiled}
              showPersonalUpload={showPersonalUpload}
            />
          </div>
          {/* Vertical Divider */}
          <div className="col-md-2 d-flex align-items-center justify-content-center">
            <div className="vr custom-vr"></div>
          </div>
          {/* Input Section */}
          <div className="col-md-5">
            <ReverseSigmoidInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              datasetSelected={datasetSelected}
            />
            {/* Launch Button */}
            <div className="launch-button-section text-end">
              <button
                className="btn btn-primary"
                disabled={!datasetSelected}
                onClick={handleLaunchClick}
              >
                Launch
              </button>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default ReverseSigmoid;
