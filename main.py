import discord
import os
import random
import tkinter as tk
import playsound
import asyncio
import threading
import logging
import subprocess
from playsound import playsound
from tkinter import messagebox
from dotenv import load_dotenv
from discord.ext import commands

# Set up logging
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)  # Scroll to the end



#Initializes a Discord client instance. This is the main entry point for interacting with the Discord API and building a Discord bot application.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="l!", intents=intents, help_command= None )

#GUI CLASS CHANNELS
async def send_message(command):
    channel = discord.utils.get(bot.get_all_channels(), name='⌨│ᴄᴏᴍᴍᴀɴᴅs-ʟɪsᴛ')  # Change to your channel name
    if channel:
        await channel.send(command)

#######  GUI Class ##########
class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discord Bot Control Center")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 800
        height = 600
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.configure(bg='#212121', highlightthickness=0)

        self.terminal_output = tk.Text(self, width=100, height=20, bg='black', fg='green')
        self.terminal_output.pack(padx=10, pady=10, fill="both", expand=True)
        self.terminal_output.insert(tk.END, "Bot Log Output:\n")

        # Create a frame for the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Kick User
        kick_frame = tk.Frame(button_frame)
        kick_frame.pack(fill="x")
        self.kick_label = tk.Label(kick_frame, text="User ID to Kick:")
        self.kick_label.pack(side="left")
        self.kick_entry = tk.Entry(kick_frame, width=20)
        self.kick_entry.pack(side="left")
        self.kick_button = tk.Button(kick_frame, text="Kick User", command=self.kick_user)
        self.kick_button.pack(side="left", padx=10)

        # Ban User
        ban_frame = tk.Frame(button_frame)
        ban_frame.pack(fill="x")
        self.ban_label = tk.Label(ban_frame, text="User ID to Ban:")
        self.ban_label.pack(side="left")
        self.ban_entry = tk.Entry(ban_frame, width=20)
        self.ban_entry.pack(side="left")
        self.ban_button = tk.Button(ban_frame, text="Ban User", command=self.ban_user)
        self.ban_button.pack(side="left", padx=10)

        # Bible Verse
        self.bible_button = tk.Button(button_frame, text="Get Bible Verse", command=self.get_bible_verse)
        self.bible_button.pack(fill="x", pady=10)

        # Chat Box
        chat_frame = tk.Frame(button_frame)
        chat_frame.pack(fill="x")
        self.chat_label = tk.Label(chat_frame, text="Message to Send:")
        self.chat_label.pack(side="left")
        self.chat_entry = tk.Entry(chat_frame, width=50)
        self.chat_entry.pack(side="left", fill="x", expand=True)
        self.chat_button = tk.Button(chat_frame, text="Send Message", command=self.send_message)
        self.chat_button.pack(side="left", padx=10)

        # Restart button
        self.restart_button = tk.Button(button_frame, text="Restart Bot", command=self.restart_bot)
        self.restart_button.pack(fill="x", pady=10)


        # Set up logging to the terminal output
        logging.basicConfig(level=logging.INFO)
        handler = TextHandler(self.terminal_output)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(handler)
    
    async def kick_member(self, user_id):
        guild = discord.utils.get(bot.guilds)  # Get the first guild (server) the bot is in
        member = guild.get_member(user_id)  # Find the member by ID
        if member:
            await member.kick(reason="Kicked by bot command")
            messagebox.showinfo("Info", f"Kicked user: {member.name}")
        else:
            messagebox.showerror("Error", f"User  not found: {user_id}")
        logging.info(f"Kicked user: {member.name}")
        

    async def ban_member(self, user_id):
        guild = discord.utils.get(bot.guilds)  # Get the first guild (server) the bot is in
        member = guild.get_member(user_id)  # Find the member by ID
        if member:
            await member.ban(reason="Banned by bot command")
            messagebox.showinfo("Info", f"Banned user: {member.name}")
        else:
            messagebox.showerror("Error", f"User  not found: {user_id}")
        logging.info(f"Banned user: {member.name}")

    async def send_message_to_channel(self, message):
        channel = discord.utils.get(bot.get_all_channels(), name='⌨│ʙᴏᴛ-ᴄᴍᴅ',)  # Replace with your channel name
        if channel:
            await channel.send(message)
        else:
            messagebox.showerror("Error", "Channel not found.")
            await self.update_chatbox()
        
    def kick_user(self):
        try:
            user_id = int(self.kick_entry.get())  # Get user ID from entry
            asyncio.run_coroutine_threadsafe(self.kick_member(user_id), bot.loop)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid user ID.")

    def ban_user(self):
        try:
            user_id = int(self.ban_entry.get())  # Get user ID from entry
            asyncio.run_coroutine_threadsafe(self.ban_member(user_id), bot.loop)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid user ID.")

    def send_message(self):
        message = self.chat_entry.get()  # Get message from entry
        if message:
            asyncio.run_coroutine_threadsafe(self.send_message_to_channel(message), bot.loop)
        else:
            messagebox.showerror("Error", "Please enter a message to send.")
        logging .info(f"Sent message: {message}")

        
    def get_bible_verse(self):
        verse = random.choice(bible_verses)
        messagebox.showinfo("Bible Verse", verse)
        
    def destroy(self):
        print("Shutting down the bot...")
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)  # Log out the bot
        super().destroy()  # Call the superclass destroy method to close the GUI
    
    def restart_bot(self):
        self.destroy()
        os.system("python main.py")
# List of Bible verses
bible_verses = [
    "For I know the plans I have for you, declares the LORD, plans to prosper you and not to harm you, plans to give you hope and a future. - Jeremiah 29:11",
    "I can do all things through Christ who strengthens me. - Philippians 4:13",
    "The LORD is my shepherd; I shall not want. - Psalm 23:1",
    "Trust in the LORD with all your heart and lean not on your own understanding. - Proverbs 3:5",
    "And we know that in all things God works for the good of those who love him, who have been called according to his purpose. - Romans 8:28",
    "But the fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control. - Galatians 5:22-23",
    "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. - John 3:16",
    "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you. - Numbers 6:24-25",
    "Be strong and courageous. Do not be afraid; do not be discouraged, for the LORD your God will be with you wherever you go. - Joshua 1:9",
    "The peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus. - Philippians 4:7",
    "Come to me, all you who are weary and burdened, and I will give you rest. - Matthew 11:28",
    "Love is patient, love is kind. It does not envy, it does not boast, it is not proud. - 1 Corinthians 13:4",
    "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. - Philippians 4:6",
    "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord. - Romans 8:38-39",
    "You are the light of the world. A town built on a hill cannot be hidden. - Matthew 5:14",
    "And now these three remain: faith, hope and love. But the greatest of these is love. - 1 Corinthians 13:13",
    "I have been crucified with Christ and I no longer live, but Christ lives in me. The life I now live in the body, I live by faith in the Son of God, who loved me and gave himself for me. - Galatians 2:20",
    "You are the salt of the earth. But if the salt loses its saltiness, how can it be made salty again? - Matthew 5:13",
    "Do not let anyone look down on you because of your youth, but set an example for the believers in speech, in conduct, in love, in faith and in purity. - 1 Timothy 4:12",
    "Cast all your anxiety on him because he cares for you. - 1 Peter 5:7",
    "God is our refuge and strength, an ever-present help in trouble. - Psalm 46:1",
    "Love each other as I have loved you. - John 15:12",
    "Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you. - Ephesians 4:32",
    "Get rid of all bitterness, rage and anger, brawling and slander, along with every form of malice. - Ephesians 4:31",
    "Be still and know that I am God. - Psalm 46:10",
    "Delight yourself in the Lord, and he will give you the desires of your heart. - Psalm 37:4",
    "Commit to the Lord whatever you do, and he will establish your plans. - Proverbs 16:3",
    "Trust in the Lord with all your heart and lean not on your own understanding. - Proverbs 3:5",
    "Whoever sows sparingly will also reap sparingly, and whoever sows generously will also reap generously. - 2 Corinthians 9:6",
    "For where your treasure is, there your heart will be also. - Matthew 6:21",
    "Do not store up for yourselves treasures on earth, where moths and vermin destroy, and where thieves break in and steal. - Matthew 6:19",
    "Store up for yourselves treasures in heaven, where moths and vermin do not destroy, and where thieves do not break in and steal. - Matthew 6:20",
    "Ask and it will be given to you; seek and you will find; knock and the door will be opened to you. - Matthew 7:7",
    "Whoever believes and is baptized will be saved, but whoever does not believe will be condemned. - Mark 16:16",
    "For God did not give us a spirit of fear, but of power and love and self-discipline. - 2 Timothy 1:7",
    "Be joyful in hope, patient in affliction, faithful in prayer. - Romans 12:12",
    "Do not be conformed to the pattern of this world, but be transformed by the renewing of your mind. - Romans 12:2",
    "Do not be overcome by evil, but overcome evil with good. - Romans 12:21",
    "Love your neighbor as yourself. - Mark 12:31",
    "Honor your father and mother, and love your neighbor as yourself. - Matthew 19:19",
    "Do not judge, or you too will be judged. - Matthew 7:1",
    "Do not condemn, and you will not be condemned. Forgive, and you will be forgiven. - Luke 6:37",
    "Give, and it will be given to you. A good measure, pressed down, shaken together and running over, will be poured into your lap. - Luke 6:38",
    "Whoever wants to become great among you must be your servant. - Mark 10:43",
    "Whoever wants to save their life will lose it, but whoever loses their life for me will save it. - Luke 9:24",
    "Whoever humbles themselves will be exalted. - Luke 14:11",
    "Whoever exalts themselves will be humbled. - Luke 14:11",
    "Whoever wants to be first must be last of all and servant of all. - Mark 9:35",
    "Whoever wants to be great among you must be your servant, and whoever wants to be first must be slave of all. - Mark 10:44",
    "Whoever loses their life for me and for the gospel will save it. - Mark 8:35",
    "Whoever wants to save their life will lose it, but whoever loses their life for me and for the gospel will save it. - Mark 8:35",
    "Whoever wants to follow me must deny themselves and take up their cross and follow me. - Mark 8:34",
    "Whoever wants to follow me must deny themselves and take up their cross daily and follow me. - Luke 9:23",
    "Whoever wants to follow me must deny themselves and take up their cross and follow me. - Matthew 16:24",
]





##Events##

# Function to run the GUI
def run_gui():
    gui = BotGUI()
    gui.mainloop()




# Get command  s from cogs
# Run the bot

if __name__ == "__main__":
    # Start the GUI in a separate thread
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Command not found: {ctx.message.content}")
    else:
        print(f"An error occurred: {error}")


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="over Lucas | L!help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Hola! Soy DORA!")
    print("Here are my commands:")
    for command in bot.commands:
        print(command.name)
    print(bot.user)
    print("Xyperserver")
    playsound('C:/Users/gamin/Desktop/Lucas bot/ping_sound.mp3')

###Load cogs##
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} Loaded")
        
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
# Help Cog
async def help():
    for filename in os.listdir("./cogs/help"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.help.{filename[:-3]}")
                print(f"{filename} Loaded")
        
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

# Misc cog
async def misc():
    for filename in os.listdir("./cogs/miscellaneous"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.miscellaneous.{filename[:-3]}")
                print(f"{filename} Loaded")

            except Exception as e:
                print(f"Failed to load {filename}: {e}")
                
# Info cog
async def info():
    for filename in os.listdir("./cogs/info"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.info.{filename[:-3]}")
                print(f"{filename} Loaded")

            except Exception as e:
                print(f"Failed to load {filename}: {e}")

##Starts Bot and load cogs##
async def main():
    async with bot:
        await misc()
        await help()
        await info()
        await load()
        await bot.start('ODM2NDAzMjUwMzQ5MDgwNjA2.GzeIUG.FVvnzhTGKBqRIsv62eWP5d59oMnMcbmRDof1eM')

# Run the bot  

load_dotenv()
token = os.environ.get("DISCORD_BOT_SECRET")
asyncio.run(main())