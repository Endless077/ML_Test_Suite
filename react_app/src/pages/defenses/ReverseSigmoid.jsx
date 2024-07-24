// Reverse Sigmoid Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
import ReverseSigmoidInput from "../../components/input/defenses/reverseSigmoidInput";

import "../../styles/defenses/ReverseSigmoid.css";

let pageTitle = "Reverse Sigmoid";

function ReverseSigmoid() {
  const [vulnerableFileUploaded, setVulnerableFileUploaded] = useState(false);
  const [robustFileUploaded, setRobustFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [vulnerableModelFile, setVulnerableRobustModelFile] = useState(null);
  const [robustModelFile, setRobustModelFile] = useState(null);
  const [personalDataset, setPersonalDataset] = useState(null);

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [beta, setBeta] = useState(1.0);
  const [gamma, setGamma] = useState(0.1);

  const [stealPercentage, setStealPercentage] = useState(0.5);
  const [useProbability, setUseProbability] = useState(false);

  /* ******************************************************************************************* */

  const handleFileUploadVulnerable = (event) => {
    const file = event.target.files[0];
    setVulnerableFileUploaded(!!file);
    setVulnerableRobustModelFile(file);
  };

  const handleFileUploadModelRobust = (event) => {
    const file = event.target.files[0];
    setRobustFileUploaded(!!file);
    setRobustModelFile(file);
  };

  const handlePersonalDatasetUpload = (event) => {
    const directory = event.target.files;
    setPersonalDataset(directory);
    if (directory.length > 0) {
      setDatasetSelected(true);
    } else {
      setDatasetSelected(false);
    }
  };

  const handleCheckboxChange = (event) => {
    if (vulnerableFileUploaded && robustFileUploaded) {
      const isPersonal = event.target.value === "personal";
      setShowPersonalUpload(isPersonal);
      setDatasetSelected(!isPersonal);
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

  const handleBetaChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setBeta(newValue);
  };

  const handleGammaChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setGamma(newValue);
  };

  const handleStealPercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 0.7) {
      setStealPercentage(newValue);
    }
  };

  const handleUseProbabilityChange = (event) => {
    setUseProbability(event.target.checked);
  };

  /* ******************************************************************************************* */

  const validateInputs = () => {
    const errors = [];

    if (!vulnerableFileUploaded || !robustFileUploaded) {
      errors.push("Upload both vulnerable and robust model files.");
    }

    if (!datasetSelected) {
      errors.push("Select a dataset.");
    }

    if (isNaN(parseInt(epochs)) || parseInt(epochs) <= 0 || epochs == "") {
      errors.push("Enter a valid number of epochs (positive value).");
    }

    if (isNaN(parseInt(batchSize)) || parseInt(batchSize) <= 0) {
      errors.push("Enter a valid batch size (positive value).");
    }

    if (isNaN(parseFloat(beta)) || beta <= 0) {
      errors.push("Enter a valid beta value (positive value).");
    }

    if (isNaN(parseFloat(gamma)) || gamma <= 0) {
      errors.push("Enter a valid gamma value (positive value).");
    }

    if (
      isNaN(parseFloat(stealPercentage)) ||
      stealPercentage < 0.1 ||
      stealPercentage > 0.7
    ) {
      errors.push("Enter a valid steal percentage (between 0.1 and 0.7).");
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
              vulnerableFileUploaded={vulnerableFileUploaded}
              robustFileUploaded={robustFileUploaded}
              showPersonalUpload={showPersonalUpload}
              attackName={pageTitle}
              handleFileUploadVulnerable={handleFileUploadVulnerable}
              handleFileUploadModelRobust={handleFileUploadModelRobust}
              handlePersonalDatasetUpload={handlePersonalDatasetUpload}
              handleCheckboxChange={handleCheckboxChange}
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
              beta={beta}
              handleBetaChange={handleBetaChange}
              gamma={gamma}
              stealPercentage={stealPercentage}
              handleStealPercentageChange={handleStealPercentageChange}
              useProbability={useProbability}
              handleUseProbabilityChange={handleUseProbabilityChange}
              handleGammaChange={handleGammaChange}
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
