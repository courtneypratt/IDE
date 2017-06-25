# IDE

The iGEM Development Environment (IDE).

IDE is a useful tool to allow local development for iGEM wiki users.

## Setup

In order to use IDE you will need python3.

Create an IDE page at `2017.igem.org/Team:TeamName/IDE` by editing the wiki page
and inserting only "IDE" as shown below for the Bristol team.

![](http://imgur.com/TQoEdXQ.png)

Then run server.py and go to `localhost:8000/Team:TeamName` in your browser. You
 should then see the original iGEM wiki template for Bristol.

## Editing

In order to edit the content go into the html folder

There are currently three sub-folders of importance:

 * css - This folder is where all your CSS should be stored. If you are planning
   on using Bootstrap 4, we have a customised version to increase compatibility
   with the iGEM wiki that can be found.
   [here](https://github.com/BristolIGEM2017/bootstrapIGEM). CSS can be
   included with the `{{css/style}}` tag to include `style.css`.
 * js - This folder should contain all of your JavaScript files. JavaScript can
   be included with the `{{js/script}}` tag to include `script.js`
 * templates - This folder should contain your templates. For example, the
   original template is included. To use it on a page you add a reference to
   the template as in wiki, that is `{{templates/header}}` to reference
   the header template

It is recommended that you have a generic header and footer template that apply
across the entirety of your wiki for ease of use.

The url correspond exactly to the folders i.e. to access a file called
`project.html` you must go to `localhost:8000/Team:Teamname/project`.

To have a page at `localhost:8000/Team:Teamname/project/description` it is
permissible to add additional folders, in this case you would require a file
called `description.html` in the folder `project`.

The base url is specified in `index.html` in the base html folder.

You do not need to restart the server to reload any of these files.


## Build

Currently not available. This will be added soon to output your files in a form
that is compatible with the iGEM wiki.


## Creators

**[Albert Wigmore](https://github.com/albertwigmore)** and **[Oliver Wright](https://github.com/meiamsome)**

If you require any assistance please contact aw13789@my.bristol.ac.uk
