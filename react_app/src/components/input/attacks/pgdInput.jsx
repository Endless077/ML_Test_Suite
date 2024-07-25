import React from "react";
import PropTypes from "prop-types";

const PGDInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  epsValue,
  handleEpsChange,
  epsStepValue,
  handleEpsStepChange,
  normValue,
  handleNormChange,
  datasetSelected,
}) => {
  return (
    <div className="text-boxes-section mb-3">
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Epochs - The number of epochs</strong>
        </label>
        <input
          id="epochs"
          type="text"
          className="form-control"
          placeholder="epochs"
          value={epochs}
          onChange={handleEpochsChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Batch Size - The batch size for the attack</strong>
        </label>
        <input
          id="batch_size"
          type="text"
          className="form-control"
          placeholder="batch_size"
          value={batchSize}
          onChange={handleBatchSizeChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Eps - Attack step size</strong>
        </label>
        <input
          id="eps"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="eps"
          value={epsValue}
          onChange={handleEpsChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Eps Step - Step size of input variation</strong>
        </label>
        <input
          id="eps_step"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="eps_step"
          value={epsStepValue}
          onChange={handleEpsStepChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Norm - The norm used for measuring the size of the perturbation
          </strong>
        </label>
        <select
          id="norm"
          className="form-select"
          value={normValue}
          onChange={handleNormChange}
          disabled={!datasetSelected}
        >
          <option value="inf">inf</option>
          <option value="1">1</option>
          <option value="2">2</option>
        </select>
      </div>
    </div>
  );
};

PGDInput.propTypes = {
  epochs: PropTypes.number.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.number.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  epsValue: PropTypes.number.isRequired,
  handleEpsChange: PropTypes.func.isRequired,
  epsStepValue: PropTypes.number.isRequired,
  handleEpsStepChange: PropTypes.func.isRequired,
  normValue: PropTypes.oneOf(["inf", "1", "2"]).isRequired,
  handleNormChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default PGDInput;
