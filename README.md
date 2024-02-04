# Data Migration APP

## Description

Data migration app is a web application that allows you to feed a SQL database (SQLite) with flat files that you can upload from the user interface built with Streamlit. There is also a large text area for batch record loading.

Additionally, it has two buttons, SQL1 and SQL2, which execute custom queries requested by the client..

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Installation
To install Data Migration App, follow these steps:

1. Clone this repository to your local machine.
2. If you want to run it locally just open a terminal install dependencies in requirements.txt and run this command 
```bash
streamlit run main.py 
```
 
3. Give access to the service account so that it can push Docker images to GCR and deploy applications to Cloud Run. Take its JSON file, place it in the specified path, and change the PATH on line 17 (credentials) in main.tf. Also, ensure that you have proper authentication from the environment to GCR.
https://cloud.google.com/container-registry/docs/advanced-authentication?hl=es-419
4. In script.sh Set up environment variables as needed. 
5. Start the GCP cloud deployment  by running script.sh


## Usage
Once you have installed My Awesome Project, you can use it as follows:

1. Open the application in your web browser.
2. Explore the amazing features of the application and enjoy.
https://misimagenespublicas.s3.amazonaws.com/Screenshot+from+2024-02-04+13-09-56.png

## License
MIT

## Contact
germanfoliaco2@gmail.com
+57 3045891787