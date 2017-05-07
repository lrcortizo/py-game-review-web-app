from google.appengine.api import users
from google.appengine.ext import ndb

from comment import Comment
from game import Game

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class DetailsHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            try:
                game = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            comments = Comment.query(Comment.game == game.id).order(Comment.date)
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "game": game,
                "comments": comments,
                "iduser": user.user_id(),
            }

            template = JINJA_ENVIRONMENT.get_template("details.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")