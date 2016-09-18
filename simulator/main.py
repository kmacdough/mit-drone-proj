"""
main.py

Run the simulator using the scenario from the command line argument
"""
import sys
import requests
from drone import Drone
from config import read, API_HOST

def main(scenario):
    config = read(scenario)
    duration = config['duration']
    drone_list = config['drones']
    parcels = config['parcels']
    places = config['places']
    users = config['users']

    for user in users:
        user['id'] = requests.post(API_HOST + '/user', json=user).json()['data']

    for place in places:
        place['id'] = requests.post(API_HOST + '/place', json=place).json()['data']

    for parcel in parcels:
        parcel['origin_id'] = [place['id'] for place in places if place['name'] == parcel['origin']][0]
        parcel['destination_id'] = [place['id'] for place in places if place['name'] == parcel['destination']][0]
        parcel['sender_id'] = [user['id'] for user in users if user['email'] == parcel['sender']][0]
        parcel['recipient_id'] = [user['id'] for user in users if user['email'] == parcel['recipient']][0]

    drones = [Drone(drone['lat'], drone['long'], parcel) for drone in drone_list]
    for i in range(duration):
        for parcel in parcels:
            if parcel['time'] == i:
                print(parcel)
                response = requests.post(API_HOST + '/parcel', json=parcel)
                print(vars(response))
        for drone in drones:
            drone.on_tick()



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Syntax: python main.py <scenario>')
    else:
        scenario = sys.argv[1]
        main(scenario)