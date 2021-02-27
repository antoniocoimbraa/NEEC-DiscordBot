from database import Session, engine, Base, discordUser
from sqlalchemy import insert
from sqlalchemy.sql import text

Base.metadata.create_all(engine)
session = Session()


# session.query(discordUser).delete()
# session.commit()
u = "teste2"
code = 3
connection = engine.raw_connection()
cursor = connection.cursor()

# users = session.query(discordUser).all()
# for x in users:
#    print(x.discordUsername)

print("Delete")
# session.query(discordUser).filter(
#    discordUser.id == "teste").delete()
print("Start")
# users2 = session.query(discordUser).filter(
#    discordUser.discordUsername == "teste").all()
# for x in users2:
#    print(x.discordUsername)
#    print(x.access_token)
#    print(x.refresh_token)
#    print(x.token_expires)
#    print(x.first_code)

sql = 'SELECT * FROM "discordUsers" WHERE id=5297;'
cursor.execute(sql)
result = cursor.fetchall()
for x in result:
    print(x)
    print("\n")


# result = cursor.execute(
#    'INSERT INTO "discordUsers" VALUES (%(id)s,%(du)s,%(at)s,%(rt)s,%(te)s,%(fc)s);', {"id": 10001, "du": u, "at": None, "rt": None, "te": None, "fc": code})
# connection.commit()
# cursor.close()

# row = cursor.fetchone()
# for x in result:
#    print(x.discordUsername)
print("Step2")
# , {"discordUsername": u, "access_token": None,"refresh_token": None, "token_expires": None, "first_code": code})
# session.add(user)
# session.commit()
users = session.query(discordUser).all()
for x in users:
    if (x.discordUsername == "teste2"):
        print(x.id)
        print(x.discordUsername)
        print(x.access_token)
        print(x.refresh_token)
        print(x.token_expires)
        print(x.first_code)

print("Clean")
print("Formatação MAL")
cursor.execute('SELECT "discordUsername" FROM "discordUsers" EXCEPT (SELECT "discordUsername" FROM "discordUsers" WHERE "discordUsername" like %(parm)s);', {
    "parm": '%#____'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1


print("Formatação correta")
cursor.execute('SELECT "discordUsername" FROM "discordUsers" WHERE "discordUsername" like %(parm)s;', {
    "parm": '%#____'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(":")
    print(x)
    print("\n")
    i += 1
print("Finish")
#    # if (x.discordUsername == "GoddessAsuna#7207"):
#         print (x.discordUsername)
#         print (x.access_token)
#         print (x.refresh_token)
#         print (x.token_expires)
#         print (x.first_code)
#    # if (x.discordUsername == "Beatrizpereira#1842"):
#    print (x.discordUsername)
# print (x.access_token)
# print (x.refresh_token)
# print (x.token_expires)
# print (x.first_code)

#   if  "EvolutionProject" in x.discordUsername[:-2]:
#      print('hey')
#     print(x.discordUsername)
#    session.delete(x)
#   session.commit()

# print(x.discordUsername)
# print(x.access_token)
# print(x.refresh_token)
# print(x.token_expires)
