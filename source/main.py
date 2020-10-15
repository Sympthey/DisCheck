import aiohttp, asyncio, aiofiles, os, easygui, sys
from colorama import Fore, init

# Without this coloramam does not always display colours correcrly.
init()

# Our Function to read the tokens in the token file passed.
async def read_tokens(token_file):
    async with aiofiles.open(token_file) as opened_token_file:
        tokens = await opened_token_file.readlines()
        return tokens

async def write_tokens(token, verified):
    path = os.getcwd()
    if verified == "Valid":
        async with aiofiles.open(f"{path}/results/Valid Tokens.txt", mode="a") as verified_tokens:
            await verified_tokens.write(token+"\n")

    if verified == "Invalid":
        async with aiofiles.open(f"{path}/results/Invalid Tokens.txt", mode="a") as invalid_tokens:
            await invalid_tokens.write(token+"\n")
    
    if verified == "Locked":
        async with aiofiles.open(f"{path}/results/Locked Tokens.txt", mode="a") as locked_tokens:
            await locked_tokens.write(token+"\n")

async def check_token(token):
    async with aiohttp.ClientSession() as hit_endpoint:
        discord_api_endpoint = "https://discordapp.com/api/v6/users/@me/guilds"
        discord_headers = {
            "Content-Type": "application/json",
            "authorization": str(token)
        }
        send_data = await hit_endpoint.get(discord_api_endpoint, headers=discord_headers)
        if send_data.status == 200:
            check_json = await send_data.json()
            print(Fore.GREEN+f"[VALID] - {token}")
            await write_tokens(token, "Valid")

        if send_data.status == 403:
            print(Fore.YELLOW+f"[LOCKED] - {token}")
            await write_tokens(token, "Locked")

        if send_data.status == 401:
            print(Fore.RED+f"[INVALID] - {token}{token}")
            await write_tokens(token, "Invalid")

        if send_data.status == 429:
            print(Fore.WHITE+f"[WARNING] IP ADDRESS RATE LIMITED!")
        else:
            # If any other condition happens (should not)
            pass

async def main():
    path = os.getcwd()
    open(f"{path}/results/Valid Tokens.txt", "w").close()
    open(f"{path}/results/Invalid Tokens.txt", "w").close()
    open(f"{path}/results/Locked Tokens.txt", "w").close()
    sys.stdout.write(f'\x1b]2;[DisCheck - Discord Token Checker] | Developer Sympthey\x07')
    print(Fore.WHITE+"CHOOSE FILE WITH DISCORD TOKENS")
    file_path = easygui.fileopenbox()
    tokens = await read_tokens(file_path)
    amount_tokens = str(len(tokens))
    sys.stdout.write(f'\x1b]2;[DisCheck - Discord Token Checker] | Developer Sympthey | Tokens Loaded: {amount_tokens}\x07')
    await asyncio.sleep(1.2)
    for token in tokens:
        cleaned_token = str(token).strip()
        await check_token(cleaned_token)
    input("Press Any Key To Exit...")
    sys.exit()
    

asyncio.run(main())