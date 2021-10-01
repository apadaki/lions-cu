const { BlobServiceClient } = require('@azure/storage-blob');
const express = require('express');
const path = require('path');
const fs = require('fs')

const app = express();
const port = process.env.PORT || 8080;

async function main() {
  require('dotenv').config()
  AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING

  // Create the BlobServiceClient object which will be used to create a container client
  const blobServiceClient = BlobServiceClient.fromConnectionString(AZURE_STORAGE_CONNECTION_STRING);

  // Create a unique name for the container
  const containerName = 'lion-data-container-v4'

  const containerClient = blobServiceClient.getContainerClient(containerName);

  // Get a reference to a container
  const blockBlobClient_johnjay = containerClient.getBlockBlobClient('johnjay_graph.html');
  const blockBlobClient_jj = containerClient.getBlockBlobClient('jj_graph.html');
  const blockBlobClient_ferris = containerClient.getBlockBlobClient('ferris_graph.html');
  

  const downloadBlockBlobResponse_johnjay = await blockBlobClient_johnjay.download(0);
  const downloadBlockBlobResponse_jj = await blockBlobClient_jj.download(0);
  const downloadBlockBlobResponse_ferris = await blockBlobClient_ferris.download(0);

  // console.log('\nDownloaded blob content...');
  const data_johnjay = await streamToString(downloadBlockBlobResponse_johnjay.readableStreamBody);
  const data_jj = await streamToString(downloadBlockBlobResponse_jj.readableStreamBody);
  const data_ferris = await streamToString(downloadBlockBlobResponse_ferris.readableStreamBody);

  var minutes = 5, the_interval = minutes * 60 * 1000;
  setInterval(function() {
    console.log("MINUTE PASSED");
    data_johnjay = await streamToString(downloadBlockBlobResponse_johnjay.readableStreamBody);
    data_jj = await streamToString(downloadBlockBlobResponse_jj.readableStreamBody);
    data_ferris = await streamToString(downloadBlockBlobResponse_ferris.readableStreamBody);
  }, 60*1000);


  

  app.get('/app/johnjay_graph.html', function(req, res) {
    res.send(data_johnjay)
  })
  app.get('/app/jj_graph.html', function(req, res) {
    res.send(data_jj)
  })
  app.get('/app/ferris_graph.html', function(req, res) {
    res.send(data_ferris)
  })
  app.get('/app/components/favicon.ico', function(req, res) {
    res.sendFile(path.join(__dirname, '/components/favicon.ico'));
  })
  app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/components/index.html'));
  });

  app.listen(port);
}

main().then(() => console.log('Done')).catch((ex) => console.log(ex.message));

// A helper function used to read a Node.js readable stream into a string
async function streamToString(readableStream) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    readableStream.on("data", (data) => {
      chunks.push(data.toString());
    });
    readableStream.on("end", () => {
      resolve(chunks.join(""));
    });
    readableStream.on("error", reject);
  });
}
