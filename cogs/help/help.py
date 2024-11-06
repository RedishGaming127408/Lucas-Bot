
#Help command
import discord
from discord.ext import commands



class  Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command(name='help', description='Displays a list of available commands.')
    async def help_command(self, ctx):
        embed = discord.Embed(title="Help Menu", description="Here are the commands you can use:", color=discord.Color.blue())
        
        embed.add_field(name="**Moderation**", value="l!kick <user> [reason] - Kicks a user from the server.\nl!ban <user> [reason] - Bans a user from the server.\nl!unban <user_id> - Unbans a user from the server.\nl!mute <user> [reason] - Mutes a user in the server.\nl!unmute <user> - Unmutes a user in the server.\nl!warn <user> [reason] - Warns a user in the server.\nl!clear <amount> - Clears a specified amount of messages.\nl!tempban <user> <duration> [reason] - Temporarily bans a user for a specified duration.\nl!tempmute <user> <duration> [reason] - Temporarily mutes a user for a specified duration.\nl!userinfo - Displays information about a user.\nl!add_bad_words - Adds a bad word to the list of bad words.\nl!remove_bad_words - Removes a bad word from the list of bad words.\nl!list_bad_words - Lists all the bad words in the list of bad words.", inline=False)
        embed.add_field(name="**Information**", value="l!rules -  Rules on the server.\nl!bot_dev - Returns the bot developer's name.\nl!member_count - Gets the member count on this server.\nl!invite_link - Gives your invite link for the server.\nl!info - Displays information about the server.", inline=False)
        embed.add_field(name="**Miscellaneous**", value="l!bible - Returns a random Bible verse.\nl!ping - Shows the ping or bot latency.\nl!sudo <text> - Bot responds with the same text as you typed.\nl!roll - Rolls a dice and returns a random number between 1 and 6.\nl!avatar - Displays the avatar of a user.\nl!joke - Tells a random joke.\nl!meme - Displays a random meme.\nl!random_fact - Returns a random fact.\nl!quote - Returns a random quote.\nl!poll - Creates a poll.\nl!8ball - Ask the magic 8ball a question.", inline=False)
        
        embed.set_footer(text="Above are the provided commands")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))