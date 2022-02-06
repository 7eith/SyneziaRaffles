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

def logWebhook(taskId, profile):
	whURL = Configuration().getWebhookURL()
	webhook = DiscordWebhook(
		url=whURL,
		username='SyneziaRaffle',
		avatar_url='https://i.imgur.com/lCg5FU2.png'
	)

	embed = DiscordEmbed(
		title="Califia", description="Task #{}".format(taskId), color=5305409
	)

	embed.set_thumbnail(
		url="https://i8.amplience.net/i/jpl/aleahimay-blog2-1-b725a762b41b4d6a61d10b66f42f4fbf"
	)

	embed.set_author(
		name="Entered with success into Raffle",
		url="https://footpatrol.s3.amazonaws.com/content/site/2017/FootPatrolRafflePage-niker-hyper.html",
		icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
	)

	embed.add_embed_field(name='Email: ', value='||{}||'.format(profile['email']), inline='true')
	embed.add_embed_field(name='Size: ', value='{} EU'.format(profile['size']), inline='true')

	embed.set_footer(text="SyneziaRaffle @ FootPatrol", icon_url='https://i.imgur.com/lCg5FU2.png')
	embed.set_timestamp()

	webhook.add_embed(embed)
	webhook.execute()

def logSuccessEntry(taskId, profile):
	Logger.success(f"[{taskId}] Successfully entered into Raffle for {profile['email']}")

	f = open('logs/fp_entry.csv', 'a')
	f.write(f"SUCCESS,{profile['first_name']},{profile['last_name']},{profile['email']}\n")
	f.close()
	
	logWebhook(taskId, profile)


def logFailedEntry(taskId, profile):
	Logger.error(f"[{taskId}] Failed entered into Raffle for {profile['email']}")

	f = open('logs/fp_entry.csv', 'a')
	f.write(f"FAILED,{profile['first_name']},{profile['last_name']},{profile['email']}\n")
	f.close()