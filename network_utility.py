import tkinter as tk
from tkinter import font, scrolledtext
import subprocess
import requests
from ftplib import FTP
import threading
import socket

def on_entry_click(event, entry_widget, default_text):
    current_text = entry_widget.get()
    if current_text == default_text:
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg='black') 

def on_focus_out(event, entry_widget, default_text):
    current_text = entry_widget.get()
    if not current_text:
        entry_widget.insert(0, default_text)
        entry_widget.config(fg='grey') 


#Output window for UDP server and client
def output_window2(output5):
    #Creating a window to display the command output
    output_window2 = tk.Toplevel(window)
    output_window2.title(f"Output for udp")
    output_window2.geometry("400x200")
            
    #making the window to have a scrolling feature
    output_text2 = scrolledtext.ScrolledText(output_window2, wrap=tk.WORD, width=40, height=20, font=bold_font)
    output_text2.pack(expand=True, fill='both')
    output_text2.insert(tk.END, output5)
            
    entry_widget.delete(0, tk.END)
            
    #This text appears after user chooses a command
    window_text.config(text="[WARNING!] Please check the opened window to view the full output.")
            
            
    #Back button
    back_button = tk.Button(output_window2, text="Back", command=output_window2.destroy, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.pack(pady=10)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
  
    
def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_ip = "127.0.0.1" #local IP address for server
    udp_port = 8080 #port number

    server.bind((udp_server_ip, udp_port))
    output5 = "UDP server is ready..."
    output_window2(output5)
    
    #receiving client server and sending a response
    try:
        while True:
            client_request, client_address = server.recvfrom(1024)
            client_request = client_request.decode("utf-8")

            if client_request.lower() == "finish":
                server.sendto("connection was closed".encode("utf-8"), client_address)
                break

            response = "The message was successfully accepted".encode("utf-8")
            server.sendto(response, client_address)
    except Exception as error:
        output5 = f"UDP server error: {error}" #handling errors
        output_window2(output5)
    finally:
        server.close()


def start_udp_client():
    #changing the association of the UDP button to the start_here2() button, so that it doesnt start the client multiple times
    udp_client_button.config(command=lambda: start_here2())
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    u_ip = "127.0.0.1" #local IP
    u_port = 8080 #port
    
    #getting message from the user and sending it to the server
    try:
        message = entry_widget.get()
        client.sendto(message.encode("utf-8")[:4096], (u_ip, u_port))

        response, _ = client.recvfrom(4096)
        response = response.decode("utf-8")
        output5 = f"Server's response: {response}"
        output_window2(output5)
            
        if response.lower() == "connection was closed":
            client.close()
    except Exception as error:
        output5 = f"UDP client error: {error}" 
        output_window2(output5)
        
    def start_here2():
        try:
            message = entry_widget.get()
            client.sendto(message.encode("utf-8")[:4096], (u_ip, u_port))

            response, _ = client.recvfrom(4096)
            response = response.decode("utf-8")
            output5 = f"Server's response: {response}"
            output_window2(output5)
            
            if response.lower() == "connection was closed":
                client.close()
            
        except Exception as error:
            output5 = f"UDP client error: {error}"
            output_window2(output5)

    
def udp_server():
    global udp_server_thread
    udp_server_thread = threading.Thread(target = start_udp_server)
    udp_server_thread.start()
    
def udp_client():
    start_udp_client()
    
    if "udp_server_thread" in locals():
        udp_server_thread.join()   

#output window for TCP connection
def output_window(output2):
    #Creating a window to display the command output
    output_window2 = tk.Toplevel(window)
    output_window2.title(f"Output for tcp")
    output_window2.geometry("400x200")
            
    #making the window to have a scrolling feature
    output_text2 = scrolledtext.ScrolledText(output_window2, wrap=tk.WORD, width=40, height=20, font=bold_font)
    output_text2.pack(expand=True, fill='both')
    output_text2.insert(tk.END, output2)
            
    entry_widget.delete(0, tk.END)
            
    #This text appears after user chooses a command
    window_text.config(text="[WARNING!] Please check the opened window to view the full output.")
            
            
    #Back button
    back_button = tk.Button(output_window2, text="Back", command=output_window2.destroy, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.pack(pady=10)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


def start_tcp_client():
    #changing the association of tcp client button to start_here()
    tcp_client_button.config(command=lambda: start_here())
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s_ip = "127.0.0.1"  #server IP
    s_port = 8080  #port
    tcp_client.connect((s_ip, s_port))
    
    #user enters message to the entry widget and client sends it to the server
    try:
        message = entry_widget.get()
        message = bytes(message, 'utf-8')
        tcp_client.send(message[:4096]) 

        server_response = tcp_client.recv(4096)
        server_response = server_response.decode("utf-8")
        if server_response.lower() == "connection was closed":
            tcp_client.close()

        output2=f"Server's response: {server_response}"
        output_window(output2)
    except Exception as error:
        output2 = f"Client error: {error}"
        output_window(output2)
        
    def start_here():
        try:
            message = entry_widget.get()
            message = bytes(message, 'utf-8')
            tcp_client.send(message[:4096]) 

            server_response = tcp_client.recv(4096)
            server_response = server_response.decode("utf-8")

            if server_response.lower() == "connection was closed":
                tcp_client.close()

            output2=f"Server's response: {server_response}"
            output_window(output2)
        except Exception as error: #error handling
            output2 = f"Client error: {error}"
            output_window(output2)
    
    return

def tcp_client():
    start_tcp_client()
    
    if "tcp_server_thread" in locals():
        tcp_server_thread.join()


def start_tcp_server():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ip = "127.0.0.1" #local IP
    tcp_port = 8080 #port number

    tcp_server.bind((tcp_ip, tcp_port))
    output4 = "Server is listening..."
    output_window(output4)
    tcp_server.listen(0)
    
    client_socket, addr = tcp_server.accept()
    

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
        output4 = f"Server error: {error}"
        output_window(output4)
    finally:
        client_socket.close()
        tcp_server.close()
    return


def tcp_server():
    #creating a thread for the server to run client and server simultaniously
    global tcp_server_thread
    tcp_server_thread = threading.Thread(target = start_tcp_server)
    tcp_server_thread.start()


def ftp_server(host_server, port_number, username, password):
    try:
        ftp = FTP()
        ftp.connect(host_server, port_number)
        ftp.login(username, password)
        return "You were successfully connected to the FTP server"
    except Exception as error:
        return f"Error occurred while connecting to the FTP server: {error}"
    finally:
        ftp.quit()

def ftp_connect(type):
    server = widget1.get()
    port = widget2.get()
    username = widget3.get()
    password = widget4.get()
    
    output3 = ftp_server(server, int(port), username, password)
    
    #Creating a window to display the command output
    output_window3 = tk.Toplevel(window)
    output_window3.title(f"Output for {type}")
    output_window3.geometry("400x200")
    
    #making the window to have a scrolling feature
    output_text3 = scrolledtext.ScrolledText(output_window3, wrap=tk.WORD, width=40, height=20, font=bold_font)
    output_text3.pack(expand=True, fill='both')
    output_text3.insert(tk.END, output3)
    
    widget1.delete(0, tk.END)
    widget2.delete(0, tk.END)
    widget3.delete(0, tk.END)
    widget4.delete(0, tk.END)
    
    #This text appears after user chooses a command
    window_text.config(text="[WARNING!] Please check the opened window to view the full output.")
    
    
    #Back button
    back_button = tk.Button(output_window3, text="Back", command=output_window3.destroy, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.pack(pady=10)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
 
    
#Sending GHTTP requests using the provided link and any other parameters
def http_request(link):
    try:
        output = requests.get(link)
        return f"Request status code: {output.status_code} \nRequest response: {output.text}"
    except requests.RequestException as error:
        return f"Something went wrong, ERROR: {error}"


def execute_http(request):
    link = entry_widget.get()
    
    output2 = http_request(link)
    
    #Creating a window to display the command output
    output_window2 = tk.Toplevel(window)
    output_window2.title(f"Output for {request}")
    output_window2.geometry("400x200")
    
    #making the window to have a scrolling feature
    output_text2 = scrolledtext.ScrolledText(output_window2, wrap=tk.WORD, width=40, height=20, font=bold_font)
    output_text2.pack(expand=True, fill='both')
    output_text2.insert(tk.END, output2)
    
    entry_widget.delete(0, tk.END)
    
    #This text appears after user chooses a command
    window_text.config(text="[WARNING!] Please check the opened window to view the full output.")
    
    
    #Back button
    back_button = tk.Button(output_window2, text="Back", command=output_window2.destroy, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.pack(pady=10)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    
    
#Executing nslookup, host, dig, traceroute and tracepath using subprocess module
def run_linux_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"


#Processing user input 
def execute_command(command_name):
    #Extracting the entered domain name or IP address
    domain_name = entry_widget.get()
    #Turning it into a list
    domain = domain_name.split()
    #Adding command type at the beginning of the list
    domain.insert(0, command_name)
    
    #Getting the command output
    output = run_linux_command(domain)
    
    #Creating a window to display the command output
    output_window = tk.Toplevel(window)
    output_window.title(f"Output for {command_name}")
    output_window.geometry("400x200")
    
    #making the window to have a scrolling feature
    output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=40, height=20, font=bold_font)
    output_text.pack(expand=True, fill='both')
    output_text.insert(tk.END, output)
    
    entry_widget.delete(0, tk.END)
    
    #This text appears after user chooses a command
    window_text.config(text="[WARNING!] Please check the opened window to view the full output.")
    
    
    #Back button
    back_button = tk.Button(output_window, text="Back", command=output_window.destroy, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.pack(pady=10)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    
def show_dns_commands():
    #hiding all buttons after pressing "DNS commands" button
    global back_button
    dns_button.place_forget()
    nt_button.place_forget()
    protocols_button.place_forget()
    tcp_button.place_forget()
    udp_button.place_forget()

    #The entry widget
    entry_widget.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    #Creating and placing three new buttons and adjusting their positions
    nslookup_button.place(relx=0.25, rely=0.2, anchor=tk.CENTER)
    host_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    dig_button.place(relx=0.75, rely=0.2, anchor=tk.CENTER)
    
    #Back button
    back_button = tk.Button(window, text="Back", command=show_main_page, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

def display_protocols():
    global back_button
    
    #Hiding all buttons
    nt_button.place_forget()
    dns_button.place_forget()
    protocols_button.place_forget()
    tcp_button.place_forget()
    udp_button.place_forget()

    entry_widget.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    
    widget1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    widget2.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
    widget3.place(relx=0.5, rely=0.54, anchor=tk.CENTER)
    widget4.place(relx=0.5, rely=0.61, anchor=tk.CENTER)

    #Creating and placing two new buttons and adjusting their positions
    http_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    ftp_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    
    #Back button
    back_button = tk.Button(window, text="Back", command=show_main_page, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.place(relx=0.8, rely=0.9, anchor=tk.CENTER)
    window_text.place(relx=0.45, rely=0.9, anchor=tk.CENTER)


def display_network_tracing():
    global back_button
    
    nt_button.place_forget()
    dns_button.place_forget()
    protocols_button.place_forget()
    tcp_button.place_forget()
    udp_button.place_forget()
    

    #Displaying the entry widget
    entry_widget.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    #Creating and placing two new buttons and adjusting their positions
    traceroute_button.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
    tracepath_button.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
    
    #Back button
    back_button = tk.Button(window, text="Back", command=show_main_page, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

def tcp_server_client():
    global back_button
    
    nt_button.place_forget()
    dns_button.place_forget()
    protocols_button.place_forget()
    tcp_button.place_forget()
    udp_button.place_forget()
    

    #Displaying the entry widget
    entry_widget.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    #Creating and placing two new buttons and adjusting their positions
    tcp_server_button.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
    tcp_client_button.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
    
    #Back button
    back_button = tk.Button(window, text="Back", command=show_main_page, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

def udp_server_client():
    global back_button
    
    nt_button.place_forget()
    dns_button.place_forget()
    protocols_button.place_forget()
    tcp_button.place_forget()
    udp_button.place_forget()
    

    #Displaying the entry widget
    entry_widget.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    #Creating and placing two new buttons and adjusting their positions
    udp_server_button.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
    udp_client_button.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
    
    #Back button
    back_button = tk.Button(window, text="Back", command=show_main_page, width=traceroute_button['width'], height=traceroute_button['height'], bg="Black", fg="white", font=bold_font)
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

def show_main_page():
    #Showing the buttons again
    dns_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    nt_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    protocols_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    tcp_button.place(relx=0.37, rely= 0.15, anchor =tk.CENTER)
    udp_button.place(relx=0.62, rely=0.15, anchor=tk.CENTER)

    #Hiding all other buttons
    entry_widget.place_forget()
    nslookup_button.place_forget()
    host_button.place_forget()
    dig_button.place_forget()
  
    
    traceroute_button.place_forget()
    tracepath_button.place_forget()
    
    http_button.place_forget()
    ftp_button.place_forget()
    
    tcp_server_button.place_forget()
    tcp_client_button.place_forget()
    
    udp_server_button.place_forget()
    udp_client_button.place_forget()
    
    widget2.place_forget()
    widget1.place_forget()
    widget3.place_forget()
    widget4.place_forget()
    

    #Destroying the "back" button and previous text
    back_button.destroy() 
    
    window_text.config(text="Command results will appear as a separate window")
    window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

def adjust_button_sizes(event):
    # Adjust button sizes based on the window size
    window_width = event.width
    window_height = event.height

    # Calculate adjusted button sizes
    adjusted_button_width = max(30, min(40, int(window_width / 15)))
    adjusted_button_height = max(3, min(4, int(window_height / 100)))

    # Configure buttons with adjusted sizes
    dns_button.config(width=adjusted_button_width, height=adjusted_button_height)
    nt_button.config(width=adjusted_button_width, height=adjusted_button_height)
    protocols_button.config(width=adjusted_button_width, height=adjusted_button_height)
    tcp_button.config(width=adjusted_button_width - 10, height=adjusted_button_height)
    udp_button.config(width=adjusted_button_width - 10, height=adjusted_button_height)
    
    nslookup_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    host_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    dig_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    
    traceroute_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    tracepath_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    
    http_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    ftp_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    
    tcp_server_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    tcp_client_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    
    udp_server_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    udp_client_button.config(width=adjusted_button_width - 10, height=adjusted_button_height - 1)
    

#Creating the main window and adjusting its initial size
window = tk.Tk()
window.title("GUI for lab assignment 1")
window.geometry("1300x700")

#Choosing the color of the window -> purple
dark_purple = "#4B0082"
window.configure(bg=dark_purple)

#Designing the text
bold_font = font.Font(family="Rod", size=14, weight="bold")

#Choosing the initial size of buttons 
initial_button_width = 40
initial_button_height = 4

#Creating main page buttons
dns_button = tk.Button(window, text="DNS Commands", command=show_dns_commands, width=initial_button_width, height=initial_button_height, bg=dark_purple, fg="white", font=bold_font)
nt_button = tk.Button(window, text="Network Tracing", command=display_network_tracing, width=initial_button_width, height=initial_button_height, bg=dark_purple, fg="white", font=bold_font)
protocols_button = tk.Button(window, text="Protocols", command=display_protocols, width=initial_button_width, height=initial_button_height, bg=dark_purple, fg="white", font=bold_font)
tcp_button = tk.Button(window, text="TCP", command=tcp_server_client, width=initial_button_width, height=initial_button_height, bg=dark_purple, fg="white", font=bold_font)
udp_button = tk.Button(window, text="UDP", command=udp_server_client, width=initial_button_width, height=initial_button_height, bg=dark_purple, fg="white", font=bold_font)

#Calling corresponding functions
nslookup_button = tk.Button(window, text="nslookup", command=lambda: execute_command("nslookup"), bg=dark_purple, fg="white", font=bold_font)
host_button = tk.Button(window, text="host", command=lambda: execute_command("host"), bg=dark_purple, fg="white", font=bold_font)
dig_button = tk.Button(window, text="dig", command=lambda: execute_command("dig"), bg=dark_purple, fg="white", font=bold_font)

traceroute_button = tk.Button(window, text="traceroute", command=lambda: execute_command("traceroute"), bg=dark_purple, fg="white", font=bold_font)
tracepath_button = tk.Button(window, text="tracepath", command=lambda: execute_command("tracepath"), bg=dark_purple, fg="white", font=bold_font)

http_button = tk.Button(window, text="HTTP", command=lambda: execute_http("HTTP"), bg=dark_purple, fg="white", font=bold_font)
ftp_button = tk.Button(window, text="FTP", command=lambda: ftp_connect("FTP"), bg=dark_purple, fg="white", font=bold_font)

tcp_server_button = tk.Button(window, text="TCP server", command=lambda: tcp_server(), bg=dark_purple, fg="white", font=bold_font)
tcp_client_button = tk.Button(window, text="TCP client", command=lambda: tcp_client(), bg=dark_purple, fg="white", font=bold_font)

udp_server_button = tk.Button(window, text="UDP server", command=lambda: udp_server(), bg=dark_purple, fg="white", font=bold_font)
udp_client_button = tk.Button(window, text="UDP client", command=lambda: udp_client(), bg=dark_purple, fg="white", font=bold_font)

#Input box for the user to enter domains etc
entry_widget = tk.Entry(window, width=30, font=bold_font)


default_text_widget1 = "Enter host server"
default_text_widget2 = "Enter port number"
default_text_widget3 = "Enter username"
default_text_widget4 = "Enter password"

widget1 = tk.Entry(window, width=20, font=bold_font, fg='grey')
widget1.insert(0, default_text_widget1)
widget1.bind('<FocusIn>', lambda event: on_entry_click(event, widget1, default_text_widget1))
widget1.bind('<FocusOut>', lambda event: on_focus_out(event, widget1, default_text_widget1))

widget2 = tk.Entry(window, width=20, font=bold_font, fg='grey')
widget2.insert(0, default_text_widget2)
widget2.bind('<FocusIn>', lambda event: on_entry_click(event, widget2, default_text_widget2))
widget2.bind('<FocusOut>', lambda event: on_focus_out(event, widget2, default_text_widget2))

widget3 = tk.Entry(window, width=20, font=bold_font, fg='grey')
widget3.insert(0, default_text_widget3)
widget3.bind('<FocusIn>', lambda event: on_entry_click(event, widget3, default_text_widget3))
widget3.bind('<FocusOut>', lambda event: on_focus_out(event, widget3, default_text_widget3))

widget4 = tk.Entry(window, width=20, font=bold_font, fg='grey')
widget4.insert(0, default_text_widget4)
widget4.bind('<FocusIn>', lambda event: on_entry_click(event, widget4, default_text_widget4))
widget4.bind('<FocusOut>', lambda event: on_focus_out(event, widget4, default_text_widget4))


#Labeling to display text
window_text = tk.Label(window, text="Command results will appear as a separate window", bg=dark_purple, fg="white", font=bold_font)
window_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

#Initial button positions
dns_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
nt_button.place(relx=0.5, rely= 0.45, anchor =tk.CENTER)
protocols_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
tcp_button.place(relx=0.37, rely= 0.15, anchor =tk.CENTER)
udp_button.place(relx=0.62, rely=0.15, anchor=tk.CENTER)

#Binding adjust_button_sizes function to the Configure event of the window
window.bind("<Configure>", adjust_button_sizes)

window.mainloop()
