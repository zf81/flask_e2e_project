# flask_e2e_project

# Final Assignment- Product / Web Service

## Web Service: 
The web service created for this project was a flask app that displays a urology database that contains fake healthcare data. It consists of three tabs the user can navigate to. The Home page welcomes the user to the urology database and allows them to log in. The Patients page contains a table that displays patient contact information. The Prostate page displays a table containing different data points relating to prostate cancer. A urologist I work with as a medical scribe uses these data points for new patients when determining what the next steps in their care should be. PSA is a blood test. Prostate volume is the size of the prostate. ExoDx score ranges from 0 to 100 and is one of the tests the urologist uses to determine if the patient should proceed with a prostate biopsy. The MRI Prostate column contains data that is found under the impression in MRI reports, specifically focusing on the PIRADS score. The Decipher score ranges from 0.0 to 1.0 and examines the likelihood of metastasis of prostate cancer. The Encounter page contains a table that displays some portions that would be found in a typical note. Family History is usually mentioned in the HPI as well as Lower Urinary Tract Symptoms (LUTS). The result of a digital rectal exam is another factor the urologist uses to determine if the patient should proceed with a prostate biopsy. The Treatment column contains some treatment options the urologist discuses with the patient if they have prostate cancer. When choosing a treatment, there is a thorough discussion factoring in the patient's age, comorbidities, and whether or not the patient has high risk prostate cancer. The final tab is a Profile page that displays a user's information after they log in. If a user clicks on this page if they aren't logged in, they would be redirected to the homepage. 

## Technologies Used:
- I created folders and files and did all coding in the Google Cloud Shell environment 
- The database was created and hosted on an Azure Database for MySQL flexible server
- Used SQLalchemy to create data tables and populate them with fake information 
- The flask app was created in a [python file](https//g.py)
- The flask app was styled with tailwind css and I built in Logger to the app
- Implemented Google Oauth which was used to allow users to log into the app with their Gmail logins
- The app has an **API service**. Specific queries can be made through the URL and this will display specific information from each table. Sample queries are located in the <code>docs</code> folder 
- The app was  conainerized through **docker**
- In order to run the app locally, type <code> python app.py </code> in terminal
- Be sure to <code>cd</code> into the app file (I first cd into the app folder which contained app.py file)
- To run on docker, be sure that all necessary files and folders are in the same level as the Dockerfile otherwise you will get an error 
- To run the image, enter docker run -p -d [machine-port-number]:[docker-image-port-number] [image-name]
- I deployed the app through Azure. Here is the link: https://urologyapp.azurewebsites.net
- The app was able to load the patients data page successfully after deploying through Azure. However, when I tried to load other pages I received an error page. Screenshot of this is located in <code>docs</code> folder. 


### Steps to Deploy Flask APp Through Azure:
- Make sure you are cd into the correct directory that contains your app
- Within the Google Shell terminal, you will need to install [AZURE CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt) using: ```curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash```. Copy and paste the line in and enter.
- Then type in ```az```
- Type in ```az login --use-device-code``` and you will see a link and code in the terminal. Copy the code and click the link to log in to your Azure account. This will help connect your Google Shell with your Azure account.
- Log in to your [Azure account](https://azure.microsoft.com/en-us/). Navigate to Resource Group and create a new Resource Group with a unique name and click **Review and Create**. 
- Go back to Google Shell and in the terminal, enter ```az account list --output table``` to check that you have the correct subscription for your Azure account. 
- If the correct subscription ID is not set, type in ```az account set --subscription <paste the desired SubscriptionId here>```.
- Type in ```az group list```.
- Enter in ```az webapp up --resource-group <resource group that you named> --name <replace with your desired webapp name> --runtime PYTHON:3.9 --sku B1```. Once entered, the Azure app service will create the web app for you.
   - Note: this step may take a while to load.
- After the deployment is complete, go to App Service in Azure. Select the web app you created. You will see an overview of the web app
- You can find the link for your web application at Default domain. Click on the link and you should be redirected to your web application.


## Template of the .env file:
For the Google OAuth, I entered: 
```
GOOGLE_CLIENT_ID = <store the client-id for your web application from Google Cloud Credentials>
GOOGLE_CLIENT_SECRET = <store the client-secret also generated on Google Cloud Credentials>
```

For the MySQL connection and for migrations:
```
DB_HOST = <IP address if using GCP>
DB_DATABASE = <enter your databasename>
DB_USERNAME = <username>
DB_PASSWORD = <password>
DB_PORT = 3306
DB_CHARSET = utf8mb4
```
