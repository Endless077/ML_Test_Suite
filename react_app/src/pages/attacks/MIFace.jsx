// MIFace Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/attacks/uploadSectionAttack";
import MIFaceInput from "../../components/input/attacks/miFaceInput";

import "../../styles/attacks/MIFace.css";

let pageTitle = "MIFace";

function MIFace() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [alreadyCompiled, setAlreadyCompiled] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [maxIter, setMaxIter] = useState(10000);
  const [windowLength, setWindowLength] = useState(100);
  const [threshold, setThreshold] = useState(0.99);
  const [learningRate, setLearningRate] = useState(0.1);

  /* ******************************************************************************************* */

  const handleFileUpload = (event) => {
    setFileUploaded(event.target.files.length > 0);
  };

  const handleAlreadyCompiledChange = (event) => {
    setAlreadyCompiled(event.target.checked);
  };

  const handleCheckboxChange = (event) => {
    if (fileUploaded) {
      setShowPersonalUpload(event.target.value === "personal");
      setDatasetSelected(true);
    }
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

  const handleMaxIterChange = (event) => {
    const newValue = event.target.value;
    if (
      newValue === "" ||
      (/^\d+$/.test(newValue) && parseInt(newValue) >= 1)
    ) {
      setMaxIter(newValue);
    }
  };

  const handleWindowLengthChange = (event) => {
    const newValue = event.target.value;
    if (
      newValue === "" ||
      (/^\d+$/.test(newValue) && parseInt(newValue) >= 1)
    ) {
      setWindowLength(newValue);
    }
  };

  const handleThresholdChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, Math.min(1, parseFloat(newValue)));
    }
    setThreshold(newValue);
  };

  const handleLearningRateChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setLearningRate(newValue);
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
          Implementation of the MIFace algorithm from Fredrikson et al. (2015).
          While in that paper the attack is demonstrated specifically against
          face recognition models, it is applicable more broadly to classifiers
          with continuous features which expose class gradients.
        </p>
        <a
          className="details-link"
          href="https://dl.acm.org/doi/10.1145/2810103.2813677"
        >
          See Details Here
        </a>
        {/* Horizontal Divider */}
        <hr />
        {/* Upload Section */}
        <div className="row">
          <div className="col-md-5">
            <UploadSection
              handleFileUpload={handleFileUpload}
              handleAlreadyCompiled={handleAlreadyCompiledChange}
              handleCheckboxChange={handleCheckboxChange}
              attackName={pageTitle}
              fileUploaded={fileUploaded}
              alreadyCompiled={alreadyCompiled}
              showPersonalUpload={showPersonalUpload}
            />
          </div>
          {/* Vertical Divider */}
          <div className="col-md-2 d-flex align-items-center justify-content-center">
            <div className="vr custom-vr"></div>
          </div>
          {/* Input Section */}
          <div className="col-md-5">
            <MIFaceInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              maxIter={maxIter}
              handleMaxIterChange={handleMaxIterChange}
              windowLength={windowLength}
              handleWindowLengthChange={handleWindowLengthChange}
              threshold={threshold}
              handleThresholdChange={handleThresholdChange}
              learningRate={learningRate}
              handleLearningRateChange={handleLearningRateChange}
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

export default MIFace;
