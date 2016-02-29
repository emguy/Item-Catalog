from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import engine, Catalog, Base, Item, User

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

# Add book catagories
cat_names = ["Mystery", "Kids", "Biography", "Romance", "Health", "Travel", "Classic", "History", "Arts", "Fantasy", "Food"]

for cat_name in cat_names:
  cata = Catalog(name=cat_name)
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
next decade, Liddy is beset with challenges.  She marries and begins a life
with her husband, Heth. When tragedy changes the course of her life, though,
Liddy must find a way to reclaim her life and find happiness, Along the way,
she becomes the victim of a womanizer, a controlling doctor, and an arsonist.
She suffers abandonment and an emotional breakdown. Set in the Missouri Ozarks
of the 1930s, "A Journey of Choice" tells the riveting tale of an enterprising
young woman dealing with events beyond her control and the message of hope that
emerges from her story.
"""
_picture = "https://d.gr-assets.com/books/1348121746l/10825796.jpg"
_catalog_id = 4
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 004
_user_id = 1
_name = "The Winter Girl"
_author = "Matt Marinovich"
_description = """
A scathing and exhilarating thriller that begins with a husband's obsession
with the seemingly vacant house next door.

It's wintertime in the Hamptons, where Scott and his wife, Elise, have come to
be with her terminally ill father, Victor, to await the inevitable. As weeks
turn to months, their daily routine-Elise at the hospital with her father,
Scott pretending to work and drinking Victor's booze-only highlights their
growing resentment and dissatisfaction with the usual litany of unhappy
marriages: work, love, passion, each other. But then Scott notices something
simple, even innocuous. Every night at precisely eleven, the lights in the
neighbor's bedroom turn off. It's clearly a timer, but in the dead of winter
with no one else around, there's something about that light he can't let go of.
So one day while Elise is at the hospital, he breaks in. And he feels a jolt of
excitement he hasn't felt in a long time. Soon, it's not hard to enlist his
wife as a partner in crime and see if they can't restart the passion.

Their one simple transgression quickly sends husband and wife down a
deliriously wicked spiral of bad decisions, infidelities, escalating violence,
and absolutely shocking revelations. Matt Marinovich makes a strong statement
with this novel. The Winter Girl is the psychological thriller done to absolute
perfection.
"""
_picture = "https://d.gr-assets.com/books/1428938255l/25352450.jpg"
_catalog_id = 1
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 005
_user_id = 1
_name = "River Road"
_author = "Carol Goodman"
_description = """
From the award-winning author of The Lake of Dead Languages comes a chilling
new psychological thriller about a professor accused of killing her favorite
student in a hit-and-run accident.

Nan Lewis-a creative writing professor at a state university in upstate New
York-is driving home from a faculty holiday party after finding out she's been
denied tenure. On her way, she hits a deer, but when she gets out of her car to
look for it, the deer is nowhere to be found. Eager to get home and out of the
oncoming snowstorm, Nan is forced to leave her car at the bottom of her snowy
driveway to wait out the longest night of the year-and the lowest point of her
life...

The next morning, Nan is woken up by a police officer at her door with terrible
news-one of her students, Leia Dawson, was killed in a hit-and-run on River
Road the night before. And because of the damage to her car, Nan is a suspect.
In the days following the accident, Nan finds herself shunned by the same
community that rallied around her when her own daughter was killed in an eerily
similar accident six years prior. When Nan begins finding disturbing tokens
that recall the death of Nan's own daughter, Nan suspects that the two
accidents are connected.

As she begins to dig further, she discovers that everyone around her, including
Leia, is hiding secrets. But can she uncover them, clear her name, and figure
out who really killed Leia before her reputation is destroyed for good?
"""
_picture = "https://d.gr-assets.com/books/1454544060l/25111007.jpg"
_catalog_id = 1
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 006
_user_id = 1
_name = "Some Kind of Courage"
_author = "Dan Gemeinhart"
_description = """
Saddle up for a life-defining, death-defying adventure.

Joseph Johnson has lost just about everyone he's ever loved. He lost his pa in
an accident. He lost his ma and his little sister to sickness. And now, he's
lost his pony--fast, fierce, beautiful Sarah, taken away by a man who had no
right to take her.

Joseph can sure enough get her back, though. The odds are stacked against him,
but he isn't about to give up. He will face down deadly animals, dangerous men,
and the fury of nature itself on his quest to be reunited with the only family
he has left.

Because Joseph Johnson may have lost just about everything; but he hasn't lost
hope. And he hasn't lost the fire in his belly that says he's getting his Sarah
back--no matter what.
"""
_picture = "https://d.gr-assets.com/books/1432247765l/25578408.jpg"
_catalog_id = 2
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 007
_user_id = 1
_name = "The Goblin's Puzzle: Being the Adventures of a Boy with No Name and Two Girls Called Alice "
_author = "Andrew S. Chilton"
_description = """
Brimming with dragons, goblins, and logic puzzles, this middle-grade fantasy
adventure is perfect for readers who enjoyed The Princess Bride or Rump.

THE BOY is a nameless slave on a mission to uncover his true destiny. THE
GOBLIN holds all the answers, but he's too tricky to be trusted. PLAIN ALICE
is a bookish peasant girl carried off by a confused dragon. And PRINCESS ALICE
is the lucky girl who wasn't kidnapped.

All four are tangled up in a sinister plot to take over the kingdom, and
together they must face kind monsters, a cruel magician, and dozens of deathly
boring palace bureaucrats. They're a ragtag bunch, but with strength, courage,
and plenty of deductive reasoning, they just might outwit the villains and
crack the goblin's puzzle.
"""
_picture = "https://d.gr-assets.com/books/1443119798l/22464760.jpg"
_catalog_id = 2
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 008
_user_id = 1
_name = "Bad Kitty Goes to the Vet "
_author = "NickBruel"
_description = """
When Kitty is happy and healthy, everything is perfect. She jumps around, eats
everything in sight, and has the energy to keep slobbering puppies in their
place. But when she's sick, all she can do is lie in her bed. Looks like it's
time for this sick kitty to go...to the vet.

When Kitty's family finally manages to get their clawing, angry pet into the
doctor's office, it's a wild adventure for Kitty, who has to get the most
dreaded thing of all...a shot. Once the shot is administered, Kitty is cast
into an ingenious dream within a dream sequence in which she has to make right
by Puppy or risk being shut out of PussyCat heaven forever.

This ninth installment of the popular Bad Kitty series from Nick Bruel is
chock-full of brilliant supporting characters and, of course, the crankiest bad
kitty you've ever seen.
"""
_picture = "https://d.gr-assets.com/books/1429575882l/25332025.jpg"
_catalog_id = 2
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 009
_user_id = 1
_name = "Vegan Under Pressure: Perfect Vegan Meals Made Quick and Easy in Your Pressure Cooker "
_author = "Jill Nussinow"
_description = """
For the growing number of people who eat vegan, a pressure cooker is a blessing
when it comes to saving time and enjoying a wider variety of foods on a regular
basis. The pressure cooker drastically shortens the cooking times of healthful
vegan staples such as dried beans and ancient grains: suddenly hummus from
scratch and braised artichokes become weeknight fare. In Vegan Under Pressure,
Jill Nussinow shows how to use the appliance safely and effectively, and
reveals the breadth of vegan fare that can be made using a pressure cooker,
including Roasted Pepper and White Bean Dip, Harissa-Glazed Carrots with Green
Olives, Pozole Chili, Farro Salad with Tomatoes and Arugula, Thai Summer
Vegetable Curry, a chapter of veggie burgers, Cornbread, Pear-Almond Upside
Down Cake, and DIY soy milk and seitan. 
"""
_picture = "https://d.gr-assets.com/books/1447139150l/23719347.jpg"
_catalog_id = 11
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 010
_user_id = 1
_name = "Romeo and Juliet"
_author = "William Shakespeare"
_description = """
In Romeo and Juliet, Shakespeare creates a world of violence and generational
conflict in which two young people fall in love and die because of that love.
The story is rather extraordinary in that the normal problems faced by young
lovers are here so very large. It is not simply that the families of Romeo and
Juliet disapprove of the lover's affection for each other; rather, the
Montagues and the Capulets are on opposite sides in a blood feud and are trying
to kill each other on the streets of Verona. Every time a member of one of the
two families dies in the fight, his relatives demand the blood of his killer.
Because of the feud, if Romeo is discovered with Juliet by her family, he will
be killed. Once Romeo is banished, the only way that Juliet can avoid being
married to someone else is to take a potion that apparently kills her, so that
she is burried with the bodies of her slain relatives. In this violent,
death-filled world, the movement of the story from love at first sight to the
union of the lovers in death seems almost inevitable.

What is so striking about this play is that despite its extraordinary setting
(one perhaps reflecting Elizabethan attitudes about hot-blooded Italians), it
has become the quintessential story of young love. Because most young lovers
feel that they have to overcome giant obstacles in order to be together,
because they feel that they would rather die than be kept apart, and especially
because the language Shakespeare gives his young lovers is so exquisite,
allowing them to say to each other just what we would all say to a lover if we
only knew how, it is easy to respond to this play as if it were about all young
lovers rather than about a particular couple in a very unusual world. (When the
play was rewritten in the eighteen century as The History and Fall of Caius
Marius, the violent setting became that of a particularly discordant period in
classical Rome; when Leonard Berstein rewrote the play as West Side Story, he
chose the violent world of New York street gangs.)
"""
_picture = "https://d.gr-assets.com/books/1327872146l/18135.jpg"
_catalog_id = 7
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 011
_user_id = 1
_name = "The Love That Split the World"
_author = "Emily Henry"
_description = """
Natalie Cleary must risk her future and leap blindly into a vast unknown for
the chance to build a new world with the boy she loves.

Natalie's last summer in her small Kentucky hometown is off to a magical
start... until she starts seeing the "wrong things." They're just momentary
glimpses at first-her front door is red instead of its usual green, there's a
pre-school where the garden store should be. But then her whole town disappears
for hours, fading away into rolling hills and grazing buffalo, and Nat knows
something isn't right.

That's when she gets a visit from the kind but mysterious apparition she calls
"Grandmother," who tells her: "You have three months to save him." The next
night, under the stadium lights of the high school football field, she meets a
beautiful boy named Beau, and it's as if time just stops and nothing exists.
Nothing, except Natalie and Beau.

Emily Henry's stunning debut novel is Friday Night Lights meets The Time
Traveler's Wife, and perfectly captures those bittersweet months after high
school, when we dream not only of the future, but of all the roads and paths
we've left untaken.
"""
_picture = "https://d.gr-assets.com/books/1433990957l/25467698.jpg"
_catalog_id = 10
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


# 012
_user_id = 1
_name = "A Thousand Naked Strangers: A Paramedic's Wild Ride to the Edge and Back "
_author = "Kevin Hazzard"
_description = """
A former paramedic's visceral, poignant, and mordantly funny account of a
decade spent on Atlanta's mean streets saving lives and connecting with the
drama and occasional beauty that lies inside catastrophe.

In the aftermath of 9/11 Kevin Hazzard felt that something was missing from his
life-his days were too safe, too routine. A failed salesman turned local
reporter, he wanted to test himself, see how he might respond to pressure and
danger. He signed up for emergency medical training and became, at age
twenty-six, a newly minted EMT running calls in the worst sections of Atlanta.
His life entered a different realm-one of blood, violence, and amazing grace.

Thoroughly intimidated at first and frequently terrified, he experienced on a
nightly basis the adrenaline rush of walking into chaos. But in his downtime,
Kevin reflected on how people's facades drop away when catastrophe strikes. As
his hours on the job piled up, he realized he was beginning to see into the
truth of things. There is no pretense five beats into a chest compression, or
in an alley next to a crack den, or on a dimly lit highway where cars have
collided. Eventually, what had at first seemed impossible happened: Kevin
acquired mastery. And in the process he was able to discern the professional
differences between his freewheeling peers, what marked each-as he termed
them-as "a tourist," "true believer," or "killer."

Combining indelible scenes that remind us of life's fragile beauty with
laugh-out-loud moments that keep us smiling through the worst, A Thousand Naked
Strangers is an absorbing read about one man's journey of self-discovery-a trip
that also teaches us about ourselves.
"""
_picture = "https://d.gr-assets.com/books/1451843171l/25111005.jpg"
_catalog_id = 3
item = Item(user_id=_user_id, name=_name, author=_author, description=_description, picture=_picture, catalog_id=_catalog_id)
db_session.add(item)


db_session.commit()
print "Titles are added!"
