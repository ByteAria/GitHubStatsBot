import discord
from discord.ext import commands
import requests
import datetime

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
TOKEN = 'YOUR_TOKEN_HERE'

@bot.slash_command()
async def git(ctx, username: str):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        created_at = datetime.datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
        updated_at = datetime.datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")

        embed = discord.Embed(title=data['login'], description=data.get('bio', 'No bio provided'), color=0xFFD700)
        embed.set_thumbnail(url=data['avatar_url'])
        embed.add_field(name="Account Information", value=f"• **Name** : {data['name']}\n"
                                                          f"• **Creation** : `{created_at}`\n"
                                                          f"• **Updated** : `{updated_at}`\n"
                                                          f"• **Location** : {data.get('location', 'Unknown')}\n"
                                                          f"• **Hireable** : {data['hireable']}\n\n"
                                                          f"• **Repositories** : {data['public_repos']}\n"
                                                          f"• **Gists** : {data['public_gists']}\n\n"
                                                          f"• **Followers** : {data['followers']}\n"
                                                          f"• **Following** : {data['following']}", inline=False)

        embed.add_field(name="GitHub Streak Stats", value=f"[View Streak Stats](https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=vue-dark&hide_border=true)", inline=False)
        embed.add_field(name="Top Languages Stats", value=f"[View Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&theme=vue-dark&show_icons=true&hide_border=true&layout=compact)", inline=False)

        if data.get('twitter_username'):
            embed.add_field(name="Twitter",value=f"[{data['twitter_username']}](https://twitter.com/{data['twitter_username']})", inline=False)
        if data.get('blog'):
            embed.add_field(name="Blog", value=f"[{data['blog']}](https://{data['blog']})", inline=False)

        embed.set_footer(text="GitHub Profile", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.url = f"https://github.com/{username}"

        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found.")

@bot.slash_command()
async def repos(ctx, username: str, page: int = 1):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()

        def create_embed(page):
            embed = discord.Embed(title=f"{username}'s Repositories", color=0x7289da)
            start_idx = (page - 1) * 5
            end_idx = min(start_idx + 5, len(repos))

            for i in range(start_idx, end_idx):
                repo = repos[i]
                description = repo['description'] or "No description"
                language = repo['language'] or "Unknown"
                embed.add_field(name=f"{i + 1} {repo['name']}", value=f"{description}\n• {language} - {'Private' if repo['private'] else 'Public'}", inline=False)

            embed.set_footer(text=f"Page {page}/{(len(repos) // 5) + 1} • {len(repos)} repositories")
            return embed

        message = await ctx.send(embed=create_embed(page))
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check)
                await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "➡️" and page < (len(repos) // 5) + 1:
                    page += 1
                    await message.edit(embed=create_embed(page))
                elif str(reaction.emoji) == "⬅️" and page > 1:
                    page -= 1
                    await message.edit(embed=create_embed(page))
            except asyncio.TimeoutError:
                break
    else:
        await ctx.send("User not found or has no public repositories.")

bot.run(TOKEN)
