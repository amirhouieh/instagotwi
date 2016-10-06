import re, os, requests, shutil, json, urllib

from tools import loadJsonFile

from time import strftime, gmtime, sleep
from selenium import webdriver
from selenium.webdriver import Firefox
from pattern.web import DOM

class scraper(object):
    configs_data = loadJsonFile('/Users/amir/Python/instagotwi/scraper/configs.json')
    js_scrollToDown = "window.scrollTo(0, document.body.scrollHeight+100);"
    js_scrollToUp = "window.scrollTo(0, 0);"
    valid_image_ext_list = ['.png','.jpg','.jpeg', '.gif', '.bmp', '.tiff']

    def __init__(self, source=None):
        """ google_image, instagram, twitter search class
            Args:
                source name
        """         
        if source is None:
            raise 'Please select a source for CRAWLER'
            return
        elif source not in self.configs_data:
            raise 'The source is not defined, please use one of "instagram", "google", "twitter" as source'
            return

        self.currentHype = None
        self.driver = None
        self.counter = 0

        ## defaults
        self.source = source
        self.download_limit = 100
        self.window_w = None
        self.window_h = None
        self.window_x = None
        self.window_y = None

        ## url variables 
        self.baseUrl = None
        self.postUrl = None
        self.query = None
        self.currentKey = None

        self.elementStack = []
        self.elementStack_size = 0

        ## storage
        self.search_list = []
        self.info = []
        self.urls = []

        ## file and folder path
        self.OUTPUT_DIR = '.'
        self.FILENAME_CONVENTION = ''

        self.set_specifications()
        print '%s initialized!' %self.source 
        self.initializeBrowser()

        print "browser is initialized!"

    #general setting handlers
    def set_specifications(self):
        configData =   self.configs_data.get(self.source)

        self.baseUrl = configData['baseUrl']
        self.postUrl = configData['postUrl']
        self.selector = configData['selector']


        if self.source == 'twitter':
            self.updateQuery = self.setQuery_twitter
            self.extractUrl = self.extractUrl_twitter

        elif self.source == "instagram":
            self.updateQuery = self.setQuery_instagram
            self.extractUrl = self.extractUrl_instagram       

        elif self.source == "google":
            self.updateQuery = self.setQuery_google
            self.extractUrl = self.extractUrl_google        


        print configData
    def set_inputFile(self, input):
        _temp = []
        with open(input,'r') as f:
            _temp = f.readlines()

        for row in _temp:
            self.search_list.append( row )

        print 'list is made with %d entries' %len(self.search_list)
    def set_downloadLimit(self, limit):

        self.download_limit = limit
    def set_outputDir(self, _dir):
        self.OUTPUT_DIR = self.source + "_" + strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        self.OUTPUT_DIR = os.path.join(_dir, self.OUTPUT_DIR)

        if not os.path.exists( self.OUTPUT_DIR ):
            os.makedirs(self.OUTPUT_DIR)

    def setQuery_google(self):
        """
        """
        self.query = self.baseUrl + self.currentKey.replace(' ', '+') + self.postUrl 
    def setQuery_instagram(self):
        """
        """
        self.query = self.baseUrl + self.currentKey
    def setQuery_twitter(self):
        """
        """
        self.query = self.baseUrl + self.currentKey


    #driver controlers
    def stop(self):

        self.driver.close()
    def initializeBrowser(self):
        """
        """
        self.driver = webdriver.Firefox()
        if self.window_w != None:
            self.driver.set_window_size(self.window_w, self.window_h)
            self.driver.set_window_position(self.window_x, self.window_y)


    #page crawler and data mining
    def extractUrl_google(self, elem):
        """
        """
        return re.search('imgurl=(.*)&imgrefurl', elem.attributes['href']).group(1)
    def extractUrl_instagram(self, elem):
        """
        """
        return elem.attributes['src']
    def extractUrl_twitter(self, elem):
        """
        """
        return elem.attributes['src']

    def jack(self):
        """
        """
        attempts = 0
        lastNumberOfImages = 0

        while attempts < 3 and self.elementStack_size <= self.download_limit:
            if attempts >= 2 and self.source == "google_image":
                try:
                    loadMoreBtn = self.driver.find_element_by_id("smb")
                    loadMoreBtn.click()
                    self.driver.execute_script( self.js_scrollToUp )
                    sleep(3)
                except:
                    pass

            self.driver.execute_script( self.js_scrollToDown )
            sleep(1)
            self.driver.execute_script( self.js_scrollToUp )

            if self.elementStack_size == lastNumberOfImages:
                attempts +=1

            lastNumberOfImages =  self.elementStack_size
            # print 'attempts: %d, elementStack_size: %d' %(attempts, self.elementStack_size)
            print 'loaded images: %d' %(self.elementStack_size)
            self.updateElementStack()

    def crawlPage(self):
        """
        start to crawl the page untill we get enough 
        """
        self.updateElementStack()

        if self.source == "instagram":
            #there is a load more botton, which needs to be triggerd
            try:
                loadMore = self.driver.find_element_by_link_text("Load more")
                loadMore.click()
            except:
                self.jack()
                print 'no load more button found'

        sleep(1)
        self.jack()
        sleep(2)


    def extractUrls(self): 
        """
            we go through all image elements and extract the image url and 
            store them in list called "urls"
        """       
        self.updateElementStack()
        self.urls = []

        for elem in self.elementStack[:self.download_limit]:
            try:
                self.urls.append( self.extractUrl(elem) )
            except:
                print 'error parsing'
    def updateElementStack(self):
        """
            We keep track of number of loaded images by stroing image elements 
            in elementStack, and here after each jack we re-write the list
        """
        try:
            #It might be possible to use driver.source_page but,
            #I've got problems on parsing the page content quite often
            #hence I am using DOM moudle from patern which works like charm!

            dom = DOM(self.driver.page_source)
            self.elementStack = dom( self.selector )
            self.elementStack_size = len( self.elementStack )
        except:
            pass
    def getPageContent(self):
        """ 
            
        """
        self.driver.get(self.query)
        sleep(1)

        self.crawlPage()

    #name conventions
    def update_FILE_NAME_CONVENTION(self):
        """
            update name convention regarding current key
        """
        self.FILENAME_CONVENTION = self.currentKey.replace(' ','_').rstrip()


    #scraping methods
    def saveImage(self, r, filename):
        """
            save downaloded image
        """
        FULL_PATH = os.path.join(self.OUTPUT_DIR, filename )

        with open(FULL_PATH, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    def saveInfolist(self):
        """ Save the info list to file.
 
        """
        temp_filename_full_path = os.path.join(self.OUTPUT_DIR, self.FILENAME_CONVENTION + '_info.txt' )

        with  open(temp_filename_full_path, 'w') as f:
            for n in self.info:
                f.write(n)
                f.write('\n')

    def downloadImage(self, src):
        """
            - downalod this particular image
            - save downaloded image in output directory
        """

        print src
        src = urllib.unquote(urllib.unquote(src))
        print src
        print ""
        extension = os.path.splitext( src )[1]

        if extension not in self.valid_image_ext_list:
            return

        try:
            r = requests.get(src, stream=True, allow_redirects=False)
            if r.status_code == 200:
                filename = str(self.counter) + "-" + self.FILENAME_CONVENTION +'-'+ self.source + extension
                self.saveImage(r, filename)
                self.info.append( filename + '\t' + src )
                print str(self.counter) +  ": " + src[0:12] + " ... " + src[len(src)-15:len(src)]+ ' '  + 'is downloaded!'
                self.counter +=1

        except requests.Timeout as err:
            print  err.message
        except requests.RequestException as err:
            print err

    def downloadImages(self):
        """
            downalod all the images's url which exsist in self.urls
        """
        print 'start to downalod ' + str(len(self.urls)) + ' images!'
        print '::::::::::::::::::::::::::::::::::::'

        for src in self.urls:
            self.downloadImage(src)

        print '####################################'
        print self.FILENAME_CONVENTION + ' is done!'
        print ''
        print ''

    def scrape(self, _key=None):
        """
            this function get one search term as key and do following steps:
                - creat the url query based on the source and search key
                - gets page content and extract images 
                - save image urls 
                - downalod all the urls and same time write them in info_list as txt file
        """
        if _key is None:
            raise 'pass a key as an arqument'
            return

        self.currentKey = _key

        self.updateQuery()
        self.update_FILE_NAME_CONVENTION()
        self.getPageContent()
        self.extractUrls()
        self.downloadImages()
        self.saveInfolist()

    def scrape_list(self, dirToList):
        """
            trigger scrape function automaticly 
            by reading input file 
            each line will be read as one search key
        """
        self.set_inputFile(dirToList)
        for _key in self.search_list:
            self.scrape( _key )