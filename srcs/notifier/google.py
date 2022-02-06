'''

[notifier] microsoft.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 09:56:16 by seith
Updated: 23/04/2021 09:56:16 by seith

Synezia Corp. (c) 2021 - MIT

'''

from configuration.configuration import Configuration
from discord_webhook import DiscordWebhook, DiscordEmbed

def NotifyFilledGoogleForm(profile, formURL, title):
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
			url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Google_Forms_2020_Logo.svg/1200px-Google_Forms_2020_Logo.svg.png"
		)

		embed.set_author(
			name="Successfully filled Google Form",
			url="https://synezia.com",
			icon_url="https://github.com/SyneziaSoft/Public/blob/main/images/success.gif?raw=true",
		)

		embed.add_embed_field(name="URL", value=f"||{formURL}||", inline=False)
		embed.add_embed_field(name='Title: ', value='{}'.format(title), inline=False)

		embed.set_footer(text="@SyneziaSoft [Raffle]", icon_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true')
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
