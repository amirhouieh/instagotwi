import scraper

gi = scraper.scraper('google')	#source [e.g. "google", "twitter", "instagram"]
gi.set_outputDir('output/')	#output directory on local disk
gi.set_downloadLimit(100)	#specified number of images

gi.scrape( "design" )	#arq: tag, search query
gi.stop()	#close the browser once scraping is done
