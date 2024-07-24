// Simple Backdoor Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/attacks/uploadSectionAttack";
import SimpleBackdoorInput from "../../components/input/attacks/simpleBackdoorInput";

import "../../styles/attacks/SimpleBackdoor.css";

let pageTitle = "Simple Backdoor";
import { startAttackProcess, showErrorAlert } from "../../utils/functions";

function SimpleBackdoor() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [modelFile, setModelFile] = useState(null);
  const [personalDataset, setPersonalDataset] = useState(null);

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [targetLabels, setTargetLabels] = useState("");
  const [poisonPercentage, setPoisonPercentage] = useState(0.3);

  /* ******************************************************************************************* */

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setFileUploaded(!!file);
    setModelFile(file);
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
    if (fileUploaded) {
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

  const handleTargetLabelsChange = (event) => {
    const newValue = event.target.value;
    const regex = /^[0-9,]*$/;
    if (regex.test(newValue)) {
      setTargetLabels(newValue.replace(/\s*,\s*/g, ","));
    }
  };

  const handlePoisonPercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 0.7) {
      setPoisonPercentage(newValue);
    }
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

    if (!targetLabels || !/^\d+(,\d+)*$/.test(targetLabels)) {
      errors.push("Enter target labels as numbers separated by commas.");
    }

    if (
      isNaN(parseFloat(poisonPercentage)) ||
      poisonPercentage < 0.1 ||
      poisonPercentage > 0.7
    ) {
      errors.push("Enter a valid poison percentage (between 0.1 and 0.7).");
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
          Implementation of backdoor attacks introduced in Gu et al., 2017.
          Applies a number of backdoor perturbation functions and switches label
          to target label.
        </p>
        <a
          className="details-link"
          href="https://people.csail.mit.edu/madry/lab/cleanlabel.pdf"
        >
          See Details Here
        </a>
        {/* Horizontal Divider */}
        <hr />
        {/* Upload Section */}
        <div className="row">
          <div className="col-md-5">
            <UploadSection
              fileUploaded={fileUploaded}
              showPersonalUpload={showPersonalUpload}
              attackName={pageTitle}
              handleFileUpload={handleFileUpload}
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
            <SimpleBackdoorInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              targetLabels={targetLabels}
              handleTargetLabelsChange={handleTargetLabelsChange}
              poisonPercentage={poisonPercentage}
              handlePoisonPercentageChange={handlePoisonPercentageChange}
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

export default SimpleBackdoor;
