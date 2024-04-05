import subprocess

#Executing traceroute and tracepath and handling the errors
def traceroute_and_tracepath(address):
    address.insert(0, 'traceroute')
    form_command = address
    
    #using the subprocess module to execute tracroute
    try:
        output = subprocess.run(form_command, capture_output=True, text=True, check=True)
        print("\nThe traceroute result:\n")
        r = output.stdout
        print(r)
    except subprocess.CalledProcessError as error:
        print(f"Error occurred while executing traceroute: {error.stderr}")
    
    #modifying the command
    address.remove('traceroute')
    address.insert(0, 'tracepath')
    form_command = address
    
    #using subprocess module to execute tracepath
    try:
        output = subprocess.run(form_command, capture_output=True, text=True, check=True)
        print("\nThe tracepath result:\n")
        r = output.stdout
        print(r)
    except subprocess.CalledProcessError as error:
        print(f"Error executing traceroute: {error.stderr}")

def main():
    #Getting input from the user
    address = input("\nPlease enter the IP address or domain name:")
    splitting = address.split()
    traceroute_and_tracepath(splitting)

if __name__ == "__main__":
    main()
