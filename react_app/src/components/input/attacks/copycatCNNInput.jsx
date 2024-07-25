import React from "react";
import PropTypes from "prop-types";

const CopycatCNNInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
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
  );
};

CopycatCNNInput.propTypes = {
  epochs: PropTypes.number.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.number.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  stealPercentage: PropTypes.number.isRequired,
  handleStealPercentageChange: PropTypes.func.isRequired,
  useProbability: PropTypes.bool.isRequired,
  handleUseProbabilityChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default CopycatCNNInput;
