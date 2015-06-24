MeneScraper is a Big Data project that monitors the social interactions of meneame.net

<h1>Information</h1>

<b>VirtualEnv</b><br>
This project uses virtualenv (https://virtualenv.pypa.io/en/latest/)<br>
The required pip packages are in <b>requirements.txt</b><br>

<b>Django</b><br>
This project is made using Django (https://www.djangoproject.com/)<br>
If you never used Django before I recomend taking it a look before trying to run your own menescraper.

<h1>Installation</h1>

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
