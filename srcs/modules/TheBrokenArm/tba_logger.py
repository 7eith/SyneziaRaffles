'''

[TheBrokenArm] tba_logger.py

Author: seith <seith.corp@gmail.com>

Created: 17/02/2021 11:41:06 by seith
Updated: 17/02/2021 11:41:06 by seith

Synezia Corp. (c) 2021 - MIT

'''

from configuration.configuration import Configuration
from logger.logger import Logger

from discord_webhook import DiscordWebhook, DiscordEmbed

def logWebhook(taskId, profile, raffleId):
	whURL = Configuration().getWebhookURL()
	webhook = DiscordWebhook(
		url=whURL,
		username='SyneziaRaffle',
		avatar_url='https://i.imgur.com/lCg5FU2.png'
	)

	embed = DiscordEmbed(
		title=raffleId, description="Task #{}".format(taskId), color=5305409
	)

	embed.set_thumbnail(
		url="https://www.the-broken-arm.com/themes/warehouse/img/nike-fragment-x-dunk-hi.jpg"
	)

	embed.set_author(
		name="Entered with success into Raffle",
		url="https://www.the-broken-arm.com/fr/raffle?color={}".format(raffleId),
		icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
	)

	embed.add_embed_field(name='Email: ', value='||{}||'.format(profile['email']), inline='true')
	embed.add_embed_field(name='Size: ', value='{} EU'.format(profile['size']), inline='true')

	embed.set_footer(text="SyneziaRaffle @ TheBrokenArm", icon_url='https://i.imgur.com/lCg5FU2.png')
	embed.set_timestamp()

	webhook.add_embed(embed)
	webhook.execute()

def logSuccessEntry(taskId, profile, raffleId):
	Logger.success(f"[{taskId}] Successfully entered into Raffle for {profile['email']}")

	f = open('logs/tba_entry.csv', 'a')
	f.write(f"SUCCESS,{profile['lastname']},{profile['firstname']},{profile['days']},{profile['months']},{profile['years']},{profile['phone']},{profile['email']},{profile['country']},{profile['size']}\n")
	f.close()
	
	logWebhook(taskId, profile, raffleId)


def logFailedEntry(taskId, profile, raffleId):
	Logger.error(f"[{taskId}] Failed entered into Raffle for {profile['email']}")

	f = open('logs/tba_entry.csv', 'a')
	f.write(f"FAILED,{profile['lastname']},{profile['firstname']},{profile['days']},{profile['months']},{profile['years']},{profile['phone']},{profile['email']},{profile['country']},{profile['size']}\n")
	f.close()