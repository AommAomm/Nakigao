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
            
            # Find the videos div
            videos_div = soup.find('div', class_='videos')
            if not videos_div:
                print("Videos div not found")
                return

            # Get all video titles
            new_videos = []
            video_elements = videos_div.find_all('div', class_='video')
            if not video_elements:
                print("No videos found")
                return

            for video in video_elements:
                title = video.find('div', class_='title').get_text(strip=True)
                if title == self.last_title:
                    break  # Stop when we reach the last known title
                new_videos.append(title)

            if new_videos:
                if self.last_title is None:
                    # First run, store the most recent title without notifying
                    self.last_title = new_videos[0]
                    print(f"Initial title: {self.last_title}")
                else:
                    # Send message with all new videos
                    user = await self.bot.fetch_user(self.user_id)
                    message = "New JAVs published!\n" + "\n".join([f"- **{title}**" for title in new_videos])
                    message += f"\nCheck them out at {self.url}"
                    await user.send(message)
                    print(f"New videos found: {new_videos}")
                    self.last_title = new_videos[0]  # Update to the most recent title
            else:
                print("No new videos")

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