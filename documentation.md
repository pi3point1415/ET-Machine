It is helpful to have used Django before. There's a decent tutorial [here](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) which this project is largely based on. In case you don't want to read through all of that documentation, here's a basic rundown of the relevant parts of this project's structure:

- Machine: this is the name of the overall project
	- Machine: this is where a few global settings for the project are located
		- settings.py: this sets the settings for the project
		- urls.py: this sets all of the urls for the website. Mainly, it imports urls from the rush app
	- rush: this is the app that handles all things actually specific to the working of the machine website
		- templates: this is where all of the html files are stored
		- forms.py: this handles all of the HTML forms for the website
		- models.py: this handles what is stored in the database and how it is accessed
		- urls.py: this sets all of the urls for the website
		- views.py: this is where each page of the website is defined
	- static: this is where static css/js files are stored
	- templates: this is where the html files for the login portion of the site are stored