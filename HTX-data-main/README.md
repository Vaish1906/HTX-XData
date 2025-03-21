# HTX Assessment

## Interacting with the live application

The application is deployed in AWS and available at: [https://url.com](https://url.com)

Underlying architecture of the application follows the proposed [deployment design](./deployment-design/design.pdf), within the constraints imposed by the AWS Free Tier.

## Running the code locally

Install Make/CMake and Docker for your operating system. Then run `make deploy` to spin up the API server and Elastic Search frontend and backend containers all at once.

If you don't already have a virtual environment setup,  run `python -m venv venv` in the root of this directory, and then activate it with `source ./venv/bin/activate`.

To install dependencies run `make install`. If any new dependencies are added, please run `make freeze` to update requirements.txt.

To download and transcribe the Common Voice dataset into the required CSV format run `make transcribe` **while the ASR API is running**.

To update the Elastic search index with the contents of the CSV run `make index` **while the Elastic Search frontend and backend are running**.
