import socket

#Send to server
def mysend(client_socket, param):
    client_socket.sendall(param)
    return None

#Recive from server

def myreceive(client_socket):
    data = client_socket.recv(5000)
    return data.decode('utf-8')

#Close connection
def terminate_client_communication(client_socket):
    client_socket.close()

#initliaze connection
def init_client_communication():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    return s
