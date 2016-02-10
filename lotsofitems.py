from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import engine, Catalog, Base, Item, User

#engine = create_engine('sqlite:///catalog_items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database db_session object. Any change made against the objects in the
# db_session won't be persisted into the database until you call
# db_session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# db_session.rollback()
db_session = DBSession()


# Create dummy user
User1 = User(name="root", email="root@gmail.com")
db_session.add(User1)
db_session.commit()

# Add book catalogs
#001
_name = "Mystery"
cata = Catalog(name=_name)
db_session.add(cata)
#002
_name = "Kids"
cata = Catalog(name=_name)
db_session.add(cata)
#003
_name="Biography"
cata = Catalog(name=_name)
db_session.add(cata)
#004
_name="Romance"
cata = Catalog(name=_name)
db_session.add(cata)
db_session.commit()

# Add book titles
# 001
_user_id = 1
_name = "Passenger"
_author = "Alexandra Bracken"
_description = """
In one devastating night, violin prodigy Etta Spencer loses everything she
knows and loves. Thrust into an unfamiliar world by a stranger with a dangerous
agenda, Etta is certain of only one thing: she has traveled not just miles but
years from home. And she's inherited a legacy she knows nothing about from a
family whose existence she's never heard of. Until now. """
_picture = "https://d.gr-assets.com/books/1446749751l/20983362.jpg"
_catalog_id = 4
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)

# 002
_user_id = 1
_name = "The Sin of Angels"
_author = "William Winchester Nivin, Jody Riddle"
_description = """
Edward Marquand knew he was playing with fire, but he just didn't care. A young
man in love is a headstrong force of nature, immune to common sense. The heart
wants what the heart wants, and Eddie wanted Sally. Just eighteen in the summer
of 1850, he was perpetually distracted. But it was not the rolling fields of
his father's southern Illinois farm that flamed his imagination. That
distinction was reserved for the forbidden curves of Sally, his father's
light-skinned slave. Sally and Edward enjoyed a passionate, lustful love
affair, but each knew how dangerous their dalliance was. Both lovers feared
discovery, but for different reasons. And on the inevitable day they were
discovered, both lives changed in an instant. Just how will John, Edward's
identical twin, leverage this new knowledge against them? Edward fears that he
cannot count on his brother's discretion, and he shares Sally's fear for her
life. Can Edward find a way to keep them both safe, or will he have to take
even more drastic steps to protect the woman he loves?
"""
_picture = "https://d.gr-assets.com/books/1445191384l/20963378.jpg"
_catalog_id = 4
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 003
_user_id = 1
_name = "A Journey of Choice"
_author = "Pat Laster"
_description = """
Written with elegance, imagination, and historical savvy, Pat Laster's "A
Journey of Choice" grabbed me from the beginning and drew me into the life and
travails of Liddy Underhill ..." -Sandy Raschke, Fiction Editor, "Calliope, A
Writer's Workshop by Mail" In 1932, young Liddy Underhill, just graduated from
high school, lands a reporter's job in an adjacent town and hitches a ride with
a peddler who lives there. From the first night of her journey throughout the
next decade, Liddy is beset with challenges. She marries and begins a life with
her husband, Heth. When tragedy changes the course of her life, though, Liddy
must find a way to reclaim her life and find happiness, Along the way, she
becomes the victim of a womanizer, a controlling doctor, and an arsonist. She
suffers abandonment and an emotional breakdown. Set in the Missouri Ozarks of
the 1930s, "A Journey of Choice" tells the riveting tale of an enterprising
young woman dealing with events beyond her control and the message of hope that
emerges from her story.
"""
_picture = "https://d.gr-assets.com/books/1348121746l/10825796.jpg"
_catalog_id = 4
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)

db_session.commit()
print "Titles are added!"
