import subprocess
import requests
from ftplib import FTP
import socket
import threading


#TASK4
def start_udp_server():
    #creating a socket object for UDP connection
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_ip = "127.0.0.1"
    udp_port = 8080

    #binding to server IP and port
    server.bind((udp_server_ip, udp_port))
    
    try:
        #continiously receiving messages from the client
        while True:
            client_request, client_address = server.recvfrom(1024)
            client_request = client_request.decode("utf-8")

            #if client's message is "finish", connection closes
            if client_request.lower() == "finish":
                server.sendto("connection was closed".encode("utf-8"), client_address)
                break

            response = "The message was successfully accepted".encode("utf-8")
            server.sendto(response, client_address)
    except Exception as error:
        print(f"UDP server error: {error}")
    finally:
        server.close()



def start_udp_client():
    #creating udp specific client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u_ip = "127.0.0.1"  #server IP
    u_port = 8080 #server port
    
    try:
        while True:
            #user enters their message
            message = input("Please enter your message: ")
            client.sendto(message.encode("utf-8")[:4096], (u_ip, u_port))

            response, _ = client.recvfrom(4096)
            response = response.decode("utf-8")
            #printing out server's response
            print(f"Server's response: {response}")
            
            #loop breaks if server confirms connection closure
            if response.lower() == "connection was closed":
                break

            
    except Exception as error:
        print(f"UDP client error: {error}")
    finally:
        client.close()


def start_tcp_client():
    #initializing TCP specific client object
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s_ip = "127.0.0.1"  #server local IP
    s_port = 8080  #port
    tcp_client.connect((s_ip, s_port))
    try:
        while True:
            #asking the user for input message and encoding it to send to the server
            message = input("Please enter your message:\n")
            message = bytes(message, 'utf-8')
            tcp_client.send(message[:4096]) 

            server_response = tcp_client.recv(4096)
            server_response = server_response.decode("utf-8")

            if server_response.lower() == "connection was closed":
                break
            #getting response from the server and printing it out
            print("Server's response:", server_response)
    except Exception as error:
        print(f"Client error: {error}")
    finally:
        tcp_client.close()


def start_tcp_server():
    #TCP server object
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ip = "127.0.0.1" #local IP address
    tcp_port = 8080 #port number

    tcp_server.bind((tcp_ip, tcp_port))
    #listening for client connection
    tcp_server.listen(0)
    
    client_socket, addr = tcp_server.accept()
    print(f"Server accepted connection from {addr[0]}:{addr[1]}") 

    #receiving data from the client side
    try:
        while True:
            conn = client_socket.recv(4096)
            conn = conn.decode('utf-8')
            
            if conn.lower() == "finish":
                r = 'connection was closed'
                r = bytes(r, 'utf-8')
                client_socket.send(r)
                break

            form_response = "Message was successfully accepted"
            form_response = bytes(form_response, 'utf-8')
            client_socket.send(form_response)
    except Exception as error:
        print(f"Server error: {error}")
    client_socket.close()
    tcp_server.close()


#TASK1
#this function can handle nslookup host and dig commands with arguments
def execute_dns_commands(command_type):
    try:
        output = subprocess.run(command_type, capture_output = True, text=True, check=True)
        r = output.stdout
        print("\nDisplaying the results of the command execution:\n", r)
    except subprocess.CalledProcessError as error:
        print(f"Something wrong happened when executing the command: {error}")


#TASK2
#Sending GHTTP requests using the provided link and any other parameters
def http_request(link, headers=None, params=None):
    try:
        output = requests.get(link, headers=headers, params=params)
        print(f"Request status code: {output.status_code} \nRequest response: {output.text}")
    except requests.RequestException as error:
        print(f"Something went wrong, ERROR: {error}")

#Connecting to the FTP server
def ftp_connect(host_server, port_number, username, password):
    try:
        ftp = FTP()
        ftp.connect(host_server, port_number)
        ftp.login(username, password)
        print("You were successfully connected to the FTP server")
    except Exception as error:
        print(f"Error occurred while connecting to the FTP server: {error}")
    finally:
        ftp.quit()


def main():
    domain_name = input("\nPlease enter domain name:")
    command_arguments = input("\nPlease enter the dns command (nslookup, host, dig) along with any related arguments e.g 'nslookup -type=soa':")
    form_command = command_arguments.split()
    form_command.insert(len(form_command), domain_name)

    execute_dns_commands(form_command)
    
    protocol_type = input("Please choose the protocol (HTTP or FTP): ").upper()

    if protocol_type == "HTTP":
        link = input("Please paste your url: ")
        headers = input("Enter headers, if any: ")
        headers = dict(tuple(header.split(':')) for header in headers.split(',')) if headers else None
        params = input("Enter query parameters, if any: ")
        params = dict(tuple(param.split(':')) for param in params.split(',')) if params else None
        http_request(link, headers=headers, params=params)
        
    elif protocol_type == "FTP":
        server = input("Enter the FTP server address: ")
        port = int(input("Enter the FTP port: "))
        username = input("Enter the FTP username: ")
        password = input("Enter the FTP password: ")
        
        ftp_connect(server, port, username, password)
    else:
        print("You entered invalid input")
        
    user_choice = input("Would you like to run the TCP server? (Y/N):")
    if user_choice == 'Y':
        tcp_server_thread = threading.Thread(target = start_tcp_server)
        tcp_server_thread.start()
        user_choice = input("Would you like to run the TCP client? (Y/N):")
    
        if user_choice == 'Y':
            start_tcp_client()
        else:
            print("What a pity...")
    
        if "tcp_server_thread" in locals():
            tcp_server_thread.join()
    else:
        print("Client can not be run before the server...")
        

    user_choice = input("Would you like to run the UDP server? (Y/N):")
    if user_choice == 'Y':
        udp_server_thread = threading.Thread(target = start_udp_server)
        udp_server_thread.start()
        user_choice = input("Would you like to run the UDP client? (Y/N):")
    
        if user_choice == 'Y':
            start_udp_client()
        else:
            print("What a pity...")
    
        if "upd_server_thread" in locals():
            udp_server_thread.join()
        
    else:
        print("Client can not be run before the UDP server...")
        

if __name__ == "__main__":
    main()
