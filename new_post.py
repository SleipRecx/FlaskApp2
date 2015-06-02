from app import db
from models import BlogPost

db.session.add(BlogPost("brooor","this is a test"))



#commit changes
db.session.commit()
