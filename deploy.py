import os

TOKEN = ""
BUILD_DOCKER = "docker build . -t discord_bot"
RUN_DOCKER = f"docker run -d -e TOKEN={TOKEN} --restart always --name bot discord_bot"
RM_CONTAINER = "docker rm bot"
STOP_CONTAINER = "docker stop bot"
PULL = "git pull"

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

    os.system("docker ps")

print("Sem Token definido")