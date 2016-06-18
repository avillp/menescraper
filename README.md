MeneScraper is a Big Data project that monitors the social interactions of meneame.net  
http://menealabs.benjami.cat/menescraper/  

### Information

This project is no longer under development.  
Made with [Django](https://www.djangoproject.com/).  
Used [virtualenv](https://virtualenv.pypa.io/en/stable/).  

### Run it on your machine

**Debian/Ubuntu:**
```
$ cd ~ && mkdir menescraper && cd menescraper
$ git clone https://github.com/TheDegree0/menescraper.git .
$ mkvirtualenv menescraper && echo "cd $HOME/menescraper" >>  ~/.virtualenvs/menescraper/bin/postactivate
$ pip install -r requirements.txt
```

Replace all **CONFIGURE-ME:** in:  
* [meneame/meneame/settings.py](meneame/meneame/settings.py)
* [menescraper/settings.py](menescraper/settings.py)
* [scraper/management/commands/social_sync.py](scraper/management/commands/social_sync.py)

More info on [Django docs](https://docs.djangoproject.com/en/1.7/) and [Scrapy docs](http://doc.scrapy.org/en/latest/)

### Last Changelog

**v1.4.2**
- Now social_sync always uses UTC
- Added a new message in originalurl.html to show the last time the URL was updated
- Changed the way some dates showed in originalurl.html
- Now the sessions that the filters create expire after two hours
- The sessions that ChangeDateForm creates expire after two hours
- All expired sessions get removed when the user visits the index page
- Added a message in originalurl.html. It pops up when the URL has no interactions yet
- Fixed that when the Facebook API returned no shares, social_sync crashed
- Now social_sync sets the Facebook shares to 0 if Facebook returns none
- Changed the footer to a less 'offensive' one
- Changed the error message that appeared when the user typed an invalid date in the charts form
- When no interactions are found on the selected date it now automatically changes the date
- Added a message on originalurl.html to let the user know that Facebook won't let us track Facebook's URLs

### Thanks To
**Benjamí Villoslada** - [@benjami](https://twitter.com/benjami) | menescraper is his idea  
**Antoni Aloy** - [@aaloy](https://twitter.com/aaloy) | for an amazing feedback!
