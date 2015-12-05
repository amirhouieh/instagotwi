# image scraper: python image scraper from Google Images, Instagram and twitter

"""
Instagotwi Image Scraper 0.2 beta

Developted by Mind Design, Amsterdam [http://minddesign.info]
Published under Creative Commons license Attribution-NonCommercial-ShareAlike [https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode]
Programming by Amir Houieh
September 2015
"""

## To Install requirements
	$ sudo pip install requirements.txt


## Get it to work
	INITIALIZATION:
		"""
		avaible source_names: 
		'google_image','twitter','instagram'
		"""

		s = scraper.scraper( 'source_name' )


	CONFIGURATIONS:
		s.set_inputFile( 'path_to_source_text_file' )	#string
		s.set_outputDit( 'path_to_output_directory' ) #string
		s.set_downloadLimit( max_number_of_images_to_download ) #int


	RUN:
		s.scrape_list() #to scrape images from all items exist in input file
		s.scrape( 'search_key' ) # to scrape images from a specific search_key  #test purpose 
