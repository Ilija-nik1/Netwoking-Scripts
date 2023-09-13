import os
import paramiko
import concurrent.futures

# Function to log in to a MikroTik router, export config, and download it
def process_router(ip, username, password, output_dir):
    try:
        # Establish an SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Run the export command
        ssh.exec_command("/export file=config")

        # Wait for a moment to ensure the export is complete
        import time
        time.sleep(5)

        # Download the config file
        scp = ssh.open_sftp()
        remote_filename = "/config.rsc"
        local_filename = os.path.join(output_dir, f"{ip}.rsc")
        scp.get(remote_filename, local_filename)
        scp.close()

        # Close the SSH connection
        ssh.close()
        print(f"Successfully downloaded config for {ip}")
    except Exception as e:
        print(f"Error processing {ip}: {str(e)}")

# Read Winbox addresses from the 'addresses.cib' file
with open('addresses.cib', 'r') as file:
    lines = file.readlines()

addresses = [line.strip() for line in lines]

# Set your SSH username and password
username = 'your_username'
password = 'your_password'

# Set the directory where you want to save the config files
output_directory = 'downloads'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Use concurrent.futures for multithreading
with concurrent.futures.ThreadPoolExecutor() as executor:
    for address in addresses:
        executor.submit(process_router, address, username, password, output_directory)