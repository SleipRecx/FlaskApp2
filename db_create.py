from app import db
from models import BlogPost

#create the database and the db tables
db.create_all()

#insert
db.session.add(BlogPost("First","first post"))


#commit changes
db.session.commit()

