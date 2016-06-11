
# Description
This application retrieves the top 100 words from any URL submitted through its form.

# Installation
Pull the repository from the the command line
> git remote add origin https://github.com/yassinemaaroufi/octo-words.git

> git push -u origin master

Upload the application on Google App Engine
> cd project-folder
> appcfg.py update .

Access the application on [Google App Engine](http://octo-words.appspot.com)

# How to use the application
Display the word cloud
1. Enter the URL you want to analyze in the form field
2. Press the submit button
3. Enjoy!

Login to the admin page
1. Click the admin page link
2. Enter the following credentials: admin/admin

# Components
This application is built on top of:
+ [Google App Engine](https://cloud.google.com/appengine/)
+ [Tornado](http://www.tornadoweb.org/)
+ [Google Cloud SQL (MySQL)](https://cloud.google.com/sql/)
+ [Python-RSA](http://stuvel.eu/rsa)
+ Hashlib

# Data storage
This application stores the data it retrieves as hashes and encrypted data
+ Data is best stored as hashed content especially for passwords and other sensitive data. This way in case of breach the users' data is not exposed since the original data cannot be extracted from the hashes directly. For additional security salt is added prior to hashing to prevent dictionary attacks on the breached data.
+ Asymmetric or symmetric encryption can be used to store other data that needs to be occasionally retrieved and used such as emails, addresses and other personal or sensitive data.
+ Salts and encryption keys must be kept in separate databases for additional protection although they were included in the code here.

# TODO
+ Upload latest version to github
+ Upload latest version to app engine
+ Create Cordova version
+ Remove dead code
