import sqlite3
import discord


EMOJIS = {
    '❤': 'b',
    '👍': 'n',
    '👎': 'w',
    '☠': 'f'
}

FULL_NAMES = {
    'b': 'Bid',
    'n': 'No Objection',
    'w': 'Weak',
    'f': 'Flush',
}


con = sqlite3.connect('db.sqlite3')
cur = con.cursor()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

data = dict()


def valid_user(user_id):
    ids = cur.execute("SELECT id FROM rush_discord").fetchall()
    ids = [int(i[0]) for i in ids]
    return user_id in ids


def get_rushees():
    rushees = cur.execute("SELECT id, name FROM rush_rushee").fetchall()
    return rushees


def get_user_id(discord_id):
    users = cur.execute(f"SELECT user_id FROM rush_discord where id={discord_id}").fetchall()
    return users[0][0]


def get_filing(discord_id, rushee_id):
    user_id = get_user_id(discord_id)
    bid_type = cur.execute(
        f"SELECT type FROM rush_filing where active_id={user_id} AND rushee_id={rushee_id}").fetchone()
    if bid_type is None:
        return 'No Filing'
    else:
        return FULL_NAMES[bid_type[0]]


def add_bid(user_id, rushee_id, bid_type):
    clear_bids(user_id, rushee_id)
    cur.execute(
        f"INSERT INTO rush_filing(type, active_id, rushee_id) VALUES ('{bid_type}', '{user_id}', '{rushee_id}')")
    con.commit()


def clear_bids(user_id, rushee_id):
    cur.execute(f"DELETE FROM rush_filing where active_id={user_id} AND rushee_id={rushee_id}")
    con.commit()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # Skip messages from the bot
    if message.author == client.user:
        return

    # Skip non-DMs
    if type(message.channel) is not discord.DMChannel:
        return

    user_id = message.author.id

    if valid_user(user_id):
        data[user_id] = dict()
        rushees = get_rushees()
        for i in rushees:
            filing = get_filing(user_id, i[0])
            message = await message.channel.send(f'||{i[1]}: {filing}||')
            data[user_id][message.id] = {
                'id': i[0],
                'name': i[1],
                'channel': message.channel,
                'message': message
            }
            for j in EMOJIS.keys():
                await message.add_reaction(j)


@client.event
async def on_raw_reaction_add(reaction):
    await on_react(reaction, True)


@client.event
async def on_raw_reaction_remove(reaction):
    await on_react(reaction, False)


async def on_react(reaction, add):
    if reaction.user_id == client.user.id:
        return
    emoji = str(reaction.emoji)
    if emoji not in EMOJIS:
        return
    if reaction.user_id not in data:
        return
    if reaction.message_id not in data[reaction.user_id]:
        return
    user_data = data[reaction.user_id][reaction.message_id]
    rushee_id = user_data['id']
    rushee_name = user_data['name']
    message = user_data['message']
    if rushee_id not in [i[0] for i in get_rushees()]:
        return
    user_id = get_user_id(reaction.user_id)
    bid_type = EMOJIS[emoji]
    bid_name = FULL_NAMES[bid_type]
    if add:
        await message.edit(content=f'||{rushee_name}: {bid_name}||')
        add_bid(user_id, rushee_id, bid_type)
    else:
        await message.edit(content=f'||{rushee_name}: No Filing||')
        clear_bids(user_id, rushee_id)


with open('token') as f:
    token = f.read()
    client.run(token)
