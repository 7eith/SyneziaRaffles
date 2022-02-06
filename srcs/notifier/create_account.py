'''

[notifier] create_account.py

Author: seith <seith.corp@gmail.com>

Created: 05/04/2021 05:43:33 by seith
Updated: 05/04/2021 05:43:33 by seith

Synezia Corp. (c) 2021 - MIT

'''

from configuration.configuration import Configuration
from discord_webhook import DiscordWebhook, DiscordEmbed

def getModuleURL(moduleName):
	if (moduleName == "StreetMachine"):
		return "[StreetMachine](https://streetmachine.com)"
	if (moduleName == "ThePlayOffs"):
		return "[ThePlayOffs](https://www.theplayoffs.com)"
	if (moduleName == "Solebox"):
		return "[Solebox](https://blog.solebox.com/)"
	if (moduleName == "Naked"):
		return "[Naked](https://nakedcph.com)"
	if (moduleName == "Kith"):
		return "[Kith](https://eu.kith.com)"
	if (moduleName == "Impact"):
		return "[Impact](https://www.impact-premium.com/)"
	if (moduleName == "Citadium"):
		return "[Citadium](https://www.citadium.com/)"

"""
	NotifyCreatedAccount
		profile ["email", "password"]
		moduleName "StreetMachine"
"""

def NotifyCreatedAccount(profile, moduleName):
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
			url="https://github.com/SyneziaSoft/Public/blob/main/images/created_account.png?raw=true"
		)

		embed.set_author(
			name="Successfully Created Account",
			url="https://synezia.com",
			icon_url="https://github.com/SyneziaSoft/Public/blob/main/images/success.gif?raw=true",
		)

		embed.add_embed_field(name="Site", value=getModuleURL(moduleName), inline=False)
		embed.add_embed_field(name='Email: ', value='||{}||'.format(profile['email']), inline=True)
		embed.add_embed_field(name='Password: ', value='||{}||'.format(profile['password']), inline=True)

		embed.set_footer(text="@SyneziaSoft [Raffle]", icon_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true')
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()

def NotifyEnterRaffle(profile, moduleName, thumbnail=None, productName=None):
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


		if (thumbnail):
			embed.set_thumbnail(
				url=thumbnail
			)

		embed.set_author(
			name="Successfully entered into Raffle",
			url="https://synezia.com",
			icon_url="https://github.com/SyneziaSoft/Public/blob/main/images/success.gif?raw=true",
		)

		embed.add_embed_field(name="Site", value=getModuleURL(moduleName), inline=False)

		if (productName):
			embed.add_embed_field(name='Product: ', value='{}'.format(productName), inline=False)

		if ("email" in profile):
			embed.add_embed_field(name='Email: ', value='||{}||'.format(profile['email']), inline=True)
		else:
			embed.add_embed_field(name='Phone: ', value='||{}||'.format(profile['phone']), inline=True)
			
		if ("size" in profile):
			embed.add_embed_field(name='Size: ', value='||{}||'.format(profile['size']), inline=True)

		embed.set_footer(text="@SyneziaSoft [Raffle]", icon_url='https://github.com/SyneziaSoft/Public/blob/main/images/logo_alone.png?raw=true')
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
		