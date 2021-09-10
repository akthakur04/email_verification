# email_verification_system
An Email verification system project made using Django rest framework. This project allows to <ul>resiter email</ul> <ul> login user with email</ul><ul>see user list</ul><ul>Logout
The url links are in emailapi/urls.py</ul>


To register a user run the project go to http://127.0.0.1:8000/api/register/ and add the fields. Or use postman to check the link. username,Emaila and password field are to be filled.
On success full registration check your mail inbox for verification link. Click on link to verify you email
To Login a user run the project go to http://127.0.0.1:8000/api/login/ and add the fields. Or use postman to check the link. username,Emaila and password field are to be filled.
To Logout a user run the project and use post man to check the link. Autthorization key with value "Token <token genrated on login>" is to be filled.
Required python libraries are given in requirement.txt
