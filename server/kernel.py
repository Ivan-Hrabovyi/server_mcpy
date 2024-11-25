import requests
import subprocess
import time

#requests-module for requesting some information via http
#subprocess-module for activation of processes
#time-sleep time controller kinda timer

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()
# this block is used for pushing comand into bash terminal


def install_jdk():
    print("Installing JDK")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo","apt","upgrade"])
    subprocess.run(["sudo", "apt", "install", "tmux"])
    subprocess.run(["sudo", "apt", "install", "openjdk-17-jre-headless"])
    print("JDK installed")
    time.sleep(5)
    return
#install jdk(java developer kit)

def version_server_jar(project, minecraft_version):
    api_url = f"https://api.papermc.io/v2/projects/{project}/versions/{minecraft_version}/builds"
    response = requests.get(api_url)
    builds = response.json().get("builds", [])
    stable_builds = [build["build"] for build in builds if build["channel"] == "default"]
    return max(stable_builds, default=None)
#this block get info about server.jar route and return to system


def download_server_jar(project, minecraft_version):
    print("Installing server jar")
    latest_build = version_server_jar(project, minecraft_version)
    if latest_build is not None:
        jar_name = f"paper-{minecraft_version}-{latest_build}.jar"
        api_url = f"https://api.papermc.io/v2/projects/{project}/versions/{minecraft_version}/builds/{latest_build}/downloads/{jar_name}"
        subprocess.run(["curl", "-o", "server.jar", api_url])
        print("server.jar downloaded")
        time.sleep(5)
        return
    else:
        print("No stable builds found")
        main()
#this one actually get info form the previous one and push request for downloading  of server.jar        

def eula():
    print("Accepting EULA")
    with open("eula.txt", "w") as f:
        f.write("eula=true")
    print("EULA accepted")
    time.sleep(5)
    return
#create txt file with user agreement 

def install_ngrok():
    print("Installing ngrok...")
    run_command("curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null")
    run_command('echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list')
    run_command("sudo apt update && sudo apt install ngrok")
    print("Ngrok installed.")
    time.sleep(5)
    return
#install ngrok

def configure_ngrok(auth_token):
    print("Configuring ngrok with auth token...")
    run_command(f"ngrok config add-authtoken {auth_token}")
    print("Ngrok configured with auth token.")
    time.sleep(5)
    return
#update config with token

def start_server():
    subprocess.run(
        ["tmux", "new-session", "-d", "-s", "minecraft", "java", "-Xmx1024M", "-Xms512M", "-jar", "server.jar",
         "nogui"])
    print("Server is starting.")
    time.sleep(30)
    print("server started")
    time.sleep("5")
    return
#run start script

def start_ngrok():
    subprocess.run(["tmux", "new-session", "-d", "-s", "ngrok-session", "ngrok", "tcp", "25565"])
    print("Ngrok started.")
    time.sleep(5)
    return
#start ngrok for port for forwarding

def close_server_and_ngrok():
    print("Closing the server and ngrok...")
    run_command("sudo pkill ngrok")
    run_command("sudo pkill -9 java")
    print("Server and ngrok closed.")
    time.sleep(5)
    return
# shutdown all process
def main():
    while True:
        try:
            print("Welcome to the server installer")
            print("1. Install JDK(required for first time)")
            print("2. Install server jar(requierd for first time)")
            print("3. Accept EULA(user agreement)")
            print("4. Install ngrok(requiered for non local connection)")
            print("5. Configure ngrok")
            print("6.start server and ngrok")
            print("7.Close server and ngrok")
            print("8.exit")

            option = input("Enter your choice: ")

            if option == "1":
                install_jdk()

            elif option == "2":
                project = input("Enter the project name (e.g., paper): ")
                minecraft_version = input("Enter the Minecraft version (e.g., 1.18.2): ")
                download_server_jar(project, minecraft_version)

            elif option == "3":
                eula()

            elif option == "4":
                install_ngrok()

            elif option == "5":
                auth_token = input("Enter your ngrok auth token: ")
                configure_ngrok(auth_token)

            elif option == "6":
                start_server()
                start_ngrok()

            elif option == "7":
                close_server_and_ngrok()

            elif option =="8":
                exit   

            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
