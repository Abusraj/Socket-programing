import socket
import threading
import random
# Constant area
########
# Fixed size
HEADER = 16
PORT = 1234
#Getting client ip
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# Exit messege
DISCONNECT = "close"
# Finding the primative root of n is difficult so we put 23 with inputs for a
Q = 23
#########

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Handling all connected clients here in each thread
def handle_client(conn, addr):
    print(f'[WELCOME] {addr} ! \n')
    a = get_root(Q)
    connected = True
    while connected:
        print(f'q(mod)={Q} and a(base){a}')
        keyQ = str(Q).encode(FORMAT)
        keyA = str(a).encode(FORMAT)
        conn.send(keyQ)
        conn.send(keyA)
        Xa = get_private(Q)
        Ya = get_public(Xa, Q, a)
        Yb_len=conn.recv(HEADER).decode(FORMAT)
        Yb = conn.recv(int(Yb_len)).decode(FORMAT)
        print(f' USER A Public key {Ya} \n')
        Yb=int(Yb)
        print(f' USER B Public key {Yb} \n')
        k = pow(Yb, Xa, Q)
        Ya=str(Ya).encode(FORMAT)
        R=str(get_R()).encode(FORMAT)
        conn.send(Ya)
        conn.send(R)
        R=int(R)
        print(f' The Challenge R= {R} \n')
        G_len=conn.recv(HEADER).decode(FORMAT)
        G=conn.recv(int(G_len)).decode(FORMAT)
        R_bar=int((G))/k
        print(f' R\' = {R_bar} \n')
        R_bar=int(R_bar)
        if((R==R_bar)):
            print(("[Authontication Success!] \n"))
            conn.send("[Success!]".encode(FORMAT))
        else :
            print(("[Authontication Failed!] \n"))
            conn.send("[Failed!]".encode(FORMAT))
        # exit msg
        messeage_length=conn.recv(HEADER).decode(FORMAT)
        msg=conn.recv(int(messeage_length)).decode(FORMAT)
        if (str(msg) == DISCONNECT):
            connected = False
    # exit 
    conn.close()

# Get randomize primative root of 23 
def get_root(Q):
    list = [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
    return list[random.randint(0, len(list)-1)]

#check the value
def authonticate(R,R_bar):
    return R==R_bar
# get private key
def get_private(Q):
    flag=True
    while flag:
        serv=int(input(f"Enter Xa < {Q} \n"))
        if(serv<Q and serv>0):
            return serv
        else:
            print("Try again \n")
    
# Get R value
def get_R():
    flag=True
    while flag:
        serv=int(input("Enter R(The challenge): \n"))
        if(serv<300):
            return serv
        else:   
            print("Try again \n")


# get public key
def get_public(Xa, q, a):
    return pow(a, Xa, q)

# start the program and threads
def start():
    server.listen()
    while True:
        print(f'[SERVER IS LISTENING] on {SERVER} \n')
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count()-1} \n')


print("[STARTING] SERVER IS ON....")
start()
