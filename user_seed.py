from models import User, db, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

User.query.delete()

# create seed users
chan = User(first_name='Jackie', last_name='Chan',
    image_url='https://m.media-amazon.com/images/M/MV5BMTk4MDM0MDUzM15BMl5BanBnXkFtZTcwOTI4MzU1Mw@@._V1_.jpg')
stiller = User(first_name='Ben', last_name='Stiller',
    image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkIpCSN42YT4TosyKMHWYWw2awXpPPKBSBACzviU7tlYbqYdv7')
wilson = User(first_name='Owen', last_name='Wilson',
    image_url='https://www.themoviedb.org/t/p/w300_and_h450_bestv2/op8sGD20k3EQZLR92XtaHoIbW0o.jpg')
alba = User(first_name='Jessica', last_name='Alba',
    image_url='https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcR43x1OlSVXS4fZD0IseZHlGAbygdKOfVgZP6Uthz3yOhbb2Qv8')
liu = User(first_name='Lucy', last_name='Liu',
    image_url='https://www.emmys.com/sites/default/files/styles/bio_pics_detail/public/bios/lucy-liu-ap-450x600.jpg?itok=R_aziYvA')

# add users to session
db.session.add(chan)
db.session.add(stiller)
db.session.add(wilson)
db.session.add(alba)
db.session.add(liu)

db.session.commit()

# create seed posts
chan_post1 = Post(title='The Dangers of Stunts',
    content='Stunts can be very dangerous. One time I broke my foot while doing a stunt. It hurt!',
    user_id=chan.id)
chan_post2 = Post(title='My Buddy, Chris Tucker',
    content='Sometimes you it''s easy to get along with your co-stars, sometimes it''s not. Chris Tucker was one of the most fun persons to work with.',
    user_id=chan.id)
stiller_post1 = Post(title='Meet the Pear Tree',
    content='I love pears, and I decided to plant a pear tree years ago. It now bears fruit every year. Those pears are so sweet!',
    user_id=stiller.id)
stiller_post2 = Post(title='How to Be Funny',
    content='It''s not easy to be funny. It''s best not to try too hard and let your quirks and unique personality shine through.',
    user_id=stiller.id)
wilson_post1 = Post(title='I''m a Cowboy',
    content='I can''t believe I starred in a movie, playing a cowboy in a movie with Jackie Chan. What an experience!',
    user_id=wilson.id)
wilson_post2 = Post(title='My Poor Nose',
    content='Unfortunately, my nose is a bit oddly shaped. It''s because I broke it, but now it is an essential part of my signature look.',
    user_id=wilson.id)
alba_post1 = Post(title='A Dictionary Can Sleep?',
    content='I once played a role in a move called "The Sleeping Dictionary." I never understood the title. A dictionary is just a book. It doesn''t sleep!',
    user_id=alba.id)
alba_post2 = Post(title='Woah, Ben!',
    content='I played a part in a movie with Ben Stiller. He once made a joke that was borderline inappropriate. I said "woah, Ben!"',
    user_id=alba.id)
liu_post1 = Post(title='Skiing Freestyle',
    content='I really like to ski in the winter. I like to ski without poles. I call it "skiing freestyle."',
    user_id=liu.id)
liu_post2 = Post(title='Have a Good Burrito!',
    content='My friend decided to go get a burrito after we had been chatting for a while. I said "have a good burrito!" My other friend who had just entered the room said "that''s an interesting salutation!"',
    user_id=liu.id)

posts = [chan_post1, chan_post2, stiller_post1, stiller_post2, wilson_post1, wilson_post2, alba_post1, alba_post2, liu_post1, liu_post2]

db.session.add_all(posts)
db.session.commit()

# create seed tags
funny = Tag(name='Funny')
fun = Tag(name='fun')
woah = Tag(name='Woah!')                          
huh = Tag(name='Huh?')
risky = Tag(name='Risky')
friends = Tag(name='Friends')
yummy = Tag(name='Yummy')
weird = Tag(name='Weird')
interesting = Tag(name='Interesting')

tags = [funny, fun, woah, huh, risky, friends, yummy, weird, interesting]

db.session.add_all(tags)
db.session.commit()
              
# associate tags with posts                           
chan_post1.tags.extend([woah, risky])                                                                              
chan_post2.tags.extend([friends, fun])
stiller_post1.tags.extend([interesting, yummy])
stiller_post2.tags.extend([funny, interesting])
wilson_post1.tags.extend([woah, fun])
wilson_post2.tags.extend([funny, interesting, weird])
alba_post1.tags.extend([funny, huh])
alba_post2.tags.extend([woah, huh, weird])
liu_post1.tags.extend([risky, interesting])
liu_post2.tags.extend([funny, friends, yummy])

db.session.commit()