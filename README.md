# Instacart Ref Generator
## Description
This is a simple script that generates a referral link for [Instacart](https://www.instacart.com/store/referrals). It is written in Python 3.9 and uses the [Requests](https://requests.readthedocs.io/en/master/) library to make HTTP requests to Instacart's servers.

This script will create a web server on port 19320 and will listen for requests. When a request is received, it will respond with a referral link. The referral link is generated using the cookies from the `cookies` folder.

## Usage
1. Install dependencies with `pip install -r requirements.txt`
2. Create txt files in folder `cookies` saving the cookies from the Instacart referral website.
3. Run the script with `python app.py`