// Projected Gradient Descent Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/attacks/uploadSectionAttack";
import PGDInput from "../../components/input/attacks/pgdInput.jsx";

import "../../styles/attacks/ProjectedGradientDescent.css";

let pageTitle = "Projected Gradient Descent";

function ProjectedGradientDescent() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [alreadyCompiled, setAlreadyCompiled] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [epsValue, setEpsValue] = useState(0.3);
  const [epsStepValue, setEpsStepValue] = useState(0.1);
  const [normValue, setNormValue] = useState("inf");

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

  const handleEpsChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setEpsValue(newValue);
    }
  };

  const handleEpsStepChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setEpsStepValue(newValue);
    }
  };

  const handleNormChange = (event) => {
    const newValue = event.target.value;
    if (["inf", "1", "2"].includes(newValue)) {
      setNormValue(newValue);
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
          The Projected Gradient Descent attack is an iterative method in which,
          after each iteration, the perturbation is projected on an lp-ball of
          specified radius (in addition to clipping the values of the
          adversarial sample so that it lies in the permitted data range). This
          is the attack proposed by Madry et al. for adversarial training.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1706.06083">
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
            <PGDInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              epsValue={epsValue}
              handleEpsChange={handleEpsChange}
              epsStepValue={epsStepValue}
              handleEpsStepChange={handleEpsStepChange}
              normValue={normValue}
              handleNormChange={handleNormChange}
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

export default ProjectedGradientDescent;
