import discord
from discord.ext import commands, tasks
import subprocess
from bs4 import BeautifulSoup

class Javcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://www.javlibrary.com/en/vl_newrelease.php?&mode=2"
        self.user_id = 279805795183624192
        self.last_title = None
        self.check_website.start()

    @tasks.loop(minutes=60)
    async def check_website(self):
        try:
            # Use curl to fetch the webpage
            curl_command = [
                "curl",
                "-s",  # Silent mode
                "-A", "Mozilla/5.0 (compatible; DiscordBot/1.0)",  # User-Agent
                self.url
            ]
            result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
            html_content = result.stdout

            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the videos div and the first video title
            videos_div = soup.find('div', class_='videos')
            if not videos_div:
                print("Videos div not found")
                return

            first_video = videos_div.find('div', class_='video')
            if not first_video:
                print("No video found")
                return

            current_title = first_video.find('div', class_='title').get_text(strip=True)
            
            if self.last_title is None:
                # First run, just store the title without notifying
                self.last_title = current_title
                print(f"Initial title: {current_title}")
            elif current_title != self.last_title:
                user = await self.bot.fetch_user(self.user_id)
                await user.send(f"New JAV published! Check out **{current_title}** at {self.url}")
                print(f"Title changed from '{self.last_title}' to '{current_title}'")
                self.last_title = current_title
            else:
                print("No change in title")

        except subprocess.CalledProcessError as e:
            print(f"Error fetching webpage with curl: {e}")
        except Exception as e:
            print(f"Error processing webpage: {e}")

    @check_website.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.check_website.cancel()

async def setup(bot):
    await bot.add_cog(Javcheck(bot))