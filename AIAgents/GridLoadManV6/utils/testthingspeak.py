import thingspeak

channel_key = 'U'
channel_id = 12397


ch = thingspeak.Channel(channel_id,api_key=channel_key)
#get one field in channel
#my_results = ch.get_field(field=4,options={'results': 60,'minutes':60})
#my_results = ch.get({'results': 240,'minutes':60})
my_results = ch.get_field(field=1,options={'results': 1000})
print(my_results)
# Open the file in write mode
with open('data/thingspeaktest.txt', 'w') as file:
    file.write(my_results)
