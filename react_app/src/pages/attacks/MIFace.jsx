// MIFace Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import MIFaceInput from "../../components/input/attacks/miFaceInput";

import "../../styles/attacks/MIFace.css";

let pageTitle = "MIFace";
import { startAttackProcess, showErrorAlert } from "../../utils/functions";

function MIFace() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [modelFile, setModelFile] = useState(null);
  const [personalDataset, setPersonalDataset] = useState(null);

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [maxIter, setMaxIter] = useState(10000);
  const [windowLength, setWindowLength] = useState(100);
  const [threshold, setThreshold] = useState(0.99);
  const [learningRate, setLearningRate] = useState(0.1);

  /* ******************************************************************************************* */

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setFileUploaded(!!file);
    setModelFile(file);
  };

  const handleCheckboxChange = (event) => {
    if (fileUploaded) {
      const isPersonal = event.target.value === "personal";
      setShowPersonalUpload(isPersonal);
      setDatasetSelected(!isPersonal);
    }
  };

  const handlePersonalDatasetUpload = (event) => {
    const dataset = event.target.files[0];
    setPersonalDataset(dataset);
    setDatasetSelected(true);
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
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setThreshold(newValue);
    }
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

  const validateInputs = () => {
    const errors = [];

    if (!fileUploaded) {
      errors.push("Upload a model file.");
    }

    if (!datasetSelected) {
      errors.push("Select a dataset.");
    }

    if (isNaN(parseInt(epochs)) || parseInt(epochs) <= 0 || epochs === "") {
      errors.push("Enter a valid number of epochs (positive value).");
    }

    if (isNaN(parseInt(batchSize)) || parseInt(batchSize) <= 0) {
      errors.push("Enter a valid batch size (positive value).");
    }

    if (isNaN(parseInt(maxIter)) || parseInt(maxIter) < 1 || maxIter === "") {
      errors.push(
        "Enter a valid maximum number of iterations (positive integer)."
      );
    }

    if (
      isNaN(parseInt(windowLength)) ||
      parseInt(windowLength) < 1 ||
      windowLength === ""
    ) {
      errors.push("Enter a valid window length (positive integer).");
    }

    if (isNaN(parseFloat(threshold)) || threshold < 0.1 || threshold > 1) {
      errors.push("Enter a valid threshold value (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(learningRate)) || parseFloat(learningRate) <= 0) {
      errors.push("Enter a valid learning rate (positive value).");
    }

    return errors;
  };

  const handleLaunchClick = () => {
    const errors = validateInputs();

    if (errors.length > 0) {
      showErrorAlert(errors);
      return;
    }

    // TODO: start the process
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
              action={pageTitle}
              fileUploaded={fileUploaded}
              showPersonalUpload={showPersonalUpload}
              handleFileUpload={handleFileUpload}
              handleCheckboxChange={handleCheckboxChange}
              handlePersonalDatasetUpload={handlePersonalDatasetUpload}
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
