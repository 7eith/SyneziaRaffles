'''

[notifier] footlocker_notifier.py

Author: seith <seith.corp@gmail.com>

Created: 19/04/2021 16:52:34 by seith
Updated: 19/04/2021 16:52:34 by seith

Synezia Corp. (c) 2021 - MIT

'''

from configuration.configuration import Configuration
from discord_webhook import DiscordWebhook, DiscordEmbed

def NotifyEndConfirmations(successTasks, failedTasks):
	whURL = Configuration().getWebhookURL()

	if (whURL):
		webhook = DiscordWebhook(
			url=whURL,
			username='SyneziaRaffle',
			avatar_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_bg.png?raw=true'
		)

		embed = DiscordEmbed(
			color=10721514
		)

		embed.set_thumbnail(
			url="https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true"
		)

		embed.set_author(
			name="Accounts confirmations is ended.",
			url="https://synezia.com",
			icon_url="https://github.com/SyneziaSoft/Public/blob/main/images/verifed.gif?raw=true",
		)

		embed.add_embed_field(name="Site", value="FootLocker (EU)", inline=False)
		embed.add_embed_field(name='Success: ', value=f"{successTasks} links confirmed", inline=True)
		embed.add_embed_field(name='Failed: ', value=f"{failedTasks} failed to confirm", inline=True)

		embed.set_footer(text="@SyneziaSoft [Tools]", icon_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true')
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
