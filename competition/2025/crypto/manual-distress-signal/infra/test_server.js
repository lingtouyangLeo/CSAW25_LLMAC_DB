// Simple test to verify server is working
const express = require("express");
const bodyParser = require("body-parser");
const crypto = require("crypto");
const zlib = require("zlib");

const app = express();
const PORT = 21022;

app.use(bodyParser.json());

const SERVER_SECRET = 'csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}';

// TLS simulation
function simulateTLSRecord(payloadBuffer) {
  const contentType = Buffer.from([0x17]); // Application Data
  const version = Buffer.from([0x03, 0x03]); // TLS 1.2 
  const length = Buffer.alloc(2);
  length.writeUInt16BE(payloadBuffer.length, 0);
  return Buffer.concat([contentType, version, length, payloadBuffer]);
}

app.get("/", (req, res) => {
  res.send("Server is running!");
});

app.post("/send", (req, res) => {
  const userData = req.body.data || "";

  const combined = JSON.stringify({ secret: SERVER_SECRET, userData });

  // Compression
  const compressed = zlib.deflateRawSync(Buffer.from(combined), { strategy: zlib.constants.Z_FIXED });

  // Encryption
  const key = crypto.randomBytes(16);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv("aes-128-cfb", key, iv);
  let ciphertext = cipher.update(compressed);

  // TLS record
  const tlsSimulated = simulateTLSRecord(ciphertext);

  res.json({
    error: "Transmission failure",
    ciphertext: tlsSimulated.toString("base64")
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✓ Server listening on http://0.0.0.0:${PORT}`);
  console.log(`✓ Test at: http://localhost:${PORT}/`);
});
