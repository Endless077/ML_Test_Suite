// Adversarial Trainer Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
import AdversarialTrainerInput from "../../components/input/defenses/adversarialTrainerInput";

import "../../styles/defenses/AdversarialTrainer.css";

let pageTitle = "Adversarial Trainer";

function AdversarialTrainer() {
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
            <AdversarialTrainerInput
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

export default AdversarialTrainer;
