#/bin/bash

#📦
sudo apt-get install python3 pip
python3 -m pip install cryptography Django getpass4 selenium termcolor

#🦪
sudo mv ./senhasegura.sh /bin
sudo chmod 755 /bin/senhasegura.sh
sudo mv /bin/senhasegura.sh /bin/senhasegura

#🦎
mkdir ~/.senhasegura
mv App core static db.sqlite3 manage.py start.py ~/.senhasegura/

clear
echo "Instalado com sucesso."
