import json, requests, tweepy # Standard libs (pip install git+https://github.com/tweepy/tweepy)
from threading import Timer # Threading for the timers
from time import sleep # Sleep to loop once per min

# Mining Rig Rentals vars
url = "https://www.miningrigrentals.com/api/v2/rig/"
id = "92087"

# Twitter vars (Get these from apps.twitter.com)
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'

# Timing vars
completeTimerStarted = periodicTimerStarted = False # Checks to see if timers are already set
periodicTimerFrequency = 600 # Post every 10 mins the periodicAlert

#create Twitter OAuthHandler instance and shits
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def rentalDone(): # Rental has finished, post it to twitter!
    global completeTimerStarted
    # Call Twitter flow
    print('The rental has been completed! Rent now!')
    api.update_status('The mining4vets rental has been completed! Rent now! You can start buying hashrate here: http://rig.rent/rigs/92087')
    completeTimerStarted = False # Start a new timer

def periodicAlert(): # Post status every once in a while, or at the start of a new renting session.
    global periodicTimerStarted

    #Convert the hours and decimal to HRF
    time = float(result['data']['status']['hours'])
    hours = int(time)
    minutes = int((time*60) % 60)
    seconds = int((time*3600) % 60)

    # Call Twitter flow
    print('The rig is being rented for ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' more seconds!')
    api.update_status('The mining4vets rig is being rented for ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' more seconds! You can start buying hashrate here: http://rig.rent/rigs/92087')
    periodicTimerStarted = False # Start a new timer

r = requests.get(url + id)
result = json.loads(r.text)
periodicAlert()
while True:
    # Get newest data from miningrigrentals.com
    r = requests.get(url + id)
    result = json.loads(r.text)
    if result['data']['status']['status'] == "rented": # Check if rig is rented
        if not completeTimerStarted: # Start timer if it isnt already
            completeTimerStarted = True
            hours = float(result['data']['status']['hours'])
            t = Timer((hours * 60 * 60), rentalDone)
            t.start()
        if not periodicTimerStarted: # Start the periodicAlert timer if it isnt already
            periodicTimerStarted = True
            t2 = Timer(periodicTimerFrequency, periodicAlert)
            t2.start()
    else:
        print('not rented')
    sleep(60) # Only check once per minute
