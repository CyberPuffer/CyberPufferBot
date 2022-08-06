# Cyber Puffer - 赛博河豚🐡

## Quick deploy:

First create a channel and add the bot to the channel, 

Then post the following settings, and pin that message.

```
enabled_modules = "uptime, keyword, luck, weibo"

# keyword reply example
[[keywords]]
keyword = "foo"
type = "plaintext"
text = "bar"
```

And now we can deploy the bot using *docker-compose*

`docker-compose.yml`
```
version: "2.4"
services:
  cyberpuffer:
    image: pufferoverflow/cyberpuffer:latest
    restart: always
    environment:
      API_SECRET: telegram:TELEGRAM_API_TOKEN:CONFIG_CHANNEL_ID
    read_only: true
    ipc: none
    mem_limit: 64M
    memswap_limit: 64M
    network_mode: bridge
```
Replace `TELEGRAM_API_TOKEN` and `CONFIG_CHANNEL_ID` with your own

## Commands:

 - `/uptime`        Reply with bot uptime
 - `/luck`          Get today's luck level
 - `/weibo [num]`   Get Weibo's Trending list (Get top 10 by default)

## Functions:

 - Reply to keywords with text, sticker or forwarded message

## Add your own functions

First make a directory with your mod name and place your program under `/modules/`

The entrance file name should be the same with directory name.

Then the bot will call the function with the same name with 2 arguments `message` and `sender` and expect the same return.

Example: `/modules/hello/hello.py`
```
def hello(message: str, sender: dict):
    reply = "Hello World!"
    receiver = sender
    return reply, receiver
```

Finally add your module name to the `enabled_modules` section in the config message and restart the bot. The bot should automatically load your function and register the corresponding command.