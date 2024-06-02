import React from "react";
import PropTypes from 'prop-types';

const UploadSection = ({
  handleFileUpload,
  handleCheckboxChange,
  fileUploaded,
  showPersonalUpload,
}) => {
  return (
    <div>
      <div className="upload-section mb-4">
        <label htmlFor="fileUpload" className="form-label">
          <strong>Upload your model</strong>
        </label>
        <input
          type="file"
          className="form-control"
          id="fileUpload"
          accept=".h5,application/octet-stream"
          onChange={handleFileUpload}
        />
      </div>
      <div className="description mb-4" style={{ fontSize: "14px" }}>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent et
        eros eu nisi consectetur feugiat.
      </div>
      <div className="mb-3">
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="isCompiledCheckbox"
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="isCompiledCheckbox">
            Already Compiled
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="defaultCheckbox"
            disabled
            checked
          />
          <label className="form-check-label" htmlFor="defaultCheckbox">
            Default (beta)
          </label>
        </div>
      </div>
      <div className="dataset-selection mt-4">
        <p>
          <strong>Select Dataset</strong>
        </p>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="mnist"
            value="mnist"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="mnist">
            Mnist
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="cifar10"
            value="cifar10"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="cifar10">
            Cifar 10
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="cifar100"
            value="cifar100"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="cifar100">
            Cifar 100
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="personal"
            value="personal"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="personal">
            Personal
          </label>
        </div>
        {showPersonalUpload && (
          <div className="mt-3">
            <label htmlFor="personalFileUpload" className="form-label">
              Select your dataset directory
            </label>
            <input
              type="file"
              className="form-control"
              id="personalFileUpload"
              webkitdirectory="true"
              directory="true"
            />
          </div>
        )}
      </div>
    </div>
  );
};

UploadSection.propTypes = {
    handleFileUpload: PropTypes.func.isRequired,
    handleCheckboxChange: PropTypes.func.isRequired,
    fileUploaded: PropTypes.bool.isRequired,
    showPersonalUpload: PropTypes.bool.isRequired,
  };

export default UploadSection;