import indicoio
indicoio.config.api_key = 'db91e10ba18babcf6e5e5209a5f0ab6f'

# single example
indicoio.sentiment("I love writing code!")

# batch example
print(indicoio.sentiment([
    "I love writing code!",
    "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
]))
