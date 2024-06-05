// STRong Intentional Perturbation Page
import React, { useState } from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/input/defenses/uploadSectionDefense";
//import STRIPInput from "../../components/input/defenses/stripInput";

import "../../styles/defenses/STRongIntentionalPerturbation.css";

let pageTitle = "STRong Intentional Perturbation";

function STRongIntentionalPerturbation() {
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
      <div className="page-content">
        {/* First Section */}
        <p className="description">
          Implementation of STRIP: A Defence Against Trojan Attacks on Deep
          Neural Networks (Gao et. al. 2020)
        </p>
        <a href="https://arxiv.org/abs/1902.06531">See Details Here</a>
        <a href="https://openreview.net/forum?id=SyJ7ClWCb">See Details Here</a>
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
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default STRongIntentionalPerturbation;
