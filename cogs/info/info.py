import discord
from discord.ext import commands
import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Rules 
    @commands.command(name='rules', brief='returns rules on server', description='Gives you rules using command l!rules')
    async def rules(self, ctx):
        embed=discord.Embed(title="Server Rules!", url="", description=f"{ctx.guild.name} is a gaming discord server which you can chat someone everywhere or anywhere here in xyperserver you can join our minecraft server or invite other users on other minecraft servers. cracked account is allowed", color=discord.Color.red())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/943828992992100413/82977fea531a3993a0a8c17fe3ad3eb9.webp")
        embed.add_field(name="Rules", value="These are the rules in the server", inline=False)
        embed.add_field(name="Rule No.1", value="Be respectful. We don't tolerate anyone who bullies someone or is being toxic.", inline=False)
        embed.add_field(name="Rule No.2", value="No racism, harassment, or sexual content.", inline=False)
        embed.add_field(name="Rule No.3", value="Don't share malicious content. Such as viruses or any program that can harm other users.", inline=False)
        embed.add_field(name="Rule No.4", value="Any content that is NSFW is not allowed under any circumstances.", inline=False)
        embed.add_field(name="Rule No.5", value="Do not post any photos in #📌│general-chat", inline=False)
        embed.add_field(name="Rule No.6", value="Do not misuse or spam on any of the channels", inline=False)
        embed.add_field(name="Rule No.7", value="Do not mention any staff when creating a ticket. Be patient and wait for the staff", inline=False)
        embed.add_field(name="Rule No.8", value="Spamming in any form is not allowed.", inline=False)
        embed.add_field(name="Rule No.9", value="Do not ping any staff if there's no legitimate reason", inline=False)
        embed.add_field(name="Rule No.10", value="Do not advertise any other server or any website in the server.", inline=False)
        embed.add_field(name=f"Members In {ctx.guild.name}", value=f"{ctx.guild.member_count}")
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
    ## BOT DEVELOPER COMMAND#   
    @commands.command(aliases=["dev"], name='developer', brief='Returns with bot dev name', description='This commands gets the bot developer name.')
    async def developer_info(self, ctx):
        embed = discord.Embed(title="Bot Developer", description="The bot was developed by:", color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/943828992992100413/82977fea531a3993a0a8c17fe3ad3eb9.webp")
        embed.add_field(name="Developer", value="Jhian Alvarez, AKA RedishGaming127", inline=False)
        embed.add_field(name="Socials", value="FB: https://web.facebook.com/jhian.manacpo", inline=False)
        embed.set_footer(text=f"Information requested by: {ctx.author.display_name}")
        await ctx.send(embed=embed)
            
    #Info command#
    @commands.command(name='info', brief='returns info on server', description='Gives you info on the server')
    async def info(self, ctx):
        embed = discord.Embed(title="Server Information", description="Here is the information of the server", color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "https://cdn.discordapp.com/avatars/943828992992100413/82977fea531a3993a0a8c17fe3ad3eb9.webp")
        embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
        embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Server Owner", value=ctx.guild.owner.mention, inline=False)
        embed.add_field(name="Server Member Count", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Server Boost Count", value=ctx.guild.premium_subscription_count, inline=False)
        embed.add_field(name="Server Roles", value=len(ctx.guild.roles), inline=False)
        embed.add_field(name="Server Emojis", value=len(ctx.guild.emojis), inline=False)
        embed.add_field(name="Server Banners", value="Yes" if ctx.guild.banner else "No", inline=False)
        embed.add_field(name="Server Description", value=ctx.guild.description if ctx.guild.description else "None", inline=False)
        embed.add_field(name="Server Features", value=', '.join(ctx.guild.features), inline=False)
        embed.add_field(name="Server Created At", value=ctx.guild.created_at.strftime("%a, %d %b %Y"), inline=False)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        embed.set_image(url="https://cdn.discordapp.com/attachments/943829013111111111/943829013111111111/animated-gif.gif")
        await ctx.send(embed=embed) 

    ##member count command##
    @commands.command(aliases=["mc"], name='member_count', brief='Gets the Member count on this server', description='Gives you a member count on the server using command l!member_count or l!mc')
    async def member_count(self, ctx):
        member_count = ctx.guild.member_count
        embed = discord.Embed(title=f"Members in {ctx.guild.name}", description=f"Total Members: {member_count}", color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "https://cdn.discordapp.com/avatars/943828992992100413/82977fea531a3993a0a8c17fe3ad3eb9.webp")
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
            

    # Invite Link Command
    @commands.command(name='invite_link', aliases=["il"], description='gives your invite link for the server using command l!il or l!invite_link', brief='gives your invite link')
    async def invite_link(self, ctx):
        embed = discord.Embed(title="Server Invite Link", description="Click the link below to invite friends to our server!", color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "https://cdn.discordapp.com/avatars/943828992992100413/82977fea531a3993a0a8c17fe3ad3eb9.webp")
        embed.add_field(name="Invite Link", value="https://discord.gg/aFt9ehJEcm", inline=False)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
        
    # User info command
    @commands.command(name='userinfo', aliases=["ui"], description='gives you information about a  user using command l!ui or l!userinfo', brief='gives you information about a user ') 
    async def userinfo(self, ctx, member: discord.Member = None): 
        if member is None:
            member = ctx.author 
        embed = discord.Embed(title=f"User Information - {member.name}", description=f"User ID : {member.id}", color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Status", value=member.status, inline=False)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%a, %d %b %Y %H:%M:%S"), inline=False)
        embed.add_field(name="Created At", value=member.created_at.strftime("%a, %d %b %Y %H:%M:%S"), inline=False)
        embed.add_field(name="Highest Role", value=member.top_role.mention, inline=False)
        embed.add_field(name="Roles", value=len(member.roles), inline=False)
        embed.add_field(name="Muted", value="Yes" if member.timed_out_until else "No", inline=False)
        embed.add_field(name="Boost", value="Yes" if member.premium_since else "No", inline=False)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await  ctx.send(embed=embed)





async def setup(bot):
    await bot.add_cog(Info(bot))