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

<b>v1.4.1</b><br>
- Changed design of icons that aren't buttons<br>
- Removed remove card button<br>
- Now the "Information" icon in originalurl.html is a "Go back" button<br>
- The chart icon in originalurl.html is now a settings button<br>
- Unminified style.css and changed the colors there<br>
- Added logo and changed favicon<br>
- Removed old favicon from repository<br>
- Removed seconds from the chart<br>
- Changed chart tooltip<br>
- Added GNU 2.0 license http://www.gnu.org/licenses/gpl-2.0.txt<br>
- Moved the license of manage.py<br>
- Changed footer<br>
- Added some help text on the charts when no data is found

<h1>Thanks To</h1>
<b>Benjamí Villoslada</b> - <a href="https://twitter.com/benjami" target="__blank">@benjami</a> | menescraper is his idea<br>
<b>Antoni Aloy</b> - <a href="https://twitter.com/aaloy" target="__blank">@aaloy</a> | for an amazing feedback!</b>