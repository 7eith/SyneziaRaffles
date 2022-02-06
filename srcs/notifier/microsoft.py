'''

[notifier] microsoft.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 09:56:16 by seith
Updated: 23/04/2021 09:56:16 by seith

Synezia Corp. (c) 2021 - MIT

'''

from configuration.configuration import Configuration
from discord_webhook import DiscordWebhook, DiscordEmbed

def NotifyFilledForm(profile, formURL, title, speed):
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
			url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBYER3XttJA59034ufSBljt6oK5HbVIzTXapyKkbzsBXE8NdP88i5Ig_bCMXG1IecFyuk&usqp=CAU"
		)

		embed.set_author(
			name="Successfully filled Microsoft Form",
			url="https://synezia.com",
			icon_url="https://github.com/SyneziaSoft/Public/blob/main/images/success.gif?raw=true",
		)

		embed.add_embed_field(name="URL", value=f"||{formURL}||", inline=False)
		embed.add_embed_field(name='Title: ', value='[{}]({})'.format(title, formURL), inline=False)
		embed.add_embed_field(name='Speed: ', value='{}s'.format(speed), inline=False)

		embed.set_footer(text="@SyneziaSoft [Raffle]", icon_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true')
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
