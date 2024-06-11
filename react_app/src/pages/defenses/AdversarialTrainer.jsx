// Adversarial Trainer Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
import AdversarialTrainerInput from "../../components/input/defenses/adversarialTrainerInput";

import "../../styles/defenses/AdversarialTrainer.css";

let pageTitle = "Adversarial Trainer";

function AdversarialTrainer() {
  const [vulnerableFileUploaded, setVulnerableFileUploaded] = useState(false);
  const [robustFileUploaded, setRobustFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [vulnerableModelFile, setVulnerableRobustModelFile] = useState(null);
  const [robustModelFile, setRobustModelFile] = useState(null);
  const [personalDataset, setPersonalDataset] = useState(null);
  const [alreadyCompiled, setAlreadyCompiled] = useState(false);

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [evasionAttack, setEvasionAttack] = useState("FGM");
  const [samplePercentage, setSamplePercentage] = useState(0.1);
  const [ratio, setRatio] = useState(0.5);

  const [epsValue, setEpsValue] = useState(0.3);
  const [epsStepValue, setEpsStepValue] = useState(0.1);
  const [normValue, setNormValue] = useState("inf");

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

  const handleAlreadyCompiledChange = (event) => {
    setAlreadyCompiled(event.target.checked);
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

  const handleEvasionAttackChange = (event) => {
    setEvasionAttack(event.target.value);
  };

  const handleSamplePercentageChange = (event) => {
    const newValue = event.target.value;
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setSamplePercentage(newValue);
    }
  };

  const handleRatioChange = (event) => {
    const newValue = event.target.value;
    if (
      !isNaN(newValue) &&
      parseFloat(newValue) >= 0.1 &&
      parseFloat(newValue) <= 1
    ) {
      setRatio(newValue);
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

    if (!vulnerableFileUploaded || !robustFileUploaded) {
      errors.push("Upload both vulnerable and robust model files.");
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

    if (!["FGM", "PGD"].includes(evasionAttack)) {
      errors.push("Select a valid evasion attack acronym.");
    }

    if (
      isNaN(parseFloat(samplePercentage)) ||
      samplePercentage < 0.1 ||
      samplePercentage > 1
    ) {
      errors.push("Enter a valid sample percentage (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(ratio)) || ratio < 0.1 || ratio > 1) {
      errors.push("Enter a valid ratio (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(epsValue)) || epsValue < 0.1 || epsValue > 1) {
      errors.push("Enter a valid eps value (between 0.1 and 1).");
    }

    if (
      isNaN(parseFloat(epsStepValue)) ||
      epsStepValue < 0.1 ||
      epsStepValue > 1
    ) {
      errors.push("Enter a valid eps step value (between 0.1 and 1).");
    }

    if (!["inf", "1", "2"].includes(normValue)) {
      errors.push("Select a valid norm value (inf, 1 or 2).");
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
          Class performing adversarial training based on a model architecture
          and one or multiple attack methods. Incorporates original adversarial
          training, ensemble adversarial training (
          <a href="https://arxiv.org/abs/1705.07204">article</a>), training on
          all adversarial data and other common setups. If multiple attacks are
          specified, they are rotated for each batch. If the specified attacks
          have as target a different model, then the attack is transferred. The
          ratio determines how many of the clean samples in each batch are
          replaced with their adversarial counterpart. Please keep in mind the
          limitations of defences. While adversarial training is widely regarded
          as a promising, principled approach to making classifiers more robust
          (see <a href="https://arxiv.org/abs/1802.00420">article</a>), very
          careful evaluations are required to assess its effectiveness case by
          case (see <a href="https://arxiv.org/abs/1902.06705">here</a>).
        </p>
        <a href="https://arxiv.org/abs/1705.07204">See Details Here</a>
        {/* Horizontal Divider */}
        <hr />
        {/* Upload Section */}
        <div className="row">
          <div className="col-md-5">
            <UploadSection
              vulnerableFileUploaded={vulnerableFileUploaded}
              robustFileUploaded={robustFileUploaded}
              alreadyCompiled={alreadyCompiled}
              showPersonalUpload={showPersonalUpload}
              attackName={pageTitle}
              handleFileUploadVulnerable={handleFileUploadVulnerable}
              handleFileUploadModelRobust={handleFileUploadModelRobust}
              handlePersonalDatasetUpload={handlePersonalDatasetUpload}
              handleAlreadyCompiledChange={handleAlreadyCompiledChange}
              handleCheckboxChange={handleCheckboxChange}
            />
          </div>
          {/* Vertical Divider */}
          <div className="col-md-2 d-flex align-items-center justify-content-center">
            <div className="vr custom-vr"></div>
          </div>
          {/* Input Section */}
          <div className="col-md-5">
            <AdversarialTrainerInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              evasionAttack={evasionAttack}
              handleEvasionAttackChange={handleEvasionAttackChange}
              samplePercentage={samplePercentage}
              handleSamplePercentageChange={handleSamplePercentageChange}
              ratio={ratio}
              handleRatioChange={handleRatioChange}
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

export default AdversarialTrainer;
