# Discord-Gatekeeper
![Discord People Online](https://img.shields.io/discord/530810422345859082) https://discord.gg/jbameAa5mf   
![Docker Build Status](https://img.shields.io/docker/cloud/build/slamanna212/discordgatekeeper) ![Docker Automated Status](https://img.shields.io/docker/cloud/automated/slamanna212/discordgatekeeper)   
![Github open issues](https://img.shields.io/github/issues/slamanna212/discord-gatekeeper) ![Github activity](https://img.shields.io/github/last-commit/slamanna212/discord-gatekeeper) ![Github top language](https://img.shields.io/github/languages/top/slamanna212/discord-gatekeeper)

# About
Discord bot written in python. Used for the r/Oilpen discord but can be used by others by modifying the settings.json file to fit your needs. 

PMs user on join with whatever message you set and a unique code, user must enter the unique code into a specified channel and they receive a discord role. Used to verify new users have read our rules and prove they are a human. 

# Running
We run ours in docker , but for most people it would be easier just running the code on your console. I am not an expert on docker, their could be an eaiser way to do this that I do not know about, feel free to submit a PR and I will change it.

## Console
1. Fork the repository
2. Open settings.json in your editor of choice and change the contents of "one", "two", and "three" to fit your needs
3. Clone the repository onto the machine you will be running the bot on
```
git clone https://github.com/YOURGITHUBUSERNAME/Discord-Gatekeeper/
```
4. Install python requirements
```
pip3 install -r requirements.txt
```
5. Edit settings.json and replace Token, Role, and Channel with your values. Role is the role it gives the user and channel is the channel it looks in for the commands to be put in. To find these ids turn on dev mode in discord and then right click the channel and role and click copy ID
6. Run the following command to run the bot
```
python3 bot.py
```
7. To make it run in the background use screen , and create a startup script in your distros preferred method.

## Docker
1. Do Steps 1 and 2 from above.
2. Create a new repo on [Docker Hub](https://hub.docker.com/) 
3. Name it discordgatekeeper
3. Connect it to Github and select your Discord Gatekeeper repo on github
4. Click Create and Build
5. Take note of the text next to the globe. That is your dockerhub username and the repo name on dockerhub you will need this later
6. On your docker host, run the following command
```
docker run -d \
  --name=DiscordGatekeeper \
  -e TOKEN='DISCORDBOTTOKEN' \
  -e ROLE='ROLEID' \
  -e CHANNEL='CHANNELID' \
  --restart unless-stopped \
YOURDOCKERHUBACCOUNTNAME/discordgatekeeper
```
7. If you want to verify its working, just check the logs for the container

# Credits
Initial code from [sourovafrin](https://www.fiverr.com/sourovafrin) on Fivrr
Assits from discord members on r/Oilpen


