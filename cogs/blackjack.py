import random
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blackjack", description="Play a hand!")
    async def blackjack(self, interaction: discord.Interaction):
        CARDS = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 10, "K": 10, "A": [1, 11]
        }
        dealerHand = []
        playerHand = []
        
        def get_card():
            card = random.choice(list(CARDS.keys()))
            return card
        
        def get_hand_value(hand):
            value = 0
            aces = 0
            for card in hand:
                if card == "A":
                    aces += 1
                else:
                    value += CARDS[card]
            for _ in range(aces):
                if value + 11 <= 21:
                    value += 11
                else:
                    value += 1
            return value
        
        # Deal initial hands
        for _ in range(2):
            playerHand.append(get_card())
            dealerHand.append(get_card())
        playervalue = get_hand_value(playerHand)
        dealervalue = get_hand_value(dealerHand)

        # Create a view with buttons
        class BlackjackView(View):
            def __init__(self):
                super().__init__(timeout=30)  # Timeout after 30 seconds
                self.playerHand = playerHand
                self.dealerHand = dealerHand
                self.interaction = interaction
                self.playervalue = playervalue
                self.dealervalue = dealervalue

            @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
            async def hit(self, interaction: discord.Interaction, button: Button):
                self.playerHand.append(get_card())
                self.playervalue = get_hand_value(self.playerHand)
                
                if self.playervalue > 21:
                    await interaction.response.edit_message(
                        content=f"Your hand: {self.playerHand} (Value: {self.playervalue})\n"
                                f"Dealer's hand: {self.dealerHand} (Value: {self.dealervalue})\n"
                                f"You busted! Dealer wins!",
                        view=None
                    )
                    self.stop()
                else:
                    await interaction.response.edit_message(
                        content=f"Your hand: {self.playerHand} (Value: {self.playervalue})\n"
                                f"Dealer's hand: {self.dealerHand[0]} and ?",
                        view=self
                    )

            @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
            async def stand(self, interaction: discord.Interaction, button: Button):
                # Dealer draws until 17 or higher
                while self.dealervalue < 17:
                    self.dealerHand.append(get_card())
                    self.dealervalue = get_hand_value(self.dealerHand)
                
                # Determine winner
                if self.dealervalue > 21:
                    result = "Dealer busted! You win!"
                elif self.dealervalue > self.playervalue:
                    result = "Dealer wins!"
                elif self.dealervalue < self.playervalue:
                    result = "You win!"
                else:
                    result = "Push! It's a tie!"
                
                await interaction.response.edit_message(
                    content=f"Your hand: {self.playerHand} (Value: {self.playervalue})\n"
                            f"Dealer's hand: {self.dealerHand} (Value: {self.dealervalue})\n"
                            f"{result}",
                    view=None
                )
                self.stop()

        # Send initial message with buttons
        view = BlackjackView()
        await interaction.response.send_message(
            f"Your hand: {playerHand} (Value: {playervalue})\n"
            f"Dealer's hand: {dealerHand[0]} and ?",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Blackjack(bot))