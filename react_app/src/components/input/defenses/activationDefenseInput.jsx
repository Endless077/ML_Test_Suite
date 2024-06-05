import React from "react";
import PropTypes from "prop-types";

const ActivationDefenseInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  poisonPercentage,
  handlePoisonPercentageChange,
  nbClusters,
  handleNbClustersChange,
  reduce,
  handleReduceChange,
  nbDims,
  handleNbDimsChange,
  clusterAnalysis,
  handleClusterAnalysisChange,
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
          <strong>Poison Percentage - Percentage of poisoned dataset</strong>
        </label>
        <input
          id="poison_percentage"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="poison_percentage"
          value={poisonPercentage}
          onChange={handlePoisonPercentageChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Number of Clusters - Number of clusters for activation clustering
          </strong>
        </label>
        <input
          id="nb_clusters"
          type="text"
          className="form-control"
          placeholder="nb_clusters"
          value={nbClusters}
          onChange={handleNbClustersChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>

      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Dimensionality Reduction Technique - Choose a reduction technique
          </strong>
        </label>
        <select
          id="reduce"
          className="form-select"
          value={reduce}
          onChange={handleReduceChange}
          disabled={!datasetSelected}
        >
          <option value="PCA">PCA</option>
          <option value="FastICA">FastICA</option>
          <option value="TSNE">TSNE</option>
        </select>
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Number of Dimensions - Number of dimensions for reduction
          </strong>
        </label>
        <input
          id="nb_dims"
          type="text"
          className="form-control"
          placeholder="nb_dims"
          value={nbDims}
          onChange={handleNbDimsChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Cluster Analysis - Choose a cluster analysis technique
          </strong>
        </label>
        <select
          id="cluster_analysis"
          className="form-select"
          value={clusterAnalysis}
          onChange={handleClusterAnalysisChange}
          disabled={!datasetSelected}
        >
          <option value="smaller">Smaller</option>
          <option value="distance">Distance</option>
        </select>
      </div>
    </div>
  );
};

ActivationDefenseInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default ActivationDefenseInput;
