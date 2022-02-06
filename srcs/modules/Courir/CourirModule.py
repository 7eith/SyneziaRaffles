import PyInquirer
import requests

from singleton import Instance
from .utils import *

class CourirModule():

	def __init__(self):
		self.raffle = promptCourirRaffle()
		self.sizes = fetchSizesFromSlug(self.raffle["slug"])
		self.sizeRanges = promptSizeRanges(self.sizes)

