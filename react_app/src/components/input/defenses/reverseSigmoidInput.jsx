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
  stealPercentage,
  handleStealPercentageChange,
  useProbability,
  handleUseProbabilityChange,
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
          <strong>Beta - A positive magnitude parameter</strong>
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
          <strong>
            Gamma - A positive dataset and model specific convergence parameter
          </strong>
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

      <hr />
      <div>
        <label
          className="form-label"
          style={{
            display: "block",
            textAlign: "left",
            fontSize: "1.2rem",
            marginTop: "1rem",
          }}
        >
          <strong>Other Options (extraction attack)</strong>
        </label>
        <div className="additional-input-section">
          <div className="mb-3">
            <label
              className="form-label"
              style={{ display: "block", textAlign: "left" }}
            >
              <strong>Steal Percentage - Percentage of stolen dataset</strong>
            </label>
            <input
              id="steal_percentage"
              type="number"
              step="0.01"
              min="0.1"
              max="0.7"
              className="form-control"
              placeholder="steal_percentage"
              value={stealPercentage}
              onChange={handleStealPercentageChange}
              disabled={!datasetSelected}
            />
          </div>
          <div className="mb-3 form-check">
            <input
              id="use_probability"
              type="checkbox"
              className="form-check-input"
              checked={useProbability}
              onChange={handleUseProbabilityChange}
              disabled={!datasetSelected}
            />
            <label className="form-check-label" htmlFor="use_probability">
              Use Probability
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

ReverseSigmoidInput.propTypes = {
  epochs: PropTypes.number.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.number.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
  beta: PropTypes.number.isRequired,
  handleBetaChange: PropTypes.func.isRequired,
  gamma: PropTypes.number.isRequired,
  handleGammaChange: PropTypes.func.isRequired,
};

export default ReverseSigmoidInput;
