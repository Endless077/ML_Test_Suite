// Activation Defense Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
import ActivationDefenseInput from "../../components/input/defenses/activationDefenseInput";

import "../../styles/defenses/AdversarialTrainer.css";

let pageTitle = "Activation Defense";

function ActivationDefense() {
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
  const [poisonPercentage, setPoisonPercentage] = useState(0.3);
  const [nbClusters, setNbClusters] = useState(2);
  const [reduce, setReduce] = useState("PCA");
  const [nbDims, setNbDims] = useState(10);
  const [clusterAnalysis, setClusterAnalysis] = useState("smaller");

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

  const handlePoisonPercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 0.7) {
      setPoisonPercentage(newValue);
    }
  };

  const handleNbClustersChange = (event) => {
    const newValue = event.target.value;
    if (
      newValue === "" ||
      (/^\d+$/.test(newValue) && parseInt(newValue) >= 2)
    ) {
      setNbClusters(newValue);
    }
  };

  const handleReduceChange = (event) => {
    setReduce(event.target.value);
  };

  const handleNbDimsChange = (event) => {
    const newValue = event.target.value;
    if (
      newValue === "" ||
      (/^\d+$/.test(newValue) && parseInt(newValue) >= 1)
    ) {
      setNbDims(newValue);
    }
  };

  const handleClusterAnalysisChange = (event) => {
    setClusterAnalysis(event.target.value);
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
          Method from Chen et al., 2018 performing poisoning detection based on
          activations clustering. Please keep in mind the limitations of
          defences. For more information on the limitations of this defence, see{" "}
          <a href="https://arxiv.org/abs/1905.13409">this article</a> . For
          details on how to evaluate classifier security in general, see{" "}
          <a href="https://arxiv.org/abs/1902.06705">this article</a>.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1811.03728">
          See Details Here
        </a>
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
            <ActivationDefenseInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              poisonPercentage={poisonPercentage}
              handlePoisonPercentageChange={handlePoisonPercentageChange}
              nbClusters={nbClusters}
              handleNbClustersChange={handleNbClustersChange}
              reduce={reduce}
              handleReduceChange={handleReduceChange}
              nbDims={nbDims}
              handleNbDimsChange={handleNbDimsChange}
              clusterAnalysis={clusterAnalysis}
              handleClusterAnalysisChange={handleClusterAnalysisChange}
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

export default ActivationDefense;
