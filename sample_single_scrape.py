import scraper

gi = scraper.scraper('instagram')	#source [e.g. "google", "twitter", "instagram"]
gi.set_outputDir('output/')	#output directory on local disk
gi.set_downloadLimit(10)	#specified number of images

gi.scrape( "design" )	#arq: tag, search query
gi.stop()	#close the browser once scraping is done
