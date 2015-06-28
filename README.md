MeneScraper is a Big Data project that monitors the social interactions of meneame.net
http://menealabs.benjami.cat/menescraper/

<h1>Information</h1>

<b>VirtualEnv</b><br>
This project uses virtualenv (https://virtualenv.pypa.io/en/latest/)<br>
The required pip packages are in <b>requirements.txt</b><br>

<b>Django</b><br>
This project is made using Django (https://www.djangoproject.com/)<br>
If you never used Django before I recomend taking it a look before trying to run your own menescraper.

<h1>For in case you want to run it yourself</h1>

Clone the repository in a directory<br>
Use <b>pip install -r requirements.txt</b> to install the needed dependencies.<br>
There's a few settings that you have to customize, it's marked with a <b>CONFIGURE-ME:</b><br>
The files that need configuration are the following:

<ul>
<li>meneame/meneame/settings.py</li>
<li>menescraper/settings.py</li>
<li>scraper/management/commands/social_sync.py</li>
</ul>

And it should be ready to run!<br>

<h1>Last Changelog</h1>

<b>v1.4.2</b><br>
- Now social_sync always uses UTC<br>
- Added a new message in originalurl.html to show the last time the URL was updated<br>
- Changed the way some dates showed in originalurl.html<br>
- Now the sessions that the filters create expire after two hours<br>
- The sessions that ChangeDateForm creates expire after two hours<br>
- All expired sessions get removed when the user visits the index page<br>
- Added a message in originalurl.html. It pops up when the URL has no interactions yet<br>
- Fixed that when the Facebook API returned no shares, social_sync crashed<br>
- Now social_sync sets the Facebook shares to 0 if Facebook returns none<br>
- Changed the footer to a less 'offensive' one<br>
- Changed the error message that appeared when the user typed an invalid date in the charts form<br>
- When no interactions are found on the selected date it now automatically changes the date<br>
- Added a message on originalurl.html to let the user know that Facebook won't let us track Facebook's URLs

<h1>Thanks To</h1>
<b>Benjamí Villoslada</b> - <a href="https://twitter.com/benjami" target="__blank">@benjami</a> | menescraper is his idea<br>
<b>Antoni Aloy</b> - <a href="https://twitter.com/aaloy" target="__blank">@aaloy</a> | for an amazing feedback!</b>
