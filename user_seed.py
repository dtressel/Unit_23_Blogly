from models import User, db
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