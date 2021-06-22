'''
coded by:
  _         _      _  _     _               _    
 | |__     (_)    | || |   (_)    __ __    (_)   
 | '_ \    | |     \_, |   | |    \ V /    | |   
 |_.__/   _|_|_   _|__/   _|_|_   _\_/_   _|_|_  
_|"""""|_|"""""|_| """"|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''



import socket 
import select
import os

#limpiar pantalla 
if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"
os.system(var)

HEADER_LENGTH =10
# Aqui debes poner tu ip privada para que otros puedan conectarse
#pero en este caso use el localhost
IP = 'localhost'
PORT = 1354

#Creando un socket
#socket.AF_INET = es el dominio del conector. En este caso, un conector IPv4.

'''
socket.Sock_Stream : tipo del conector (no todos los dominios soportan los mismos
 tipos). En este caso, un conector de tipo STREAM: usando el protocolo TCP, que
 proporciona ciertas garantias de seguridad: los paquetes llegan en orden,
 descartando los repetido y/o dañados.

''' 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}

print('''

  ██████ ▓█████  ██▀███   ██▒   █▓▓█████  ██▀███  
▒██    ▒ ▓█   ▀ ▓██ ▒ ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒███   ▓██ ░▄█ ▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒▓█  ▄ ▒██▀▀█▄    ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒░▒████▒░██▓ ▒██▒   ▒▀█░  ░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒▓ ░▒▓░   ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░ ░ ░  ░  ░▒ ░ ▒░   ░ ░░   ░ ░  ░  ░▒ ░ ▒░
░  ░  ░     ░     ░░   ░      ░░     ░     ░░   ░ 
      ░     ░  ░   ░           ░     ░  ░   ░     
                              ░                   
by: biyivi
''')
print(f'Esperando conexiones en {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:

        return False 
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user 

            print('Nueva conexion >> {}:{}, usuario: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)

            if message is False:
                print('Cerrando conexion con: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                sockets_list.remove(notified_socket)

                del clients[notified_socket]

                continue
            user = clients[notified_socket]
            print(f'Mensaje recibido de >> {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'] )
    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)

        del clients[notified_socket]            
