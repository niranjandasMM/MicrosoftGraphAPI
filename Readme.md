Offical Docs and more features to follow : https://learn.microsoft.com/en-us/graph/overview

1. First install two modules using pip : 
    pip3 install python-dotenv && pip3 install msal

2. In Your Azure AD : https://portal.azure.com/#home
     - Register an app under app registrations of azure services (No subrciptions are needed to use this service.)
        Learn how to : https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application
        and set redirect URLs to by default : https://localhost:3000
     - You can see your Application (client) ID in Overview. Copy that and paste it in your .env file
     - Make sure that under your app name, in authentication tab in advanced setttings that 'Allow public client flows
' is enabled.
<br>
<img width="1434" alt="Screenshot 2023-11-24 at 3 35 08 PM" src="https://github.com/niranjandasMM/MicrosoftGraphAPI/assets/85221814/47b76ff4-0f93-4b02-aaba-ff264146f584">
<br>
  
4. Running the scripts :
     - First run the config_first.py file to generate a api_token.json which will authenticate your account.
         This will take you to a web browser for logging in and further Installation, while running this print a user_code, copy that and            paste it in web browser asking for the code and follow your rest of the login process.
         It will generate a api_token_access.json in your CWD. Once done, you don't have to login again except when you changed permissions           or updated any scopes, delete and run the config_first.py  again. 

      - Run DownloadFromOneDrive.py, OutlookEmailsRead.py and UploadToOneDrive.py predifined sripts. Update and add more features as per your needs by reading the Api Docs :  https://learn.microsoft.com/en-us/graph/overview
