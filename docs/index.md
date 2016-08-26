# Partisan Discourse

**A web application that identifies bias in political discourse and serves as a template for operationalized machine learning.**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coveralls_href]
[![Stories in Ready][waffle_img]][waffle_href]
[![Political Parties](img/partisan.jpg)][partisan.jpg]

For an in-depth description of the project's purpose, head to the [About](about.md) page.

## Quick Start Guide for Developers

**Note:**
This project uses Django and Python 3. If you're unfamiliar with Django, it may be helpful to go through their [tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/).

1. **Clone the repository:**

        $ git clone git@github.com:DistrictDataLabs/partisan-discourse.git
        $ cd partisan-discourse


2. **Create a virtualenv and install the dependencies:**

        $ virtualenv venv
        $ source venv/bin/activate
        $ pip install -r requirements.txt


3. **Download NLTK data, which the app uses for NLP purposes.** Open python in your REPL:

        >>> import NLTK
        >>> nltk.download()


    You should have a directory within your home directory called "nltk_data". You'll use the path to that directory in your .env file, which we'll establish soon.

4.  **Google OAuth Client ID and Secret.** Google OAuth is for enabling API access from Google+, which is the method by which users interact with our app.
      - Head to the [Google developer console page](https://console.developers.google.com), and click on the "Credentials" tab on the left-hand side of the screen. In the center of the screen, click the "Create a Project" button. Name the project "Partisan Discourse," and if you agree to the terms of service, fill the "yes" radio button and click "Create."
      - In the upper-middle section of the page, click "OAuth consent screen." Fill in the product name with "Partisan Discourse;" you can leave the rest blank as long as you're just developing. Click the "Save" button.
      - Back under the main "Credentials" page, click the "Create credentials" drop-down button, and select the "OAuth Client ID" option. The page will prompt you to select an application type; select the "Web application" radio button.
      - Name the app "Partisan Discourse." In the "Authorized JavaScript origins" field, enter **http://127.0.0.1:8000**. Under "Authorized redirect URIs," enter **http://127.0.0.1:8000/complete/google-oath2/**. Click "create," and you should receive your OAuth client ID and secret.  


        Save your ID and secret; you'll use them soon to allow users to interact with your API using their Google+ information.  


5.  **Bitly Access Token.** Partisan Discourse shortens URLs using the Bitly service. Go to Bit.ly and create an account.
    - After creating an account, click on the menu icon at the top right corner of the screen. Go to Settings > Advanced Settings, and click on the "OAuth" link under the "For Developers" section. You should arrive at the [Bitly OAuth page](https://bitly.com/a/oauth_apps).
    - Click on the "Register an Application" link, then click on the "Get Registration Code" button. Check the email account that you used to sign up for Bitly, and click on the link in the email that says "Verify your Email."
    - After verifying your email, head back to the [manage my apps](https://bitly.com/a/oauth_apps) page, and click "generate token."
    - You should have received another email from Bitly; in it, click "Complete Registration." Name it Partisan Discourse, and set the link to **http://127.0.0.1:8000/** (Django's default port is 8000). The redirect link should be **http://127.0.0.1:8000/complete/google-oauth2/**. The description that we use is "A web application that identifies party in political discourse and serves as an example of operationalized machine learning." Click "Create Your App" at the bottom of the page.
    - At this point, you should see a page that gives you a client ID, a client secret, and a generic access token.


        Save your access token; you'll use it soon to allow app users to connect to the Bitly API.   


6.  **Create a .env file for your environment variables:**

        $ touch .env  
        $ open .env

    Paste in the following:

        WEB_CONCURRENCY=2  
        DATABASE_URL=postgres://django@localhost/partisan  
        DJANGO_SETTINGS_MODULE=partisan.settings.development  
        SECRET_KEY=""  
        EMAIL_HOST_USER=""  
        EMAIL_HOST_PASSWORD=""  
        GOOGLE_OAUTH2_CLIENT_ID="your-oauth-client-ID"  
        GOOGLE_OAUTH2_CLIENT_SECRET="your-oauth-client-secret"  
        BITLY_ACCESS_TOKEN="your-bitly-access-token"  
        NLTK_DATA= /path/to/your/NLTK/data  

      Here's an explanation of each of the .env lines and their purposes:  

    - **Web concurrency:** Heroku hosting setting.
    - **Database URL:** describes how to connect to Postgres locally. Here, you're specifying to use the Postgres protocol, which is necessary for Partisan Discourse. The "django@localhost" specifies that the user should be "django" and the database should be "partisan".
    - **Django settings module:** specifies where to retrieve the settings documents. Instead of just using a settings.py, we use different settings documents for production, development, and testing. Changing the DJANGO_SETTINGS_MODULE in your .env file will change the settings that you use accordingly.
    - **Secret key:** additional security. Using the secret key in your .env file (and including your .env file in your .gitignore file) will help prevent unauthorized access to your app.
    - **Email host user and password: this allows Django to send email on your behalf.
    - **Google OAuth Client ID and secret** (referenced earlier): replace the quotation marks with your client ID and secret.
    - **Bitly Access Token:** URL shortening (referenced earlier); replace the quotation marks with your access token.
    - **NLTK data:** paste the path to your nltk_data directory. It should have installed to your home directory.  



7.  **Set up your Postgres database.** Ensure that Postgres is running. Next, create the proper role ("django") and database ("partisan") by typing the following into your psql terminal window:

        =# CREATE ROLE django WITH LOGIN;
        =# CREATE DATABASE partisan WITH OWNER django;

    When you view your databases, you should now see one with the name "partisan" and the owner "django."

8. **Migrate the app.** Django uses migrations to propogate changes you've made in your models (like adding a field) into your database schema. Enter the following into your terminal:

        $ python manage.py migrate


9. Run the server. By default, Django uses port 8000.

        $ python manage.py runserver

      In your web browser, go to address 127:0.0.1:8000. If you see a login page, then congratulations! You have successfully set up Partisan Discourse locally!





## Contributing to Partisan Discourse

1. Head to the [Github repository](https://github.com/DistrictDataLabs/partisan-discourse) and fork the project.  


2. Check out the appropriate branch:  

        $ git fetch origin develop
        $ git checkout develop  


3. After making changes that you feel would benefit the project, push them to Github:


        $ git add .
        $ git commit -m "bug fix #[insert fix number here]"
        $ git push origin develop


4. Submit a pull request. Head to the Partisan Discourse [Github repository](https://github.com/DistrictDataLabs/partisan-discourse), click on "pull requests," and then click on "new pull request." Choose the proper base fork and branch (Partisan Discourse; develop) and the proper head fork and branch (your fork; develop).

If you find an issue but can't fix it, be sure to submit an issue [here](https://github.com/DistrictDataLabs/partisan-discourse/issues).  



#### Changelog

The release versions that are deployed to the web servers are also tagged in GitHub. You can see the tags through the GitHub web application and download the tarball of the version you'd like.

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

#### Version 0.1 Beta 1

* **tag**: [v0.1b1](https://github.com/DistrictDataLabs/partisan-discourse/releases/tag/v0.1b1)
* **deployment**: Monday, July 18, 2016
* **commit**: [see tag](#)

This is the first beta release of the Partisan Discourse application. Right now this simple web application allows users to sign in, then add links to go fetch web content to the global corpus. These links are then preprocessed using NLP. Users can tag the documents as Republican or Democrat, allowing us to build a political classifier.

#### Attribution

The image used in this README, [Partisan Fail][partisan.jpg] by [David Colarusso](https://www.flickr.com/photos/dcolarusso/) is licensed under [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/)

<!-- References -->
[travis_img]: https://travis-ci.org/DistrictDataLabs/partisan-discourse.svg
[travis_href]: https://travis-ci.org/DistrictDataLabs/partisan-discourse
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/partisan-discourse.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/partisan-discourse
[coveralls_img]: https://coveralls.io/repos/github/DistrictDataLabs/partisan-discourse/badge.svg?branch=master
[coveralls_href]:https://coveralls.io/github/DistrictDataLabs/partisan-discourse?branch=master
[partisan.jpg]: https://flic.kr/p/a3bXVU
