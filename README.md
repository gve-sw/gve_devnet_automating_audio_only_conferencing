# gve_devnet_automating_audio_only_conferencing

A sample script that sets the users' pins based on predefined data (in a CSV file and as environment variables). Furthermore, a personal audio conference is automatically created for each user. The resulting joining information is sent to the associated user based on an email template. 

## Contacts
* Roaa Alkhalaf
* Ramona Renner

## Solution Components
* Webex Control Hub (Webex admin access)
* Webex Meetings XML API
* Gmail

##  Workflow

![/IMAGES/0image.png](/IMAGES/workflow.png)

## Related Sandbox Environment

This sample code can be tested using a [Cisco Developer Sandbox](https://developer.webex.com/docs/developer-sandbox-guide) which provides you with administrator access to a licensed Webex organization manageable via Webex Control Hub. A licensed org lets you create and test capabilities of the Webex platform that are not available with Webex free plans.

## Prerequisite

To use the Webex Meetings XML API for this demo, you need a Webex admin account. This demo allows using the Webex Control Hub username and password or a Webex oAuth token for authentication purposes. 

If the username and password option is preferred, please skip the following section: "Register a Webex OAuth Integration".

If the oAuth option is preferred, execute the steps described in the following section.

### Register a Webex OAuth Integration

**OAuth Integrations**: Integrations are how you request permission to invoke the Webex REST API on behalf of a Webex Teams user. To do this securely, the API supports the OAuth2 standard, which allows third-party integrations to get a temporary access token for authenticating API calls. 

To register an integration with Webex Teams:
1. Log in to **developer.webex.com**
2. Click on your avatar at the top of the page and then select **My Webex Apps**
3. Click **Create a New App**
4. Click **Create an Integration** to start the wizard
5. Fill in the following fields of the form:
   * **Will this integration use a mobile SDK?**: No
   * **Integration name**
   * **Icon**
   * **App Hub Description**
   * **Redirect URI(s)**: http://localhost:5000/authorize
   * **Scopes**: Select "spark-admin:telephony_config_read spark-admin:telephony_config_write spark:all spark-admin:telephony_config_read spark:telephony_config_write meeting:admin_config_read meeting:admin_config_write"
6. Click **Add Integration**
7. After successful registration, you'll be taken to a different screen containing your integration's newly created Client ID and Client Secret and more. Copy the secret, ID and OAuth Authorization URL and store it safely. Please note, that the Client Secret will only be shown once for security purposes

  > To read more about Webex Integrations & Authorization and to find information about the different scopes, you can find information [here](https://developer.webex.com/docs/integrations)

8. (For demo purposes optional) Generate the self-signed certificate used to serve the Flask web app with HTTPS. This requires OpenSSL tools to be installed (the command below was used on Ubuntu 19.04.). From a terminal at the repo root:     
    ```
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    ```
9. (For demo purposes optional) Fill in the generated value at line 34 of the main_oauth.py file.   

## Installation/Configuration

1. Make sure you have [Python 3.8.10](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

2. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html))   

3. Access the created virtual environment folder
    ```
    cd [add name of virtual environment here] 
    ```

4. Clone this GitHub repository into the local folder:  
    ```
    git clone [add GitHub link here]
    ```
    * For GitHub link: 
      In GitHub, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  

  * Or simply download the repository as zip file using 'Download ZIP' button and extract it

5. Access the downloaded folder:  
    ```
    cd gve_devnet_automating_audio_only_conferencing
    ```

6. Install all dependencies:
    ```
    pip3 install -r requirements.txt
    ```

7. Provide a CSV file with user data or fill in the available CSV template users.csv. The required format is as follows. Each row describes a user that is **available** and **activated** in Webex Control Hub and has the required licenses.

    ```
    First Name,Last Name,Email
    example_first_name,example_last_name,example_email@text.com
    ```

    > Note: Please add no empty spaces between the comma's.

8. Fill in your variables in the .env file. 

  ```python
    
    USERNAME="<Webex Control Hub Admin Username>"

    #For password authentication
    PASSWORD="<Webex Control Hub Admin Password>"

    #Alternative for oauth authentication
    CLIENT_ID="<Webex oAuth client id (see Prerequisite)>"
    CLIENT_SECRET="<Webex oAuth client secret (see Prerequisite)>"

    # Webex sitename, e.g. For cisco.webex.com sitename will be cisco
    SITENAME="<Webex Sitename, e.g. for cisco.webex.com the sitename will be cisco>"

    #Conference PINs
    AUDIO_PIN=<Audio Pin to configure for all users. A PIN must be exactly 4 digits. It can not contain sequential digits or repeat a digit four times.>
    HOST_PIN=<Host Pin to configure for all users. A PIN must be exactly 4 digits. It can not contain sequential digits or repeat a digit four times.>

    #Sender of Emails
    EMAIL_SENDER="<Email address to send the email from>"
    EMAIL_APP_PASSWORD="<Password for above email account. In case of Gmail a specific App Password is required (see https://support.google.com/accounts/answer/185833?hl=en)>" 

    # CSV file with user data
    USER_CSV_FILENAME="<File containing the user data, e.g. users.csv>"
  ```

> Note: Mac OS hides the .env file in the finder by default. View the demo folder for example with your preferred IDE to make the file visible.

9. The email template includes two static phone numbers for call-in. These numbers might differ for your site. Thereby, please adapt lines 24 and 28 of the templates/email_template.html file and lines 7 and 8 of templates/text_template.txt accordingly. The URL is automatically adapted based on the site defined in the .env file.


## Usage

10. Run the script depending on the choosen authentication:   


For username and password:   
```python3 main_UaP.py``` 
     
The script will run without further user interaction.   


For oAuth:   
```python3 main_oauth.py```   
   
Navigate to http://localhost:5000 and follow the authentication workflow. Use your Webex Control Hub admin account to log in during the process.  

## Joining the audio conference

**As host :**
1. Call a number from the email or URL in the template
2. Enter the digit host access code 
3. The system is asking if you are the host: Enter the digit Audio PIN     
Audio bridge is opened as host.
 
**As attendee :**
1. Call a number from the URL in the template
2. Enter the digit attendee access code 
3. The system is asking if you are the host: Enter no pin   
Wait in the lobby for the host to join, or join the meeting if the host is already attending.


# Screenshots

![/IMAGES/0image.png](/IMAGES/screenshot.png)


# Resources

* Webex Meetings XML API - Authentication: https://developer.cisco.com/docs/webex-xml-api-reference-guide/#!request-authentication/request-authentication
* Webex Integrations & Authorization: https://developer.webex.com/docs/integrations
* Run a Webex OAuth Integration Locally: https://developer.webex.com/docs/run-an-oauth-integration
* Google App Password: https://support.google.com/accounts/answer/185833?hl=en


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.