import json
import socket
import threading
import requests
import os

print("\n********************The Server Has Started******************** \n")
Ssock_p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ssock_p.bind(("192.168.43.201", 52499))
params = {
        'access_key': '8b7b55ffde4a7166324303e189733607',
    }
api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()
Directory = r'C:\Users\amool\PycharmProjects\ITCE320_Project\server'
if not os.path.exists(Directory):
    os.mkdir(Directory)
file_path = Directory + '/G2.json'

file = open(file_path, 'w')
file.write(json.dumps(api_response, indent=3))  # Saving the retrieved information in a .json file
file.close()

Ssock_p.listen(3)


def accept_connection(sock):
    client_name = sock.recv(1025).decode('ascii')
    clients.append(client_name)
    print("The client -- {} -- is connected".format(client_name))
    arr_icao = sock.recv(1025).decode('ascii')

    def getFlightsDetails(params):
        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
        api_response = api_result.json()

        Directory = r'C:\Users\amool\PycharmProjects\ITCE320_Project\server'
        if not os.path.exists(Directory):
            os.mkdir(Directory)
        file_path = Directory + '/G2.json'

        file = open(file_path, 'w')
        file.write(json.dumps(api_response, indent=3))  # Saving the retrieved information in a .json file
        file.close()

        return (file_path)

    while True:
        option = sock.recv(1025).decode('ascii')
        if int(option) == 1:
            params = {
            'access_key': '8b7b55ffde4a7166324303e189733607',
            'arr_icao' : arr_icao,
            'flight_status' : 'landed'
            }


            with open(getFlightsDetails(params), 'rb') as file:
                toSendFile = file.read()  # Reading the content of the file as a preparation for sending
                sock.sendall(toSendFile)
            print("The requested details about arrived flights "
                  "( Flight code (IATA), Departure Airport, Arrival Time, "
                  "Terminal, Gate ) from client -- {} -- sent successfully".format(client_name))


        if int(option) == 2:
            params = {
                'access_key': '8b7b55ffde4a7166324303e189733607',
                'dep_icao': arr_icao,
                'min_delay_arr': '0'
            }

            with open(getFlightsDetails(params), 'rb') as file:
                toSendFile = file.read()  # Reading the content of the file as a preparation for sending
                sock.sendall(toSendFile)
            print("The requested details about delayed flights "
                  "( Flight code (IATA), Departure Airport, Departure Time, "
                  "Estimated Arrival Time, Terminal, Gate) from client -- {} -- "
                  "sent successfully".format(client_name))

        if int(option) == 3:
            city_code = sock.recv(1025).decode('ascii')
            params = {
            'access_key': '8b7b55ffde4a7166324303e189733607',
            'arr_icao' : arr_icao,
            'dep_iata' : city_code
            }

            with open(getFlightsDetails(params), 'rb') as file:
                sendfile = file.read()
                sock.sendall(sendfile)
            print("The requested details from client -- {} -- sent successfully".format(client_name))

        if int(option) == 4:
            flightName = sock.recv(1025).decode('ascii')
            params = {
                'access_key': '8b7b55ffde4a7166324303e189733607',
                'arr_iata': arr_icao,
                'flight_number': flightName
            }

            with open(getFlightsDetails(params), 'rb') as file:
                sendfile = file.read()
                sock.sendall(sendfile)
            print("The requested details from client -- {} -- sent successfully".format(client_name))

        if int(option) == 5:
            clients.remove(client_name)
            print("Connection with client -- {} -- is closed".format(client_name))
            break

clients = []
while True:
    Ssock_a, sockName = Ssock_p.accept()
    t = threading.Thread(target=accept_connection(Ssock_a))
    t.start()
