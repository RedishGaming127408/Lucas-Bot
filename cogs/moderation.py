import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_users = {}

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="Kick", description=f'Kicked {member.mention} for: {reason}', color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Ban", description=f'Banned {member.mention} for: {reason}', color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title="Unban", description=f'Unbanned {user.mention}', color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(title="Error", description=f'User  {member} not found in ban list.', color=0xFF0000)
        await ctx.send(embed=embed)

    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(role, reason=reason)
        self.muted_users[member.id] = role
        embed = discord.Embed(title="Mute", description=f'Muted {member.mention} for: {reason}', color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(title="Unmute", description=f'Unmuted {member.mention}', color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f'{member.mention} is not muted.', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='warn')
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title="Warning", description=f'Warning {member.mention} for: {reason}', color=discord.Color.blue())
        await ctx.send(embed=embed)
    # Temp ban
    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: int, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Ban", description=f"Banned {member.mention} for {duration} days for: {reason}", color=discord.Color.blue())
        await ctx.send(embed=embed)
        await asyncio.sleep(duration * 86400)  # 86400 seconds in a day
        await member.unban(reason='Temp ban duration expired')
        embed = discord.Embed(title="Unban", description=f"Unbanned {member.mention}", color=discord.Color.blue())
        await ctx.send(embed=embed)
        
    # temp mute
    @commands.command(name='tempmute')
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if role in member.roles:
            embed = discord.Embed(title="Error", description=f"{member.mention} is already muted.", color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role, reason=reason)
            self.muted_users[member.id] = role
            embed = discord.Embed(title="Mute", description=f"Muted {member.mention} for {duration} days for: {reason}", color=discord.Color.blue())
            await ctx.send(embed=embed)
            await asyncio.sleep(duration * 86400)  # 86400 seconds in a day
            await member.remove_roles(role, reason='Temp mute duration expired')
            embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", color=discord.Color.blue())
            await ctx.send(embed=embed)
            del self.muted_users[member.id]
        
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Clear", description=f'Cleared {amount} messages.', color=discord.Color.blue())
        await ctx.send(embed=embed)
        await ctx.message.delete()

    #### AUTO MODERATION ####
    
    
    bad_words = ["asshole", "bitch", "cock", "cunt", "damn", "dick", "fuck", "fucker", "fucking", "hell", "motherfucker", "nigger", "nigga", "piss", "pussy", "shit", "shitty", "son of a bitch",
             "asshole!", "bitch!", "cock!", "cunt!", "damn!", "dick!", "fuck!", "fucker!", "fucking!", "hell!", "motherfucker!", "nigger!", "nigga!", "piss!", "pussy!", "shit!", "shitty!", "son of a bitch!",
             "ASSHOLE", "BITCH", "COCK", "CUNT", "DAMN", "DICK", "FUCK", "FUCKER", "FUCKING", "HELL", "MOTHERFUCKER", "NIGGER", "NIGGA", "PISS", "PUSSY", "SHIT", "SHITTY", "SON OF A BITCH",
             "ASSHOLE!", "BITCH!", "COCK!", "CUNT!", "DAMN!", "DICK!", "FUCK!", "FUCKER!", "FUCKING!", "HELL!", "MOTHERFUCKER!", "NIGGER!", "NIGGA!", "PISS!", "PUSSY!", "SHIT!", "SHITTY!", "SON OF A BITCH!",
             "ASSHOLE.", "BITCH.", "COCK.", "CUNT.", "DAMN.", "DICK.", "FUCK.", "FUCKER.", "FUCKING.", "HELL.", "MOTHERFUCKER.", "NIGGER.", "NIGGA.", "PISS.", "PUSSY.", "SHIT.", "SHITTY.", "SON OF A BITCH.",
             "ASSHOLE?", "BITCH?", "COCK?", "CUNT?", "DAMN?", "DICK?", "FUCK?", "FUCKER?", "FUCKING?", "HELL?", "MOTHERFUCKER?", "NIGGER?", "NIGGA?", "PISS?", "PUSSY?", "SHIT?", "SHITTY?", "SON OF A BITCH?",
             "ASSHOLE.", "BITCH.", "COCK.", "CUNT.", "DAMN.", "DICK.", "FUCK.", "FUCKER.", "FUCKING.", "HELL.", "MOTHERFUCKER.", "NIGGER.", "NIGGA.", "PISS.", "PUSSY.", "SHIT.", "SHITTY.", "SON OF A BITCH.",
             "ASSHOLE!", "BITCH!", "COCK!", "CUNT!", "DAMN!", "DICK!", "FUCK!", "FUCKER!", "FUCKING!", "HELL!", "MOTHERFUCKER!", "NIGGER!", "NIGGA!", "PISS!", "PUSSY!", "SHIT!", "SHITTY!", "SON OF A BITCH!",
             "ASSHOLE?", "BITCH?", "COCK?", "CUNT?", "DAMN?", "DICK?", "FUCK?", "FUCKER?", "FUCKING?", "HELL?", "MOTHERFUCKER?", "NIGGER?", "NIGGA?", "PISS?", "PUSSY?", "SHIT?", "SHITTY?", "SON OF A BITCH?",]
   
    # moderation
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.lower() in self.bad_words:
            await message.delete()
            embed = discord.Embed(title="Auto Moderation", description=f'Automatically deleted message from {message.author.mention} for saying a bad word.', color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await message.channel.purge(limit=1, check=lambda m: m.author == self.bot.user)

            
    # add bad word
    @commands.command(name='add_bad_word')
    @commands.has_permissions(manage_messages=True)
    async def add_bad_word(self, ctx, *, word):
        self.bad_words.append(word.lower())
        embed = discord.Embed(title="Add Bad Word", description=f'Added {word} to the  list of bad words.', color=discord.Color.blue())
        await ctx.send(embed=embed)
        await ctx.message.delete()
    # clear badword
    @commands.command(name='clear_bad_words')
    @commands.has_permissions(manage_messages=True)
    async def clear_bad_words(self, ctx):
        self.bad_words.clear()
        embed = discord.Embed(title="Clear Bad Words", description=f'Cleared all bad words.', color=discord.Color.blue())
        await ctx.send(embed=embed)
        await ctx.message.delete()
    # remove badwords
    @commands.command(name='remove_bad_word')
    @commands.has_permissions(manage_messages=True)
    async def remove_bad_word(self, ctx, *, word):
        self.bad_words.remove(word.lower())
        embed = discord.Embed(title="Remove Bad Word", description=f'Removed {word} from the bad words list.' , color=discord.Color.blue())
        await ctx.send(embed=embed)
        
    # returns the list of bad words
    @commands.command(name='list_bad_words')
    @commands.has_permissions(manage_messages=True)
    async def list_bad_words(self, ctx):
        embed = discord.Embed(title="Bad Words List", description='\n'.join(self.bad_words), color=discord.Color.blue())
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))