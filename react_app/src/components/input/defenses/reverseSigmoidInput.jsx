import React from "react";
import PropTypes from "prop-types";

const ReverseSigmoidInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  beta,
  handleBetaChange,
  gamma,
  handleGammaChange,
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
          <strong>Beta - The value of beta</strong>
        </label>
        <input
          id="beta"
          type="text"
          className="form-control"
          placeholder="beta"
          value={beta}
          onChange={handleBetaChange}
          disabled={!datasetSelected}
          pattern="[0-9]*\.?[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Gamma - The value of gamma</strong>
        </label>
        <input
          id="gamma"
          type="text"
          className="form-control"
          placeholder="gamma"
          value={gamma}
          onChange={handleGammaChange}
          disabled={!datasetSelected}
          pattern="[0-9]*\.?[0-9]*"
        />
      </div>
    </div>
  );
};

ReverseSigmoidInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
  beta: PropTypes.string.isRequired,
  handleBetaChange: PropTypes.func.isRequired,
  gamma: PropTypes.string.isRequired,
  handleGammaChange: PropTypes.func.isRequired,
};

export default ReverseSigmoidInput;
