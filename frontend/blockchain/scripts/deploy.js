// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  // Option A: use deployContract (simpler in Ethers v6)
  const provenanceRegistry = await hre.ethers.deployContract("ProvenanceRegistry");

  // Wait for the deployment to be mined
  await provenanceRegistry.waitForDeployment();

  // Get the deployed address
  const address = await provenanceRegistry.getAddress(); // or provenanceRegistry.target

  console.log("ProvenanceRegistry deployed to:", address);
}

// Hardhat’s recommended pattern
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
