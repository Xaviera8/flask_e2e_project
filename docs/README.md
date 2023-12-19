# flask_e2e_project

# Final Assignment (Product / Web Service)



## My Webservice
The webservice I created is a crude copy of the application MyFitnessPal. This webservice allows a user to record and track their weight and view the logs in a table sorted by time.

Technologies Used
Github (Version Control)
Flask (Python; Frotend & Backend)
MySQL (GCP Database)
SQLAlchemy (ORM)
.ENV (Environment Variables)
Tailwind (Frontend Styling)
Authorization (Google OAuth)
API Service (Flask Backend)
Sentry.io (Logging)
Docker (Containerization)
GCP or Azure (Deployment)

The steps to run your web service if someone wanted to either run locally or deploy to the cloud
## How to run it without Docker locally? 
A user would have to clone my github repository into their ide of choice. Select the code button, copy url to clipboard. In the ide terminal use the function git clone <url>. Once cloned, the user would have to select the folder app as their present working directory. cd flask_e2e_project, then cd app.py. Once app.py is their present working directory, the user can call the function python app.py to run the webservice. Once run, a local host url will appear, the user can click that link to access the webservice. 

## How to run it with Docker locally?
User would have to set app as their present working directory. Once that is set they will use the command docker build -t xavier . in the terminal. Next they will enter docker run xavier.
## How to deploy it to the cloud?

## Linking with Azure
In the google shell, you have to download the Azure Command Line Interface to interact with the Azure Cloud Service. This can be done by using the command "curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"

## Log-in with Azure Account
After installed, you can login with your Azure Account using the command, az login --use-device-code. This will prompt you to click a hyperlink and enter a code that will link your azure account to your google cloud session

## Change subscription ID
After you are logged in, you have to change your subscription ID to the subscription linked to your stony brook account. You can find the azure student subscription ID with the following command: 'az account list --output table'. You can set the subscription ID with the following command: 'az account set --subscription'.

## Creating a resource group
Now that the Google shell session and the azure cloud service are linked, you can log into the azure web portal and create a new resource group. This can be done on the homepage under the azure services.

## Deployment
The final step to deploy your flask application is to enter the following command into the terminal of your google shell session.
"az webapp up --resource-group 'groupname'> --name 'app-name' --runtime PYTHON:3.9 --sku B1". The values encased in the ' ' must be replaced with the information for your application.


## .ENV File Structure        
database = 
user = 
password = 
host = 
db_url = 
GOOGLE_CLIENT_ID = 
GOOGLE_CLIENT_SECRET = 

## Errors
I primarily had issues with the docker image and deployment.

### Docker
