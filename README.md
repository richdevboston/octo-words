
# Description
This application retrieves the top 100 words from any URL submitted through its form.

# Installation
Pull the repository from the the command line
> git remote add origin https://github.com/yassinemaaroufi/octo-words.git
> git push -u origin master

Upload the application on Google App Engine
> cd <project-folder>
> appcfg.py update .

Access the application on [Google App Engine](http://octo-words.appspot.com)

# How to use the application
1. Enter the URL you want to analyze in the form field
2. Press the submit button
3. Enjoy!

# Components
This application is built on top of:
+ Google App Engine
+ Tornado
+ MySQL
+ [Python-RSA](http://stuvel.eu/rsa)

# TODO
+ Upload latest version to github
+ Upload latest version to app engine
+ Create Cordova version
+ Exceptions: request timeout, URL not available
+ Add taskqueues to insert data into DB?
