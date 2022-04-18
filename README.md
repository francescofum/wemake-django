

<h1> WeMake Installation Guide </h1>

<ol>
  <li> Create a directory called "wemake-django" run <code>mkdir wemake-django && cd wemake-django</code> </li>
  <li> Clone this repo inside that directory <code>git clone git@github.com:francescofum/wemake-django.git src</code> </li>
  <li> from the "wemake-django" directory create a virtual environment by running <code>virtualenv wm-env</code> <br><strong>Note:</strong> virtualenv needs to be installed (run <code>sudo pip3 install virtualenv</code> to install) </li>
  <li> Activate your virtual environment <code>source wm-env/bin/activate</code> </li>
  <li> Install required modules <code>pip install -r src/requirements.txt</code> </li>
  <li> Run django server <code>cd src && python manage.py runserver</code> </li>
</ol>

<strong>Note:</strong> If you install any modules make sure to generate a new requirements.txt by running <code>pip freeze>requirements.txt</code>
<br>
<strong>Note:</strong> Remember to activate your environemnt each time you open a new terminal.

<h1> Creating a superuser </h1>
<ol> 
  <li> From the src directory run <code>python manage.py createsuperuser</code></li>
  <li> Fill in the details </li>
  <li> Start the server and navigate to http://127.0.0.1:8000/admin </li>
  <li> Make sure your user is the owner of all folders/files in directory. If not, <code>sudo chown -R ['user' eg: raul] wemake-django</code> </li>
</ol>

<h1> Making database migrations </h1>  
<p> 
  Any changes to any of the models requires a migration to take place. 
  This is fairly simple, first run <code>python manage.py makemigrations <optional application name> </code> followed by <code>python manage.py migrate</code>.
 </p>


<h1> Running a script using runscript </h1>  
<ol>
  <li> TODO </li>
</ol>

<h1> Setting up the debugger </h1> 
<ol>
  <li> TODO </li>
</ol>

<h1>Useful Plugins</h1>
<ul>
  <li>GitLense</li>
  <li>GitGraph</li>
  <li>Remote-SSH</li>
  <li>TODO: add django plugins</li>
</ul>


<h1>Useful Tips</h1>
<ul>
  <li>How do I ignore an error on 'git pull' about my local changes would be overwritten by merge?<code>git stash push --include-untracked</code><code>git pull</code><code>git stash drop</code></li> 

</ul>
