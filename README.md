# Discord GitHub Stats Bot

This Discord bot provides commands to retrieve GitHub statistics and information for a specified user. It utilizes slash commands for ease of use and includes features such as displaying account information, repository details, top languages, and more.

## Features
- **/git command**: Retrieves and displays GitHub statistics for a specified user, including account information, repositories, followers, following, and more.
- **/repos command**: Lists the repositories of a GitHub user with pagination support, including repository name, description, language, and privacy status.

## Installation
1. Clone this repository: `git clone https://github.com/your-username/discord-github-stats-bot.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your Discord bot and obtain the token.
4. Replace `'YOUR_TOKEN_HERE'` in the code with your Discord bot token.
5. Run the bot: `python bot.py`

## Usage
1. Invite the bot to your Discord server using the OAuth2 URL.
2. Use the `/git` command followed by the GitHub username to retrieve their statistics.
3. Use the `/repos` command followed by the GitHub username to list their repositories.

## Example
- `/git username`: Retrieves GitHub statistics for the specified user.
- `/repos username page`: Lists the repositories of the specified user, with pagination support.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- This bot is built using the `discord.py` library.
- GitHub API is used to retrieve GitHub statistics.

Feel free to contribute to this project by submitting pull requests or opening issues. Enjoy!
