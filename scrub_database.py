from database import Session, engine, Base, discordUser

Base.metadata.create_all(engine)
session = Session()


# session.query(discordUser).delete()
# session.commit()

users = session.query(discordUser).all()
for x in users:
    if (x.discordUsername == "AntonioC#1021"):
        print (x.discordUsername)
        #session.delete(x)
        #session.commit()



    if  'AntonioC' in x.discordUsername[:-2]:
        print('hey')
        print(x.discordUsername)
        #session.delete(x)
        #session.commit()
    





    # print(x.discordUsername)
    # print(x.access_token)
    # print(x.refresh_token)
    # print(x.token_expires)
