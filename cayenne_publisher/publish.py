from __future__ import print_function
import paho.mqtt.publish as publish
import time
import json



# get configuration
def get_configs():
    with open("./config.json") as config_file:
        config = json.load(config_file)
    return config


# connection_configuration
general_conf = get_configs()['general']

# get cayenne configuration
cayenne_conf = get_configs()['env']['cayenne_test']

'''
cayenne server topic format: 

v1/username/things/clientID/data/channel
'''
cayenne_topic = 'v1/' + cayenne_conf['username'] + '/things/' + cayenne_conf['client_id'] + '/data/'


def publish_cayenne(payload):

    # attempt to publish this data to the topic 
    try:
        print ("Publishing data to Cayenne")
        parsed_payload = json.loads(payload)

        '''
        cayenne payload should be in the form of:

        type,unit=value

        '''

        mqtt_auth = {'username':cayenne_conf['username'], 'password':cayenne_conf['password']}

        for key, value in parsed_payload.iteritems():
            if key == 'rel_hum':
                hum_payload = key + ',p=' + str(value)
                hum_topic = cayenne_topic + "4"
                publish.single(hum_topic+"4", payload=hum_payload, qos=cayenne_conf['qos'], retain=False, hostname=cayenne_conf['broker_address'],
                               port=general_conf['broker_port'], client_id="", keepalive=general_conf['broker_keep_alive'], auth=mqtt_auth)

            if key == 'temp':
                temp_payload = key + ',t=' + str(value)
                temp_topic = cayenne_topic + "5"
                publish.single(temp_topic, payload=temp_payload, qos=cayenne_conf['qos'], retain=False,
                               hostname=cayenne_conf['broker_address'],
                               port=general_conf['broker_port'], client_id="",
                               keepalive=general_conf['broker_keep_alive'], auth=mqtt_auth)

        print("Publishing completed")

    except KeyboardInterrupt:
        print ("Keyboard interrupt")

    except:
        print ("There was an error while publishing the data.")