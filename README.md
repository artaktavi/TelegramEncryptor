# TCrypto

TCrypto is a telegram bot that performs text encryption function. It will help you to _**secure important information**_ by encrypting messages or files. You need only Internet connection and valid [telegram](https://en.wikipedia.org/wiki/Telegram_(software)) account to use this bot.

Here are some features of this project:

- _**Encryption (and decryption)**_ of text with a few cyphers:
  - Caesar cipher
  - Vigener cipher
  - Vernam cipher
- _**Hacking**_ of Caesar cipher by frequency analysis method

TCrypto is completely _**safe**_ tool. It doesn't save personal data or user's messages text.



## Usage

If you're completely confused, just send `/help` message to bot, it will show you short info about TCrypto and it's usage.

Send `/start` message to interact with TCrypto. It will show you instruction. You should choose cipher you want to use after that.

To change cipher send `/cipher` message to bot, it should suggest options.

Now, when cipher is chosen, use:

- `/encrypt`
- `/decrypt`
- `/hack`

commands for encryption \ decryption \ hacking, after that send message with text \ file with text that you want to process. Bot will respond about correctness of your request. After that bot should send you result, sometimes it can take time, so just wait a bit...

Success! You got a encrypted \ decrypted \ hacked file or message, it depends on what did you send to bot (file or message) and chosen command.



## Architecture of project

To get more information about data encrypting core, read [FCrypto](docs/Encryptor.md) file.
