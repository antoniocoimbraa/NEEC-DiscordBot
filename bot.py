# bot.py
import os
import random
import pandas as pd
import json
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs

import fenixedu
import discord
from fenixedu import User
from discord.ext import commands
from dotenv import load_dotenv

#Database
from database import Session, engine, Base, discordUser

Base.metadata.create_all(engine)
session = Session()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv('DISCORD_GUILD')


config = fenixedu.FenixEduConfiguration.fromConfigFile()
fenix_client = fenixedu.FenixEduClient(config)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='!')

id_cadeiras = dict()


@bot.event
async def on_ready():
    print(f'{bot.user} conectou-se ao Discord!')

    meec_server = bot.get_guild(705045833451700254)
    print(f'Estou aqui no {meec_server}')


@bot.event
async def on_member_join(member):
    

    await member.create_dm()
    url = fenix_client.get_authentication_url()
    await member.dm_channel.send(f'Olá {member.name}, Sê bem-vindo ao servidor de MEEC. Clica neste link para aproveitares esta experiência ao máximo! Não te esqueças de inserir o teu username no formato "username#XXXX", com os 4 dígitos associados à tua conta!!!')
    await member.dm_channel.send(url)
    await member.dm_channel.send('Depois de te registares, dirige-te ao canal #bot-commands e insere o comando `!cadeiras` para teres acesso aos teus canais!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Não tens o cargo necessário para usar este comando.')



@bot.command(name='new_url', help='Este comando envia por mensagem direta um novo link de autenticação do Fénix')
async def get_new_url(ctx):
    message = ctx.message
    await message.delete(delay=None)
    member = ctx.author   
    await member.create_dm()
    url = fenix_client.get_authentication_url()
    await member.dm_channel.send(f'Olá {member.name}, segue este link para concluíres a tua autenticação')
    await member.dm_channel.send(url)



@bot.command(name='cadeiras', help='Este comando dá-te acesso aos canais das cadeiras nas quais estás inscrito.')
async def cadeiras(ctx):
    print("oi")

    #delete da mensagem e ir buscar o autor do comando
    message = ctx.message
    await message.delete(delay=None)

    member = ctx.author   
    users = session.query(discordUser).all()
    print(member)
  
    for x in users:
        if(str(x.discordUsername) == str(member)):
            print("Estás na base de dados")

            #verificar se já existe este discordUsername já tem codigos de acesso na Database
            if x.access_token != None:
                print('tens tokens')
                #ou seja, se já tiver criado o seu user do fénix, tenho que usar esses códigos para criar novo objeto user

                r = requests.post(f'https://fenix.tecnico.ulisboa.pt/oauth/refresh_token?client_id=1132965128044744&client_secret=UceVvflDH0knsARwostsUag1w/UqU5Y8LCKTs2u5aX1Zwa0BcLdSkPpapR7XxbYMyP2MCpZVJ2VKz3Ui1w4yGg==&refresh_token={x.refresh_token}&grant_type=refresh_token')
                res = json.loads(r.text)
                print(res)
                user = User(res['access_token'], x.refresh_token, res['expires_in'])
                print(user)

                x.access_token = res['access_token']
                x.token_expires = res['expires_in']
                session.commit()


                
                curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)
                person = fenix_client.get_person(user)
    
                # verificar se a pessoa pertence ao curso de MEEC
                belongs = False
                for m in range(len(curriculum)):
                    if curriculum[m]['degree']['acronym'] == "MEEC":
                        belongs = True
                if not belongs:
                    channel = bot.get_channel(705090002261901332)
                    await channel.send(f"{member} não é de MEEC... vai levar facada ఠ_ఠ")
                    await member.create_dm()
                    await member.dm_channel.send("O seu usuário do fénix não está inscrito como aluno no curso de MEEC no IST\nFoi enviada uma notificação aos membros do NEECIST, e entraremos em contacto consigo o mais rapidamente possível.")
                    return
                

                guild = ctx.guild
                roles = guild.roles
                table = pd.read_csv('cadeiras_acronimos.csv')

            
                #remover cadeiras do semestre passado
                for kk in range(len(table['Acronimo usado na guild'])):
                    for role in ctx.message.author.roles:
                        if (table['Acronimo usado na guild'][kk]) == str(role):
                            await member.remove_roles(role, reason=None, atomic=True)
                            
                #dar os roles pedidos            
                for i in range(len(cadeiras['enrolments'])):
                    for k in range(len(table['Nome da cadeira'])):
                        if table['Nome da cadeira'][k] == "Empreendedorismo, Inovação e Transferência de Tecnologia":
                            print("vamoooos")
                        if cadeiras['enrolments'][i]['name'] == table['Nome da cadeira'][k]:
                            await member.create_dm()
                            await member.dm_channel.send('Concedido acesso a ' + table['Acronimo usado na guild'][k])
                            for j in range(len(roles)):
                                if roles[j].name == table['Acronimo usado na guild'][k]:
                                    await member.add_roles(roles[j], reason=None, atomic=True)
                #dar o role de AComp
                for i in range(len(cadeiras['attending'])):
                    if (cadeiras['attending'][i]['name']) == "Arquitectura de Computadores":
                        await member.create_dm()
                        await member.dm_channel.send("Concedido acesso a AComp")
                        for j in range(len(roles)):
                            if roles[j].name == "AComp":
                                await member.add_roles(roles[j], reason=None, atomic=True)


                for l in range(len(roles)):
                    if (curriculum[0]['start'][-2:] == roles[l].name[:2]):
                        await member.create_dm()
                        await member.dm_channel.send('Concedido acesso a ' + roles[l].name)
                        await member.add_roles(roles[l], reason=None, atomic=True)
                        break
                for p in range(len(roles)):
                    if roles[p].name == "NovoMembro":
                        await member.remove_roles(roles[p], reason=None, atomic=True)
                        break
                string = person['displayName']
                split = string.split()
                substring = split[0] + " " + split[-1]
                await member.edit(nick=substring)
                await member.create_dm()
                await member.dm_channel.send('Parabéns!!! As tuas cadeiras foram adicionadas com sucesso!')
                await member.dm_channel.send('Se desejas ser removido de algum canal destas cadeiras,  usa o comando "!remove" seguido do acrónimo da respetiva cadeira.')

                return



            else:

                print("Não tens tokens")
                #ou seja, se tiver de ir criar user no fénix
                #vai ser criado o user e guardados os valores na base de dados
                # valores a ser guardados - 'access_token' 'refresh_token' 'expires_in'

                
                code = str(x.first_code)
                r = requests.post(f"https://fenix.tecnico.ulisboa.pt/oauth/access_token?client_id=1132965128044744&client_secret=UceVvflDH0knsARwostsUag1w/UqU5Y8LCKTs2u5aX1Zwa0BcLdSkPpapR7XxbYMyP2MCpZVJ2VKz3Ui1w4yGg==&redirect_uri=http://51.132.30.72:80/&code={code}&grant_type=authorization_code")
                
                res = json.loads(r.text)
                print(res)
                user = User(res['access_token'], res['refresh_token'], res['expires_in'])
                print(user)
                curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)
                person = fenix_client.get_person(user)

                #guardar info na database
                x.access_token = res['access_token']
                x.refresh_token = res['refresh_token']
                x.token_expires = res['expires_in']
                session.commit()

                 # verificar se a pessoa pertence ao curso de MEEC
                belongs = False
                for m in range(len(curriculum)):
                    if curriculum[m]['degree']['acronym'] == "MEEC":
                        belongs = True
                if not belongs:
                    channel = bot.get_channel(705090002261901332)
                    await channel.send(f"{member} não é de MEEC... vai levar facada ఠ_ఠ")
                    await member.create_dm()
                    await member.dm_channel.send("O seu usuário do fénix não está inscrito como aluno no curso de MEEC no IST\nFoi enviada uma notificação aos membros do NEECIST, e entraremos em contacto consigo o mais rapidamente possível.")
                    return

                #print(x.access_token)
                guild = ctx.guild
                roles = guild.roles

                table = pd.read_csv('cadeiras_acronimos.csv')

                #remover cadeiras do semestre passado
                for kk in range(len(table['Acronimo usado na guild'])):
                    for role in ctx.message.author.roles:
                        if (table['Acronimo usado na guild'][kk]) == str(role):
                            await member.remove_roles(role, reason=None, atomic=True)

                            
                for i in range(len(cadeiras['enrolments'])):
                    for k in range(len(table['Nome da cadeira'])):
                        if cadeiras['enrolments'][i]['name'] == table['Nome da cadeira'][k]:
                            await member.create_dm()
                            await member.dm_channel.send('Concedido acesso a ' + table['Acronimo usado na guild'][k])
                            for j in range(len(roles)):
                                if roles[j].name == table['Acronimo usado na guild'][k]:
                                    await member.add_roles(roles[j], reason=None, atomic=True)
                #dar o role de AComp
                for i in range(len(cadeiras['attending'])):
                    if (cadeiras['attending'][i]['name']) == "Arquitectura de Computadores":
                        await member.create_dm()
                        await member.dm_channel.send("Concedido acesso a AComp")
                        for j in range(len(roles)):
                            if roles[j].name == "AComp":
                                await member.add_roles(roles[j], reason=None, atomic=True)
                for l in range(len(roles)):
                    if (curriculum[0]['start'][-2:] == roles[l].name[:2]):
                        await member.create_dm()
                        await member.dm_channel.send('Concedido acesso a ' + roles[l].name)
                        await member.add_roles(roles[l], reason=None, atomic=True)
                        break
                for p in range(len(roles)):
                    if roles[p].name == "NovoMembro":
                        await member.remove_roles(roles[p], reason=None, atomic=True)
                        break
                
                string = person['displayName']
                split = string.split()
                substring = split[0] + " " + split[-1]
                await member.edit(nick=substring)
                await member.create_dm()
                await member.dm_channel.send('Parabéns!!! As tuas cadeiras foram adicionadas com sucesso!')
                await member.dm_channel.send('Se desejas ser removido de algum canal destas cadeiras,  usa o comando "!remove" seguido do acrónimo da respetiva cadeira')
                return

    #se chegar aqui significa que a autenticação não foi bem conseguida     

    url = fenix_client.get_authentication_url()
    await member.create_dm()
    await member.dm_channel.send('O teu username do Discord não foi registado corretamente. Verifica se escreveste bem. Usa o seguinte link para tentares novamente\nAtenção: Se mudaste recentemente o teu username do Discord, tens que fazer a autenticação de novo!!')
    await member.dm_channel.send(url)

    channel = bot.get_channel(813909050923941938)
    await channel.send(f"{member.mention} não conseguiu autenticar-se :(")

    return






@bot.command(name='remove', help='Este comando retira-te o cargo associado a uma cadeira')
async def remove_cadeira(ctx, *args):
    message = ctx.message
    await message.delete(delay=None)
    guild = ctx.guild
    roles = guild.roles
    member = ctx.author
    for i in range(len(roles)):
        if len(args) == 1:
            acronimo = str(args[0])
            if roles[i].name == acronimo:
                await member.remove_roles(roles[i], reason=None, atomic=True)
                await member.create_dm()
                await member.dm_channel.send(f'Foste removido do canal de {acronimo}.')
                return
        elif len(args) == 2:
            acronimo = str(args[0]) +' '+ str(args[1])
            if roles[i].name == acronimo:
                await member.remove_roles(roles[i], reason=None, atomic=True)
                await member.create_dm()
                await member.dm_channel.send(f'Foste removido do canal de {acronimo}.')
                return
            
            
    await member.create_dm()
    await member.dm_channel.send(f'Verifica se escreveste bem o acrónimo da cadeira')


########################################################################### Experimental ###################################################################################################

# @bot.command(name='teste2', help='Este comando dá-te acesso aos canais das cadeiras nas quais estás inscrito.')
# async def teste2(ctx):
#     print("oi")

#     #delete da mensagem e ir buscar o autor do comando
#     message = ctx.message
#     await message.delete(delay=None)

#     member = ctx.author   
#     users = session.query(discordUser).all()
#     print(member)
  
#     for x in users:
#         if(str(x.discordUsername) == str(member)):
#             print("Estás na base de dados")

#             #verificar se já existe este discordUsername já tem codigos de acesso na Database
#             if x.access_token != None:
#                 print('tens tokens')
#                 #ou seja, se já tiver criado o seu user do fénix, tenho que usar esses códigos para criar novo objeto user

#                 r = requests.post(f'https://fenix.tecnico.ulisboa.pt/oauth/refresh_token?client_id=1132965128044744&client_secret=UceVvflDH0knsARwostsUag1w/UqU5Y8LCKTs2u5aX1Zwa0BcLdSkPpapR7XxbYMyP2MCpZVJ2VKz3Ui1w4yGg==&refresh_token={x.refresh_token}&grant_type=refresh_token')
  
#                 res = json.loads(r.text)
#                 user = User(res['access_token'], x.refresh_token, res['expires_in'])

#                 x.access_token = res['access_token']
#                 x.token_expires = res['expires_in']
#                 session.commit()

#                 print(r)
#                 print(user)

                
#                 # curriculum = fenix_client.get_person_curriculum(user)
#                 # print(curriculum)
#                 # print("\n\n")
#                 cadeiras = fenix_client.get_person_courses(user)
#                 print(cadeiras)
#                 print("\n\n")

#                 for i in range(len(cadeiras['attending'])):
#                     print(cadeiras['attending'][i]['name'])

#                 person = fenix_client.get_person(user)
#                 print(person)
#                 print("\n\n")
#                 aulas = fenix_client.get_person_classes(user)
#                 print(aulas)
#                 print("\n\n")
#                 avaliacoes = fenix_client.get_person_evaluations_calendar(user)
#                 print(avaliacoes)
#                 print("\n\n")   
#                 print("end")

@bot.command()
@commands.has_role('Admin')
async def auth(ctx):
    print("lets start")

    #delete da mensagem
    message = ctx.message
    await message.delete(delay=None)

    guild = ctx.guild

    users = session.query(discordUser).all()
    # members = message.guild.members
    
    users = session.query(discordUser).all()
    print(users.discordUsername)
 


    async for member in guild.fetch_members(limit=None):
        if member.name in users.discordUsername:
            print(f"{member.name} está na base de dados")



    print("end")










@bot.command()
@commands.has_role('Admin')
async def escreve(ctx):
    print("lets start")

    #delete da mensagem
    message = ctx.message
    await message.delete(delay=None)

    guild = ctx.guild

    acomp_students = 0
    role = discord.utils.find(lambda r: r.name == "AComp", guild.roles)
    f = open("alunos_de_acomp.txt", "w")
    f.write(f"Lista de alunos com o role de AComp:\n\n")
    async for member in guild.fetch_members(limit=None):
        if role in member.roles:
            if member.nick != None:
                print(member.nick)
                acomp_students += 1
                f.write(f"{member.nick}\n")
            else:
                print(str(member)[:-5])
                acomp_students += 1
                f.write(f"{str(member)[:-5]}\n")
    
    f.write(f"\n\nTotal de alunos com o role de AComp: {acomp_students}")
    print(acomp_students)






bot.run(TOKEN)
