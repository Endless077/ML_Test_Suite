// TotalVarMin Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import TotalVarMinInput from "../../components/input/defenses/totalVarMinInput";

import "../../styles/defenses/TotalVarMin.css";

let pageTitle = "Total Variance Minimization";

function TotalVarMin() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [modelFile, setModelFile] = useState(null);
  const [personalDataset, setPersonalDataset] = useState(null);

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [evasionAttack, setEvasionAttack] = useState("FGM");
  const [samplePercentage, setSamplePercentage] = useState(0.1);
  const [prob, setProb] = useState(0.3);
  const [normInt, setNormInt] = useState(2);
  const [lamb, setLamb] = useState(0.5);
  const [solverValue, setSolverValue] = useState("L-BFGS-B");
  const [maxIterValue, setMaxIterValue] = useState("10");

  const [epsValue, setEpsValue] = useState(0.3);
  const [epsStepValue, setEpsStepValue] = useState(0.1);
  const [normValue, setNormValue] = useState("inf");

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

  const handleEvasionAttackChange = (event) => {
    setEvasionAttack(event.target.value);
  };

  const handleSamplePercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setSamplePercentage(newValue);
    }
  };

  const handleProbChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setProb(newValue);
    }
  };

  const handleNormIntChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setNormInt(newValue);
  };

  const handleLambChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setLamb(newValue);
  };

  const handleSolverChange = (event) => {
    const newValue = event.target.value;
    setSolverValue(newValue);
  };

  const handleMaxIterChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setMaxIterValue(newValue);
    }
  };

  /* ******************************************************************************************* */

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

    if (
      isNaN(parseFloat(samplePercentage)) ||
      samplePercentage < 0.1 ||
      samplePercentage > 1
    ) {
      errors.push("Enter a valid sample percentage (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(prob)) || prob < 0.1 || prob > 1) {
      errors.push("Enter a valid probability (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(normInt)) || parseFloat(normInt) <= 0) {
      errors.push("Enter a valid norm interval (positive value).");
    }

    if (isNaN(parseFloat(lamb)) || parseFloat(lamb) <= 0) {
      errors.push("Enter a valid lambda value (positive value).");
    }

    if (isNaN(parseInt(maxIterValue)) || parseInt(maxIterValue) <= 0) {
      errors.push("Enter a valid max iterations value (positive value).");
    }

    if (isNaN(parseFloat(epsValue)) || epsValue < 0.1 || epsValue > 1) {
      errors.push("Enter a valid epsilon value (between 0.1 and 1).");
    }

    if (
      isNaN(parseFloat(epsStepValue)) ||
      epsStepValue < 0.1 ||
      epsStepValue > 1
    ) {
      errors.push("Enter a valid epsilon step value (between 0.1 and 1).");
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
          Implement the total variance minimization defence approach. Please
          keep in mind the limitations of defences. For more information on the
          limitations of this defence, see{" "}
          <a href="https://arxiv.org/abs/1802.00420">this article</a>. For
          details on how to evaluate classifier security in general, see{" "}
          <a href="https://arxiv.org/abs/1902.06705">this article</a>.
        </p>
        <a href="https://openreview.net/forum?id=SyJ7ClWCb">See Details Here</a>
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
            <TotalVarMinInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              evasionAttack={evasionAttack}
              handleEvasionAttackChange={handleEvasionAttackChange}
              samplePercentage={samplePercentage}
              handleSamplePercentageChange={handleSamplePercentageChange}
              prob={prob}
              handleProbChange={handleProbChange}
              normInt={normInt}
              handleNormIntChange={handleNormIntChange}
              lamb={lamb}
              handleLambChange={handleLambChange}
              solver={solverValue}
              handleSolverChange={handleSolverChange}
              maxIter={maxIterValue}
              handleMaxIterChange={handleMaxIterChange}
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

export default TotalVarMin;
