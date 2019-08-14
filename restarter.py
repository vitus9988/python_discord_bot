import subprocess


def pid_detect(process):
    result = subprocess.check_output("ps -ef | grep -i " + process + " | grep -v 'grep' | awk {'print $2'}", shell=True, encoding='utf-8')
    if result == '':
        subprocess.run(['nohup python /home/vitus9988/workspace/discord_bot/new_discord_bot.py &'], shell=True)
        subprocess.run(['date'], shell=True)
    else:
        pass


if __name__ == '__main__':
    pid_detect('new_discord_bot.py')