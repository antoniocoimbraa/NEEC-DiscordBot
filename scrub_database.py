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

print("Start")
# users2 = session.query(discordUser).filter(
#    discordUser.discordUsername == "teste").all()
# for x in users2:
#    print(x.discordUsername)
#    print(x.access_token)
#    print(x.refresh_token)
#    print(x.token_expires)
#    print(x.first_code)

sql = 'SELECT * FROM "discordUsers" WHERE id=3;'
cursor.execute(sql)
result = cursor.fetchall()
for x in result:
    print(x)
    print("\n")

print("Clean")
print("Formatação MAL")
cursor.execute('SELECT id FROM "discordUsers" EXCEPT (SELECT id FROM "discordUsers" WHERE "discordUsername" like %(parm)s);', {
    "parm": '%#____'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1
    # print("Corrigido")
    # print(x.discordUsername)


print("Formatação correta")
cursor.execute('SELECT id,"discordUsername" FROM "discordUsers" WHERE "discordUsername" like %(parm)s;', {
    "parm": '%#____'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1
print("Finish")

print("\nReparo!")
users = session.query(discordUser).all()
for x in users:
    if (x.id == 5170):
        print(x.id)
        print(x.access_token)
        print(x.refresh_token)
        print(x.token_expires)
        print(x.first_code)
        print("Antes")
        print(x.discordUsername)
        print("Depois")
        print(str(x.discordUsername[:-2]))
        print("Confirmacao")
        print(str(x.discordUsername[:-4]))

print("\nAgora um MAC!")
for x in users:
    if (x.id == 5185):
        print(x.id)
        print(x.access_token)
        print(x.refresh_token)
        print(x.token_expires)
        print(x.first_code)
        print("Antes")
        print(x.discordUsername)
        print("Depois")
        print(str(x.discordUsername[:-2]))
        print("Confirmacao")
        print(str(x.discordUsername[:-4]))

print("\n Nomes inválidos:")
# for x in users:
#    if (len(x.discordUsername) < 7 or len(x.discordUsername) > 37):
#        print("Nome invalido:")
#        print(x.id)

cursor.execute(
    'SELECT id FROM "discordUsers" WHERE LENGTH("discordUsername")<7 OR LENGTH("discordUsername")>37;')
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1

print("Nomes que podemos deixar na db")

cursor.execute(
    'SELECT id,"discordUsername" FROM "discordUsers" WHERE "discordUsername" like %(parm1)s OR "discordUsername" like %(parm2)s ORDER BY id ASC;', {
        "parm1": '%#____', "parm2": '%#____\r\n'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1

print("Nomes A RETIRAR na db")

cursor.execute(
    'SELECT id FROM "discordUsers" EXCEPT (SELECT id FROM "discordUsers" WHERE "discordUsername" like %(parm1)s OR "discordUsername" like %(parm2)s) ORDER BY id ASC;', {
        "parm1": '%#____', "parm2": '%#____\r\n'})
result = cursor.fetchall()
i = 0
for x in result:
    print(i)
    print(x)
    i += 1

# print("APAGAR!")
# i = 0
# print("Total rows are:  ", len(result))
# for x in result:
#    print(i)
#    print("Id: ", x[0])
#    i += 1
#    user = session.query(discordUser).filter(
#        discordUser.id == x[0]).all()
#    for y in user:
#        print("Encontrou: ", y.id)
#    session.query(discordUser).filter(discordUser.id == x[0]).delete()
# session.commit()

# print("Delete")
# user = session.query(discordUser).filter(discordUser.id == 10001).all()
# for y in user:
#    print("Encontrou: ", y.discordUsername)
# session.query(discordUser).filter(discordUser.id == 10001).delete()
# session.commit()

print("Maior id")
cursor.execute(
    'SELECT id FROM "discordUsers" WHERE id >= all (SELECT id FROM "discordUsers")')
result = cursor.fetchone()
for x in result:
    print(x)

print("FIX NOMES")
# cursor.execute('SELECT id,"discordUsername" FROM "discordUsers"')
# result = cursor.fetchall()
# for x in result:
#    print("Antes")
#    print(x)
#    if x[1].endswith('\r\n'):
#        print(len(x[1]))
#        var = x[1]
#        var = var[:-2]
#        print("Depois")
#        print(len(var))

cursor.execute(
    'SELECT * FROM "discordUsers" ORDER BY id ASC')
result = cursor.fetchall()
for x in result:
    print(x)

# print("MODIFICACAO!")
# print("\n\n")
#result = session.query(discordUser).all()
# for x in result:
#    if x.discordUsername.endswith('\r\n'):
#        x.discordUsername = x.discordUsername[:-2]
# session.commit()
# print("\n\n")
# print("NOVO!")
# cursor.execute(
#    'SELECT id,"discordUsername" FROM "discordUsers" ORDER BY id ASC')
#result = cursor.fetchall()
# for x in result:
#    print(x)


# teste = 'Antonio#1234'
# print(len(teste))
# if teste.endswith('\r\n'):
#    teste = teste[:-2]
# print(len(teste))

# teste2 = 'Antonio#1234\r\n'
# print(len(teste2))
# if teste2.endswith('\r\n'):
#    teste2 = teste2[:-2]
# print(len(teste2))


#   if  "EvolutionProject" in x.discordUsername[:-2]:
#      print('hey')
#     print(x.discordUsername)
#    session.delete(x)
#   session.commit()
