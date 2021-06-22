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
import sys
import errno 
import os 

#limpiar pantalla 
if os.name == "posix":
    var = "clear"
elif os.name =="ce" or os.name == "nt" or os.name =="dos":
    var ="cls"
os.system(var)

HEADER_LENGTH =10


#aqui va la ip y el puerto del server
IP = 'localhost'
PORT = 1354


print('''
███    █▄     ▄████████    ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███   ███    ███ 
███    ███   ███    █▀    ███    █▀    ███    ███ 
███    ███   ███         ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███    ███ ▀███████████ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    ███          ███   ███    █▄  ▀███████████ 
███    ███    ▄█    ███   ███    ███   ███    ███ 
████████▀   ▄████████▀    ██████████   ███    ███ 
                                       ███    ███
by: biyivi
''')
my_username = input("Nombre de usuario: ")
os.system(var)
print( '''
   _     _     _     _     _     _     _     _     _     _  
  / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
 ( B ) ( i ) ( e ) ( n ) ( v ) ( e ) ( n ) ( i ) ( d ) ( o )
  \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 

''')
#Creando un socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True: 
    message = input(f'{my_username} > ')

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Conexion cerrada por el servidor....')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')
    
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error: {}'.format(str(e)))
        
        continue
    except Exception as e:
        print('Error: '.format(str(e)))
        sys.exit()
