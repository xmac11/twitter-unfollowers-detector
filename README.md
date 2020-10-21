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

**Set the required environment variables with your API keys and tokens:**  
- `TWITTER_API_KEY`  
- `TWITTER_API_KEY_SECRET`  
- `TWITTER_ACCESS_TOKEN`  
- `TWITTER_ACCESS_TOKEN_SECRET`  

**Create a virtual environment with Python 3.6 or higher.**

**Install required packages:**    
```bash
pip install -r requirements.txt
```

**Run the script:**
```bash
python twitter_unfollowers.py
```

###### Example output:
```
1 user(s) unfollowed you {'00001': 'TwitterUsername'}
Unfollowed TwitterUsername (user_id='00001')
```
A complete history of the results is kept in `logs/unfollowers.log`

## Email Notifications
If you would like to be notified via email for any users you unfollow, or any errors that may occur while the script is running:
- Set `FROM_ADDRESS` and `TO_ADDRESS` in `constants/config.py`
- Set `EMAIL_PASSWORD` in your environment variables, corresponding to the password for `FROM_ADDRESS`

## Schedule the script
To get the most out of the script, you could schedule it to run periodically using cron jobs or Windows Task Scheduler.

**Disclaimer**: This project was built for fun while learning Python :)