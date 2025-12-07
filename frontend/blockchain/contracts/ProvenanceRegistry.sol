// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ProvenanceRegistry {
    struct Dataset {
        string datasetId;
        bytes32 hash;
        string metadata;
        uint256 timestamp;
        address uploader;
    }

    struct Model {
        string version;
        bytes32 hash;
        string datasetId;
        uint256 timestamp;
        address uploader;
    }

    struct LogAnchor {
        string sessionId;
        bytes32 hash;
        string modelVersion;
        uint256 timestamp;
        address committer;
    }

    mapping(string => Dataset) public datasets;
    mapping(string => Model) public models;
    mapping(string => LogAnchor) public logAnchors;

    event DatasetRegistered(string datasetId, bytes32 hash, string metadata, address uploader);
    event ModelRegistered(string version, bytes32 hash, string datasetId, address uploader);
    event LogCommitted(string sessionId, bytes32 hash, string modelVersion, address committer);

    function registerDataset(
        string memory datasetId,
        bytes32 hash,
        string memory metadata
    ) public {
        datasets[datasetId] = Dataset(datasetId, hash, metadata, block.timestamp, msg.sender);
        emit DatasetRegistered(datasetId, hash, metadata, msg.sender);
    }

    function registerModel(
        string memory version,
        bytes32 hash,
        string memory datasetId
    ) public {
        models[version] = Model(version, hash, datasetId, block.timestamp, msg.sender);
        emit ModelRegistered(version, hash, datasetId, msg.sender);
    }

    function commitLog(
        string memory sessionId,
        bytes32 hash,
        string memory modelVersion
    ) public {
        logAnchors[sessionId] = LogAnchor(sessionId, hash, modelVersion, block.timestamp, msg.sender);
        emit LogCommitted(sessionId, hash, modelVersion, msg.sender);
    }
}
