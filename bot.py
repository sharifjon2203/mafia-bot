import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define your Telegram bot token here
API_TOKEN = '7655315804:AAEA5HtBoVlcgQ_V9W40QoKIZWxW4hrWThU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Game state
players = []
game_started = False
roles = ["Mafia", "Mafia", "Mafia", "Don", "Detective", "Doctor", "Villager", "Villager", "Villager", "Villager"]
player_roles = {}

# Helper function to randomize roles
def assign_roles():
    random.shuffle(roles)
    for i, player in enumerate(players):
        player_roles[player] = roles[i]

# Start command
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    global game_started
    if not game_started:
        await message.answer("Welcome to the Mafia game! Type /join to join the game.")
    else:
        await message.answer("The game has already started!")

# Join command
@dp.message_handler(commands=['join'])
async def join_game(message: types.Message):
    global players, game_started
    if game_started:
        await message.answer("The game has already started, you can't join now.")
    else:
        if message.from_user.username not in players:
            players.append(message.from_user.username)
            await message.answer(f"{message.from_user.username} has joined the game!")
        else:
            await message.answer("You're already in the game!")

# Start the game command
@dp.message_handler(commands=['startgame'])
async def start_game_phase(message: types.Message):
    global game_started
    if len(players) < 4:
        await message.answer("Not enough players to start the game. Minimum 4 players required.")
        return
    
    if not game_started:
        game_started = True
        assign_roles()  # Randomly assign roles
        await message.answer("Game started! Roles have been assigned.")
        for player in players:
            await bot.send_message(player, f"Your role is: {player_roles[player]}")
        
        # Start the Night phase
        await message.answer("Night phase: Mafia, Don, and Doctor, make your decisions privately.")
    else:
        await message.answer("The game is already running.")

# Night phase
@dp.message_handler(commands=['night'])
async def night_phase(message: types.Message):
    if not game_started:
        await message.answer("The game has not started yet!")
        return

    # Only Mafia and Don can act in night phase
    if player_roles.get(message.from_user.username) in ["Mafia", "Don"]:
        await message.answer("It's your turn! Choose a player to eliminate.")
        # Logic to handle Mafia action
    else:
        await message.answer("It's not your turn yet. Wait for your phase.")

# Day phase (Voting)
@dp.message_handler(commands=['day'])
async def day_phase(message: types.Message):
    if not game_started:
        await message.answer("The game has not started yet!")
        return

    await message.answer("Day phase: Everyone votes for who to eliminate. Type /vote followed by a player's name.")

# Voting command
@dp.message_handler(commands=['vote'])
async def vote_player(message: types.Message):
    global players
    if not game_started:
        await message.answer("The game has not started yet!")
        return

    vote_target = message.get_args()
    if vote_target in players:
        # Logic to eliminate player
        players.remove(vote_target)
        await message.answer(f"{vote_target} has been voted off the game!")
    else:
        await message.answer("Invalid player name. Try again.")

# End game command
@dp.message_handler(commands=['endgame'])
async def end_game(message: types.Message):
    global game_started
    if game_started:
        game_started = False
        players.clear()
        player_roles.clear()
        await message.answer("The game has ended!")
    else:
        await message.answer("No game is currently running.")

# Run the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
