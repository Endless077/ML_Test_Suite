// Activation Defense Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import ActivationDefenseInput from "../../components/input/defenses/activationDefenseInput";

import "../../styles/defenses/AdversarialTrainer.css";
import Swal from "sweetalert2";

let pageTitle = "Activation Defense";
import {
  showErrorAlert,
  uploadModel,
  uploadDataset,
  startDefenseProcess,
} from "../../utils/functions";

function ActivationDefense() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [model, setModel] = useState(null);
  const [dataset, setDataset] = useState(null);

  const navigate = useNavigate();

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [poisonAttack, setPoisonAttack] = useState("cleanlabel");
  const [poisonPercentage, setPoisonPercentage] = useState(0.3);
  const [clusterAnalysis, setClusterAnalysis] = useState("smaller");
  const [nbClusters, setNbClusters] = useState(2);
  const [reduce, setReduce] = useState("PCA");
  const [nbDims, setNbDims] = useState(10);

  /* ******************************************************************************************* */

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setFileUploaded(!!file);
    setModel(file);
  };

  const handleCheckboxChange = (event) => {
    if (fileUploaded) {
      const isPersonal = event.target.value === "personal";
      setShowPersonalUpload(isPersonal);
      setDatasetSelected(!isPersonal);
      setDataset(event.target.value);
    }
  };

  const handledatasetUpload = (event) => {
    const dataset = event.target.files[0];
    setDataset(dataset);
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

  const handlePoisonAttackChange = (event) => {
    setReduce(event.target.value);
  };

  const handlePoisonPercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 0.7) {
      setPoisonPercentage(newValue);
    }
  };

  const handleClusterAnalysisChange = (event) => {
    setClusterAnalysis(event.target.value);
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
      isNaN(parseFloat(poisonPercentage)) ||
      poisonPercentage < 0.1 ||
      poisonPercentage > 0.7
    ) {
      errors.push("Enter a valid poison percentage (between 0.1 and 0.7).");
    }

    if (isNaN(parseInt(nbClusters)) || parseInt(nbClusters) < 2) {
      errors.push("Enter a valid number of clusters (minimum value: 2).");
    }

    if (!["PCA", "FastICA", "TSNE"].includes(reduce)) {
      errors.push("Select a valid reduce value (PCA, FastICA or TSNE).");
    }

    if (isNaN(parseInt(nbDims)) || parseInt(nbDims) < 1) {
      errors.push("Enter a valid number of dimensions (minimum value: 1).");
    }

    if (!["smaller", "distance"].includes(clusterAnalysis)) {
      errors.push(
        "Select a valid cluster analysis method value (smaller or distance)."
      );
    }

    return errors;
  };

  const uploadFiles = async () => {
    const uploadModelFetch = async () => {
      try {
        const filename = model.name.split(".").slice(0, -1).join(".");
        const uploadResponse = await uploadModel(filename, model);

        if (!uploadResponse.ok) {
          throw new Error(
            uploadResponse.detail ||
              "Error during model upload. Please try again later."
          );
        }

        const response = await uploadResponse.json();
        console.log(response);
        return true;
      } catch (error) {
        console.error("Error during model upload:", error);
        Swal.fire({
          icon: "error",
          title: "Error during model upload",
          text: error.message,
        });
        return false;
      }
    };

    const uploadDatasetFetch = async () => {
      try {
        const filename = dataset.name.split(".").slice(0, -1).join(".");
        const uploadResponse = await uploadDataset(filename, dataset);

        if (!uploadResponse.ok) {
          throw new Error(
            uploadResponse.detail ||
              "Error during dataset upload. Please try again later."
          );
        }

        const response = await uploadResponse.json();
        console.log(response);
        return true;
      } catch (error) {
        console.error("Error during dataset upload:", error);
        Swal.fire({
          icon: "error",
          title: "Error during dataset upload",
          text: error.message,
        });
        return false;
      }
    };

    const uploadModelCheck = await uploadModelFetch();
    return uploadModelCheck && showPersonalUpload
      ? await uploadDatasetFetch()
      : uploadModelCheck;
  };

  const handleLaunchClick = async () => {
    const errors = validateInputs();

    if (errors.length > 0) {
      showErrorAlert(errors);
      return;
    }

    const upload = await uploadFiles();
    if (upload) {
      const defenseModel = {
        epochs: epochs,
        batch_size: batchSize,
        filename: model.name.split(".").slice(0, -1).join("."),
        dataset_type: dataset,
        dataset_name: dataset.split(".").slice(0, -1).join(".") || dataset,
        eps: epsValue,
        eps_step: epsStepValue,
        norm: normValue,
      };

      console.log(attackModel);
      await startDefenseProcess(
        "detector",
        "activationdefense",
        defenseModel,
        navigate
      );
    }
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
              action={pageTitle}
              fileUploaded={fileUploaded}
              showPersonalUpload={showPersonalUpload}
              handleFileUpload={handleFileUpload}
              handleCheckboxChange={handleCheckboxChange}
              handledatasetUpload={handledatasetUpload}
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
              poisonAttack={poisonAttack}
              handlePoisonAttackChange={handlePoisonAttackChange}
              poisonPercentage={poisonPercentage}
              handlePoisonPercentageChange={handlePoisonPercentageChange}
              clusterAnalysis={clusterAnalysis}
              handleClusterAnalysisChange={handleClusterAnalysisChange}
              nbClusters={nbClusters}
              handleNbClustersChange={handleNbClustersChange}
              reduce={reduce}
              handleReduceChange={handleReduceChange}
              nbDims={nbDims}
              handleNbDimsChange={handleNbDimsChange}
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
