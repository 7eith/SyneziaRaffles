# 🚀 SyneziaRaffles
> An open source raffle bot made to increase the chance of winning limited sneaker raffles by automating entries.

![Synezia](https://github.com/iSnkh/SyneziaRaffles/blob/master/resources/Synezia_MainMenu.png?raw=true)


# 🏄‍♂️ Quick Start

Prerequisites: [Python 3 + PIP](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads)

> clone/fork SyneziaRaffles

```bash
git clone https://github.com/iSnkh/SyneziaRaffles
```

> install and start SyneziaRaffles

```bash
cd SyneziaRaffle
pip3 install -r requirements.txt
python srcs/run.py
```

# 📚 Links

- [Website](https://synezia.com)
- [Download](https://cdn.discordapp.com/attachments/827984372736983090/940232734243164220/SyneziaRaffle.exe)
- [Guide](https://synezia.gitbook.io/syneziasoft/)
- [Twitter](https://twitter.com/SyneziaSoft)
- [Discord](https://discord.gg/hRxp4Ka8xF)

# 🛠 Build
You need to install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) & [PyArmor](https://github.com/dashingsoft/pyarmor) before

```bash
# PYFIGLET PATH: path to pyfiglet directory
# RANDOM UA PATH: path to random user agent directory
# ICO PATH: path to your logo in .ico
# NAME: name of the executable 

pyarmor pack --clean -e '--onefile --hidden-import pyfiglet --add-data {PYFIGLET PATH} --add-data {RANDOM UA PATH} --icon {ICO PATH}' srcs/main.py --name {NAME}
```

An example, i use that to compile the Client.
The folder *libs* contains source code of random_user_agent and pyfiglet 
```bash
pyarmor pack --clean -e '--onefile --hidden-import pyfiglet --add-data "./libs/pyfiglet;./pyfiglet" --add-data "./libs/random_user_agent;./random_user_agent" --icon icon.ico' srcs/main.py --name SyneziaRaffle
```

# 💌 P.S.

SyneziaRaffles was a free software in beta that helped to checkout more than 1000+ pairs. The best modules was FootLocker App, TheBrokenArm and NakedCPH.

The code is really bad, i have started to learn Python in December 2020 and i have release Synezia the 4 February 2021. 

I release it now, because when i started to make my own Sneakers Bot i haven't found how to do it like how to compile exe, how to deal with requests. The code is really outdated, i advice you to not use it but take a look to learn. It missing some stuffs like Server (License System) and Monitors

For any commercial purpose feel free to reach me using [Twitter](https://twitter.com/7eith_), by email at seith@synezia.com or using discord seith#0001