import os
import sys
import re
import configparser
import cgi, cgitb
import logging
import psutil
import datetime
import time
   
from pathlib import Path
from threading import Thread
from subprocess import run
from subprocess import call

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget

from akoteka.handle_property import Config
from akoteka.handle_property import config_ini
#from akoteka.logger import logger

filter_key = {
    "title":{
        "store-mode": "t",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "title"
    },
    "best":{
        "store-mode": "v",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "rating"
    },
    "new":{
        "store-mode": "v",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "rating"
    },
    "favorite":{
        "store-mode": "v",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "rating"
    },
    "director":{
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "general"
    },
    "actor": {
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "general"
    },
    "theme":{
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": True,
        "value-dict-prefix": "theme_",
        "section": "general"
    },
    "genre":{        
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": True,
        "value-dict-prefix": "genre_",
        "section": "general"
    },
    "sound":{
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": True,
        "value-dict-prefix": "sound_",
        "section": "general"
    },
    "sub":{
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": True,
        "value-dict-prefix": "sub_",
        "section": "general"
    },
    "country":{
        "store-mode": "a",
        "key-dict-prefix": "title_",
        "value-dict": True,
        "value-dict-prefix": "country_",
        "section": "general"
    },
    "year":{
        "store-mode": "v",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "general"
    },    
    "length":{        
        "store-mode": "v",
        "key-dict-prefix": "title_",
        "value-dict": False,
        "section": "general"
    },
}

logger = None
def initialize_log():
    global logger
    LOG_FOLDER = 'logs'
    LOG_PATH = os.path.join(Config.get_path_to_config_folder(), LOG_FOLDER)
    filename = os.path.join(LOG_PATH, "test.log")    
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"
    Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
    logging.basicConfig( 
        filename = filename, 
        level = logging.WARNING,
        format = LOG_FORMAT,
        filemode = 'w'
    )
    logger = logging.getLogger()
    logger.critical('')
    logger.critical('--------- Started ----------')        
initialize_log()

class FlowLayout(QLayout):

    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    # to keep it in style with the others..
    def rowCount(self):
        return self.count()

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
    

def get_pattern_video():
    ptrn = '|'.join( config_ini['media_player_video_ext'].split(",") )
    return re.compile( '^.+[.](' + ptrn + ')$' )    

def get_pattern_audio():
    ptrn = '|'.join( config_ini['media_player_audio_ext'].split(",") )
    return re.compile( '^.+[.](' + ptrn + ')$' )    

def get_pattern_image():
    return re.compile( '^image[.]jp(eg|g)$' )
    
def get_pattern_card():
    return re.compile('^card.ini$')

def get_pattern_length():
    return re.compile('^\d{1,3}[:]\d{1,2}$')

def get_pattern_year():
    return re.compile('^(19|[2-9][0-9])\d{2}$')

def folder_investigation( actual_dir, json_list):
    
    # Collect files and and dirs in the current directory
    file_list = [f for f in os.listdir(actual_dir) if os.path.isfile(os.path.join(actual_dir, f))] if os.path.exists(actual_dir) else []
    dir_list = [d for d in os.listdir(actual_dir) if os.path.isdir(os.path.join(actual_dir, d))] if os.path.exists(actual_dir) else []

    # now I got to a certain level of directory structure
    card_path_os = None
    media_path_os = None
    image_path_os = None
    media_name = None
    
    is_card_dir = True

    # Go through all files in the folder
    for file_name in file_list:

        #
        # collect the files which count
        #
        
        # find the Card
        if get_pattern_card().match( file_name ):
            card_path_os = os.path.join(actual_dir, file_name)
            
        # find the Media (video or audio)
        if get_pattern_audio().match(file_name) or get_pattern_video().match(file_name):
            media_path_os = os.path.join(actual_dir, file_name)
            media_name = file_name
            
        # find the Image
        if get_pattern_image().match( file_name ):
           image_path_os = os.path.join(actual_dir, file_name)


    card = {}
    
    title_json_list = {}
#    title_json_list['hu'] = media_name
#    title_json_list['en'] = media_name
    card['title'] = title_json_list

    storyline_json_list = {}
#    storyline_json_list['hu'] = ""
#    storyline_json_list['en'] = ""
    card['storyline'] = storyline_json_list
                
    general_json_list = {}
 #   general_json_list['year'] = ""
    general_json_list['director'] = []
 #   general_json_list['length'] = ""
    general_json_list['sound'] = []
    general_json_list['sub'] = [] 
    general_json_list['genre'] = []
    general_json_list['theme'] = []
    general_json_list['actor'] = []
    general_json_list['country'] = []
    card['general'] = general_json_list
                
    rating_json_list = {}
 #   rating_json_list['best'] = ""
 #   rating_json_list['new'] = ""
 #   rating_json_list['favorite'] = ""
    card['rating'] = rating_json_list
                                        
    card['links'] = {}

    extra_json_list = {}    
#    extra_json_list['image-path'] = ""
#    extra_json_list['media-path'] = ""
    extra_json_list['recent-folder'] = actual_dir
    extra_json_list['sub-cards'] = []
    card['extra'] = extra_json_list


    # ----------------------------------
    #
    # it is a COLLECTOR CARD dir
    #
    # there is:     -Card 
    #               -at least one Dir
    # ther is NO:   -Media
    #  
    # ----------------------------------
    if card_path_os and not media_path_os and dir_list:
                
        parser = configparser.RawConfigParser()
        parser.read(card_path_os, encoding='utf-8')
        
        # I collect the data from the card and the image if there is and the folders if there are
        try:
            
            # save the http path of the image
            card['extra']['image-path'] = image_path_os

            # saves the os path of the media - There is no
            card['extra']['media-path'] = None
            
            card['title']['hu'] = parser.get("titles", "title_hu")
            card['title']['en'] = parser.get("titles", "title_en")
                
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)

        json_list.append(card)
        
    # --------------------------------
    #
    # it is a MEDIA CARD dir
    #
    # there is:     -Card 
    #               -Media
    # 
    # --------------------------------
    elif card_path_os and media_path_os:

        # first collect every data from the card
        parser = configparser.RawConfigParser()
        parser.read(card_path_os, encoding='utf-8')

        # save the os path of the image
        card['extra']['image-path'] = image_path_os            

        # saves the os path of the media
        card['extra']['media-path'] = media_path_os

        try:
            card['title']['hu'] = parser.get("titles", "title_hu")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['title']['hu'] = "Default title hu"
            
        try:            
            card['title']['en'] = parser.get("titles", "title_en")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['title']['en'] = "Default title en"

        try:
            card['storyline']['hu'] = parser.get("storyline", "storyline_hu")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['storyline']['hu'] = ""

        try:
            card['storyline']['en'] = parser.get("storyline", "storyline_en")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['storyline']['en'] = ""

        try:            
            card['general']['year'] = parser.get("general", "year")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['general']['year'] = '1900'
        else:
            if not get_pattern_year().match( card['general']['year'] ):
                card['general']['year'] = "1900"
            
        try:
            directors = parser.get("general", "director").split(",")            
            for director in directors:
                card['general']['director'].append(director.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            card['general']['length'] = parser.get("general", "length")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['general']['length'] = "0:00"
        else:
            if not get_pattern_length().match( card['general']['length'] ):
                card['general']['length'] = "0:00"
            
        try:
            sounds = parser.get("general", "sound").split(",")
            for sound in sounds:
                card['general']['sound'].append(sound.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            subs = parser.get("general", "sub").split(",")
            for sub in subs:
                card['general']['sub'].append(sub.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            genres = parser.get("general", "genre").split(",")
            for genre in genres:
                card['general']['genre'].append(genre.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            themes = parser.get("general", "theme").split(",")
            for theme in themes:
                card['general']['theme'].append(theme.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            actors = parser.get("general", "actor").split(",")
            for actor in actors:
                card['general']['actor'].append(actor.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            countries = parser.get("general", "country").split(",")
            for country in countries:
                card['general']['country'].append(country.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            
        try:
            card['rating']['best'] = parser.get("rating", "best")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['rating']['best'] = "n"
            
        try:
            card['rating']['new'] = parser.get("rating", "new")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['rating']['new'] = "n"

        try:
            card['rating']['favorite'] = parser.get("rating", "favorite")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['rating']['favorite'] = "n"

        try:                                                
            card['links']['imdb'] = parser.get("links", "imdb")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            log_msg("MESSAGE: " + str(nop_err) + " FILE NAME: " + card_path_os)
            card['links']['imdb'] = ""

        json_list.append(card)

    # ----------------------------------
    #
    # it is NO CARD dir
    #
    # ----------------------------------
    else:
        
        is_card_dir = False
        
    # ----------------------------
    #
    # Through the Sub-directories
    #
    # ----------------------------    
    for name in dir_list:
        subfolder_path_os = os.path.join(actual_dir, name)
        folder_investigation( subfolder_path_os, card['extra']['sub-cards'] if is_card_dir else json_list )

    # and finaly returns
    return

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater() 

def log_msg(message):
    logger.warning( message)    

def collect_cards( rootdirs ):
    media_list = []

    for rootdir in rootdirs:
        folder_investigation(rootdir, media_list)

    return media_list

def play_media(media_path):
    param_list = []
    player = None

    # video
    if get_pattern_video().match(media_path):
        switch_list = config_ini['media_player_video_param'].split(" ")
        player = config_ini['media_player_video']
        param_list.append(player)
        param_list.append(media_path)
        param_list += switch_list

        param_list.append("1>/dev/null")
        param_list.append("2>/dev/null")

    # audio
    elif get_pattern_audio().match(media_path):
        switch_list = config_ini['media_player_audio_param'].split(" ")
        player = config_ini['media_player_audio']
        param_list.append(player)
        #param_list += switch_list
        param_list.append(media_path)

    start_time = datetime.datetime.now().timestamp()

    pid = None

    if player:
    
        # start playing media    
        thread = Thread(target=run, args=(param_list, ))
        thread.start()
        time.sleep(0.2)
    
        # get the pid of the player
        for p in psutil.process_iter():
            if p.name() == player and (start_time-p.create_time()) <= 1.0:
                pid = p.pid
                break
            
    return pid

