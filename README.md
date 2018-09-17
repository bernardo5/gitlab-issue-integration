# gitlabIntegration

This project aims to create an external interface to create and view issues on gitlab. The final result is up and running on Heroku: `https://gitlab-web-app.herokuapp.com/`

This code is a copy of `https://gitlab.com/bernardo5/gitlabIntegration` were the code was stored as the development occurred.

## Start developing / setup locally

1. Clone the repository

2. Create a virtualenv: `virtualenv venv`

3. Run `source venv/bin/activate`

4. Install the requirements in your virtual environment: `pip install -r requirements.txt`

## Requirements

Apart from the process above, you will only need to have a gitlab token that can be fetched following the steps in `https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html`

## View Issues

Ideally, this app should be able to fetch the issues and display them, however, Gitlab returns a message in the issue `Description` field saying that issues descriptions should not be displayed in web apps. Consequently, it was decided that the issues could be displayed in column and with an hyperlink to the the issue itself on Gitlab

## References

This project uses the `python-gitlab package` with the following documentation: `https://python-gitlab.readthedocs.io/en/stable/`