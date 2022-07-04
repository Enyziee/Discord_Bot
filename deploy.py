import os

TOKEN = ""
BUILD_DOCKER = "sudo docker build . -t discord_bot"
RUN_DOCKER = f"sudo docker run -d -e TOKEN=<TOKEN> --restart always --name bot discord_bot"
RM_CONTAINER = "sudo docker rm bot"
STOP_CONTAINER = "sudo docker stop bot"
PULL = "sudo git pull"

if TOKEN:
    print("\nProcurando uma nova versão!")
    os.system(PULL)
    print("\nIniciando Build do container:")
    os.system(BUILD_DOCKER)
    print("Build Finalizada!")
    print("\nParando Container desatualizado!")
    os.system(STOP_CONTAINER)
    print("\Removendo Container desatualizado!")
    os.system(RM_CONTAINER)
    print("\nIniciando Container atualizado!")
    os.system(RUN_DOCKER)
    os.system("sudo docker ps")

else:
    print("Sem Token definido")
