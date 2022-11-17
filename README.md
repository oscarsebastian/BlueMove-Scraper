# BlueMove-Scraper
Script to scrape Aptos drops on bluemove.

# What do I need to know?

*BlueMove's api is protected by cloudflare since it should not be able to be accessed by non authorised devices, in order to avoid getting blocked we will be using cloudscraper library.
*Scraper will send a webhook whenever a new drop is scheduled for the current date.
*<b>You must have a checked_collections.csv in the same folder as main.py</b>
# How do I use it?

Just unpack the zip and install requirements with <b>pip install -r requirements.txt</b>
<br>
<b>Then open main.py and input your webhook url in the function call.</b>

Enjoy!
