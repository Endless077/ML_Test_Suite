// Reverse Sigmoid Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import ReverseSigmoidInput from "../../components/input/defenses/reverseSigmoidInput";

import "../../styles/defenses/ReverseSigmoid.css";
import Swal from "sweetalert2";

let pageTitle = "Reverse Sigmoid";
import {
  showErrorAlert,
  uploadModel,
  uploadDataset,
  startDefenseProcess,
} from "../../utils/functions";

function ReverseSigmoid() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [model, setModel] = useState(null);
  const [dataset, setDataset] = useState(null);

  const navigate = useNavigate();

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [beta, setBeta] = useState(1.0);
  const [gamma, setGamma] = useState(0.1);

  const [stealPercentage, setStealPercentage] = useState(0.5);
  const [useProbability, setUseProbability] = useState(false);

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

    if (!fileUploaded) {
      errors.push("Upload a model file.");
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
        beta: beta,
        gamma: gamma,
        steal_percentage: stealPercentage,
        use_probability: useProbability,
      };

      console.log(attackModel);
      await startDefenseProcess(
        "postprocessor",
        "reversesigmoid",
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
