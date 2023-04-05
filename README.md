# Hellbug

Sync your posts Hellsite (tumblr dot com) to Cohost.org

## Setup

0. Use python 3.9 or newer
1. Clone this repo
2. Install requirements with `pip install -r requirements.txt`
3. Setup the following environment variables:

- `TUMBLR_KEY` - your API key for Tumblr
- `TUMBLR_URL` - the URL of the Tumblr blog you wish to sync
- `COHOST_EMAIL` - the email you use to login to Cohost
- `COHOST_PASS` - your password for Cohost
-  [Optional] `COHOST_PROJECT` - the page you want to post to on Cohost. If not specified, will use your default page
- [Optional] `TUMBLR_TAG` - the tag required on a post for Hellbug to sync it. Defaults to `txt`. You can turn off tag filtering by setting this to an empty string `export TUMBLR_TAG=""`

4. Run `python main.py`
5. The latest matching tumblr post will be posted to Cohost!

To run this automatically, set this script up in a Cron job. Be wary of Tumblr's API limits of 5000 API calls a day - do not run this script more than once every 5 seconds.

As of now the script will only get the *latest* post, and will not recurse back.