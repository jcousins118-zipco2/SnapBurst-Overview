import { createHash, createPrivateKey, randomUUID, sign } from "node:crypto";

const target = process.env.SITL_RUNNER_URL;
const privateKeyPem = process.env.SITL_RUNNER_PRIVATE_KEY_PEM;
if (!target || !privateKeyPem) {
  throw new Error("Set SITL_RUNNER_URL and SITL_RUNNER_PRIVATE_KEY_PEM in the worker environment.");
}

const jobId = process.env.SITL_RUNNER_JOB_ID || randomUUID();
const runKey = process.env.SITL_RUNNER_RUN_KEY || `synthetic-${jobId}`;
const timestamp = String(Date.now());
const requestBody = { kind: "runSITLValidation", fixtureFingerprint: "sitl-fixture-v1", runKey };
const bodyHash = createHash("sha256").update(JSON.stringify({
  action: "run-sitl-validation",
  fixtureFingerprint: requestBody.fixtureFingerprint,
  runKey: requestBody.runKey,
})).digest("hex");
const canonical = `${jobId}.${timestamp}.${bodyHash}`;
const signature = sign(null, Buffer.from(canonical), createPrivateKey(privateKeyPem)).toString("base64url");

const response = await fetch(`${target.replace(/\/$/, "")}/api/workspace`, {
  method: "POST",
  headers: {
    "content-type": "application/json",
    "x-snapburst-job-id": jobId,
    "x-snapburst-job-timestamp": timestamp,
    "x-snapburst-job-signature": signature,
  },
  body: JSON.stringify(requestBody),
});
const result = await response.json();
console.log(JSON.stringify({ status: response.status, ...result }, null, 2));
if (!response.ok) process.exitCode = 1;
