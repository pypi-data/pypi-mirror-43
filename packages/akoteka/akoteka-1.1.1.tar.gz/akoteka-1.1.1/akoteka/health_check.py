import os
import re
import configparser

from akoteka.handle_property import get_config_ini
from akoteka.handle_property import config_ini
from akoteka.handle_property import _

from akoteka.accessories import collect_cards
from akoteka.accessories import get_pattern_video
from akoteka.accessories import get_pattern_audio
from akoteka.accessories import get_pattern_image
from akoteka.accessories import get_pattern_card
from akoteka.accessories import get_pattern_length
from akoteka.accessories import get_pattern_year

HIGHLIGHT = '\033[31m'
COLORBACK = '\033[0;0m'

#def folder_investigation( actual_dir, json_list):
def folder_investigation( actual_dir):
    
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
    
    card['title'] = {}
    card['storyline'] = {}
                
    general_json_list = {}
    general_json_list['director'] = []
    general_json_list['sound'] = []
    general_json_list['sub'] = [] 
    general_json_list['genre'] = []
    general_json_list['theme'] = []
    general_json_list['actor'] = []
    general_json_list['country'] = []
    card['general'] = general_json_list
                
    card['rating'] = {}                                        
    card['links'] = {}

    extra_json_list = {}    
    extra_json_list['sub-cards'] = []
    extra_json_list['recent-folder'] = actual_dir
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
        
        try:            
            # save the http path of the image
            card['extra']['image-path'] = image_path_os

            # saves the os path of the media - There is no
            card['extra']['media-path'] = None
            
            card['title']['hu'] = parser.get("titles", "title_hu")
            card['title']['en'] = parser.get("titles", "title_en")
                
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            print(nop_err, "in ", card_path_os)
        
    # --------------------------------
    #
    # it is a MEDIA CARD dir
    #
    # there is:     -Card 
    #               -Media
    # 
    # --------------------------------
    elif card_path_os and media_path_os:

        err = []

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
            err.append(str(nop_err))
        else:
            if not card['title']['hu']:
                err.append("Empty attribute: 'title_hu' in section: 'titles'")
                
        try:            
            card['title']['en'] = parser.get("titles", "title_en")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['title']['en']:
                err.append("Empty attribute: 'title_en' in section: 'titles'")

        try:
            card['storyline']['hu'] = parser.get("storyline", "storyline_hu")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))

        try:
            card['storyline']['en'] = parser.get("storyline", "storyline_en")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))

        try:            
            card['general']['year'] = parser.get("general", "year")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['year'] :
                err.append("Empty attribute: 'year' in section: 'general section'")
            elif not get_pattern_year().match( card['general']['year'] ):
                err.append("Wrong attribute: 'year' in section: 'general' value: " + HIGHLIGHT + card['general']['year'] + COLORBACK)
            
        try:
            directors = parser.get("general", "director").split(",")            
            for director in directors:
                card['general']['director'].append(director.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['director']:
                err.append("Empty attribute: 'director' in section: 'general'")
            
        try:
            card['general']['length'] = parser.get("general", "length")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['length']:
                err.append("Empty attribute: 'length' in section: 'general'")
            elif not get_pattern_length().match( card['general']['length'] ):
                err.append("Wrong attribute: 'length' in section: 'general' value: " + HIGHLIGHT + card['general']['length'] + COLORBACK)
                
        try:
            sounds = parser.get("general", "sound").split(",")
            for sound in sounds:
                if sound:
                    if "lang_" in _("lang_" + sound.strip()):
                        err.append("Missing translation for 'sound': " + HIGHLIGHT + "lang_" + sound.strip() + COLORBACK + " in property files.")
                    if "lang_long_" in _("lang_long_" + sound.strip()):
                        err.append("Missing translation for 'sound': " + HIGHLIGHT + "lang_long_" + sound.strip() + COLORBACK + " in property files.")                    
                    card['general']['sound'].append(sound.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['sound']:
                err.append("Empty attribute: 'sound' in section: 'general'")

        try:
            subs = parser.get("general", "sub").split(",")
            for sub in subs:
                if sub:
                    if "lang_" in _("lang_" + sub.strip()):
                        err.append("Missing translation for 'sub': " + HIGHLIGHT + "lang_" + sub.strip() + COLORBACK + " in property files.")
                    if "lang_long_" in _("lang_long_" + sub.strip()):
                        err.append("Missing translation for 'sub': " + HIGHLIGHT + "lang_long_" + sub.strip() + COLORBACK + " in property files.")                    
                    card['general']['sub'].append(sub.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        
        try:
            genres = parser.get("general", "genre").split(",")
            for genre in genres:
                if "genre_" in _("genre_" + genre.strip()):
                    err.append("Missing translation for 'genre': " + HIGHLIGHT + "genre_" + genre.strip() + COLORBACK + " in property files.")
                card['general']['genre'].append(genre.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['genre']:
                err.append("Empty attribute: 'genre' in section: 'general'")

        try:
            themes = parser.get("general", "theme").split(",")
            for theme in themes:
                if theme:
                    if "theme_" in _("theme_" + theme.strip()):
                        err.append("Missing translation for 'theme': " + HIGHLIGHT + "theme_" + theme.strip() + COLORBACK + " in property files.")                
                    card['general']['theme'].append(theme.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))

        try:
            actors = parser.get("general", "actor").split(",")
            for actor in actors:
                card['general']['actor'].append(actor.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))

        try:
            countries = parser.get("general", "country").split(",")
            for country in countries:
                if "country_" in _("country_" + country.strip()):
                    err.append("Missing translation: " + HIGHLIGHT + "country_" + country.strip() + COLORBACK + " in property files.")
                if "country_long_" in _("country_long_" + country.strip()):
                    err.append("Missing translation: " + HIGHLIGHT + "country_long_" + country.strip() + COLORBACK + " in property files.")                   
                card['general']['country'].append(country.strip())
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['general']['country']:
                err.append("Empty attribute: 'country' in section: 'general'")

        try:
            card['rating']['best'] = parser.get("rating", "best")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['rating']['best']:
                err.append("Empty attribute: 'best' in section: 'rating'")
            
        try:
            card['rating']['new'] = parser.get("rating", "new")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['rating']['new']:
                err.append("Empty attribute: 'new' in section: 'rating'")

        try:
            card['rating']['favorite'] = parser.get("rating", "favorite")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))
        else:
            if not card['rating']['favorite']:
                err.append("Empty attribute: 'favorite' in section: 'rating'")

        try:                                                
            card['links']['imdb'] = parser.get("links", "imdb")
        except (configparser.NoSectionError, configparser.NoOptionError) as nop_err:
            err.append(str(nop_err))        

        if err:
            print(card_path_os)
            for msg in err:
                print("       " + msg)

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
        folder_investigation( subfolder_path_os )

    # and finaly returns
    return

def main():    
    config_ini_function = get_config_ini()
    paths = config_ini_function.get_media_path()
    folder_investigation(paths)
