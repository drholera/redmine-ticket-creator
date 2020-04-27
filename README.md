# Redmine Ticket Creator

![Build Status](https://travis-ci.com/drholera/redmine-ticket-creator.svg?branch=master) [![codecov](https://codecov.io/gh/drholera/redmine-ticket-creator/branch/master/graph/badge.svg)](https://codecov.io/gh/drholera/redmine-ticket-creator)

# Use cases
Very often we need to create a ticket in Redmine which will contain a list of "What we're going to deploy". This tool will help you to create such a ticket very fast.

The tickets which will be deployed must be assigned to a "Deployment" group in Redmine. 

# Installation
1. Clone or download this repository
2. Run `pip install -r requirements.txt`
3. (optional) If you're using Windows 10 run `pip install -r requirements-win.txt`

That's all, you're ready to configure your Ticket Creator.

# Configuration

1. Open ```config/config.yml```
2. Add a proper information to required variables. For examlple - if you have only 2 Deployment Groups - for Preprod and Prod servers you can just delete ```dev``` and ```stage``` rows. 
3. If you have httpAuth in your Redmine - switch `http_auth['enabled']` var to `True` and enter username and password to variables below.
4. That's all, you're about to start!

# Usage
To execute program you need to run command:

```python  main.py```

Select required environment you're going to deploy.

You'll see list of tickets you have assigned to required depoyment group. 

If you will select "y/yes" the deployment ticket will be created after that and you'll see the link to it.

If you select "n/no" - program will be finished, no tickets will be created.

## Contribution
Please feel free to create an issue and advise what functionality also could be added and will be helpful. Thanks!