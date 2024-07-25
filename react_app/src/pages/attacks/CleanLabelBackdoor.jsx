// CleanLabelBackdoor Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import CleanLabelBackdoorInput from "../../components/input/attacks/cleanLabelBackdoorInput";

import "../../styles/attacks/CleanLabelBackdoor.css";
import Swal from "sweetalert2";

let pageTitle = "Clean Label Backdoor";
import {
  showErrorAlert,
  uploadModel,
  uploadDataset,
  startAttackProcess,
} from "../../utils/functions";

function CleanLabelBackdoor() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [model, setModel] = useState(null);
  const [dataset, setDataset] = useState(null);

  const navigate = useNavigate();

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [targetLabels, setTargetLabels] = useState("");
  const [poisonPercentage, setPoisonPercentage] = useState(0.3);

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
      const attackModel = {
        epochs: epochs,
        batch_size: batchSize,
        filename: model.name.split(".").slice(0, -1).join("."),
        dataset_type: dataset,
        dataset_name: dataset.split(".").slice(0, -1).join(".") || dataset,
        //TODO: missing params
      };

      console.log(attackModel);
      await startAttackProcess(
        "poisoning",
        "cleanlabel",
        attackModel,
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
          Implementation of Clean-Label Backdoor Attack introduced in Turner et
          al., 2018. Applies a number of backdoor perturbation functions and
          does not change labels.
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
            <CleanLabelBackdoorInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              poisonPercentage={poisonPercentage}
              targetLabels={targetLabels}
              handleTargetLabelsChange={handleTargetLabelsChange}
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

export default CleanLabelBackdoor;
