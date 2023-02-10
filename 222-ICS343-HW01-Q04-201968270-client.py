import random
import socket
# Constant area
########
# Fixed size
HEADER=16
# Our port
PORT=1234
# Our cliner
# clinER= "100.50.200.5"
clinER="192.168.1.129" 
# Sending Protocol
FORMAT='utf-8'
# Address
ADDR=(clinER,PORT)
#########
# Initilizing socket 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Send function encodes the messege then pads it to reach the required amount before sending it 
def send(msg):
    msg=str(msg).encode(FORMAT)
    msg_len=len(msg)
    send_len=str(msg_len).encode(FORMAT)
    send_len+= b' '*(HEADER-len(send_len))
    client.send(send_len)  
    client.send(msg)

# Calculate public key
def get_public(Xb,q,a):
    return pow(a,Xb,q)

# Calculate private (random version)
# def get_private(q):
#     return random.randint(0,(q-1))

# Calculate private (input version)
def get_private(Q):
    flag=True
    while flag:
        clin=int(input(f"Enter Xb < {Q} \n"))
        if(clin<Q and clin>0):
            return clin
        else:
            print("Try again \n")

client.connect(ADDR)
q=client.recv(HEADER).decode(FORMAT)
q=int(q)
a=client.recv(HEADER).decode(FORMAT)
a=int(a)
print(f'q(mod)={q} and a(base){a}')
Xb=get_private(q)     
Yb=get_public(Xb,q,a)
print(f' USER B Public key {Yb} \n')
send(Yb)
Ya=client.recv(HEADER).decode(FORMAT)
Ya=int(Ya)
print(f' USER A Public key {Ya} \n')
R=client.recv(HEADER).decode(FORMAT)
R=int(R)
print(f' The Challenge R= {R} \n')
k=pow(Ya,Xb,q)
G=R*k
send(G)
print(f' The Reponse G= {G} \n')
send("close")
print(client.recv(HEADER).decode(FORMAT))