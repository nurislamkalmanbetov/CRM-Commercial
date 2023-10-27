import aiohttp
http_api = 'https://crm.iwex.kg'


async def user_get(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/accounts/user-lists/?email={user_id}") as resp:
            data  = await resp.json()
            if data and not data[0]['is_staff']:
                return False
            if resp.status == 200:
                return data
            else:
                return False

                
async def user_list(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/bot/telegram_user_list/?user_id={user_id}") as resp:
            data  = await resp.json()
            if not data:
                return False
            if resp.status == 200:
                return data
            else:
                return False


async def user_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/bot/create_telegram_user/", data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False






