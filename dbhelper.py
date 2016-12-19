import app
from playhouse.migrate import *

db = SqliteDatabase('app/configserver.db')
migrator = SqliteMigrator(db)

#price_field = DecimalField(default=0.0)
#comments_field = TextField(null=True)
#
#with db.transaction():
#	migrate(
#       migrator.drop_column('CustomerOrderProduct','price'),
#       migrator.drop_column('CustomerOrderProduct','comments2'),
#       migrator.add_column('CustomerOrderProduct', 'price', price_field),
#       migrator.add_column('CustomerOrderProduct', 'comments2', comments_field) 
#	)
#
#	for cop in app.models.CustomerOrderProduct:
#		cop.comments2 = cop.comments
#	app.models.CustomerOrderProduct.update()
#
#migrate(
#   migrator.drop_column('CustomerOrderProduct','comments'),
#    migrator.rename_column('CustomerOrderProduct', 'comments2', 'comments')
#)

#migrate(
#	migrator.rename_table('AnonBasket', 'AnonBasket_old'),
#	migrator.rename_table('AnonBasket2','AnonBasket')
#)

with db.transaction():
	migrate(
       migrator.add_column('Template', 'enabled', BooleanField(default=True)),
       migrator.add_column('User', 'lang', TextField(default='en')),
	)
