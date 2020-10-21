# twitter-unfollowers-detector

You know how it goes. Somebody follows you on Twitter and you follow them back, because you are a nice person. But then they go ahead and unfollow you. Not cool, right?  
This script detects this, unfollows them back and - optionally - notifies you via email.

## Requirements
- A Twitter developer account (Apply [here](https://developer.twitter.com/en/apply-for-access))
- A Twitter App with `Read and Write` permissions
- Python 3.6+

## Getting Started
**Clone this repository and `cd` into it:**
```bash
git clone https://github.com/xmac11/twitter-unfollowers-detector.git
cd twitter-unfollowers-detector/
```

**Set required environment variables with your API keys and tokens:**  
- `TWITTER_API_KEY`  
- `TWITTER_API_KEY_SECRET`  
- `TWITTER_ACCESS_TOKEN`  
- `TWITTER_ACCESS_TOKEN_SECRET`  

**Create a virtual environment with Python 3.6 or higher.**

**Install required packages:**    
```bash
pip install -r requirements.txt
```

## Email Notifications
If you would like to be notified via email for any users you unfollow, or any errors that may occur while the script is running:
- Set `FROM_ADDRESS` and `TO_ADDRESS` in `constants/config.py`
- Set `EMAIL_PASSWORD` in your environment variables, corresponding to the password for `FROM_ADDRESS`