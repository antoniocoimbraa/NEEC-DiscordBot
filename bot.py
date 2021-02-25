4# bot.py
import os
import random
import pandas as pd
import json
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs

import fenixedu
from fenixedu import User
from discord.ext import commands
from dotenv import load_dotenv

#Database
from database import Session, engine, Base, discordUser

Base.metadata.create_all(engine)
session = Session()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#print(TOKEN)
GUILD = os.getenv('DISCORD_GUILD')
#GUILD = os.getenv('CLIENT_SECRET')

config = fenixedu.FenixEduConfiguration.fromConfigFile()
fenix_client = fenixedu.FenixEduClient(config)

bot = commands.Bot(command_prefix='!')

id_cadeiras = dict()


@bot.event
async def on_ready():
    print(f'{bot.user} conectou-se ao Discord!')


@bot.event
async def on_member_join(member):
    

    await member.create_dm()
    url = fenix_client.get_authentication_url()
    await member.dm_channel.send(f'Olá {member.name}, Sê bem-vindo ao servidor de MEEC. Clica neste link para aproveitares esta experiência ao máximo! Não te esqueças de inserir o teu username no formato "username#XXXX", com os 4 dígitos associados à tua conta!!!')
    await member.dm_channel.send(url)
    await member.dm_channel.send('Depois de te registares, dirige-te ao canal #bot-commands e insere o comando "!cadeiras" para teres acesso aos teus canais!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


#@bot.command(name='rola_dado', help='Simulates rolling dice.')
#async def roll(ctx, number_of_dice: int, number_of_sides: int):
   # dice = [
     #   str(random.choice(range(1, number_of_sides + 1)))
     #   for _ in range(number_of_dice)
   # ]
   # await ctx.send(', '.join(dice))


# @bot.command(name='horário', help='Este comando vai buscar o Horário da cadeira onde for escrito e envia o a quem pediu.')
# async def course_schedule(ctx, acronym):
#     message = ctx.message
#     await message.delete(delay=None)
#     id = id_cadeiras[acronym]
#     horario = fenix_client.get_course_schedule(id)
#     my_lst_str = ' '.join(map(str, horario['courseLoads']))
#     print(my_lst_str)
#     await ctx.send(my_lst_str)


# @bot.command(name='avaliações', help='Este comando vai buscar o Horário da cadeira onde for escrito e envia o a quem pediu.')
# async def course_evaluations(ctx, acronym):
#     member = ctx.author
#     message = ctx.message
#     await message.delete(delay=None)
#     id = id_cadeiras[acronym]
#     testes = fenix_client.get_course_evaluations(id)
#     await member.create_dm()
#     for i in range(len(testes)):
#         if testes[i]['evaluationPeriod']['end'] != '':
#             await member.dm_channel.send(testes[i]['name'])
#             await member.dm_channel.send(testes[i]['evaluationPeriod'])


# @bot.command(name='config', help='Este comando vai buscar as cadeiras de um certo curso e guarda as para uso posterior.')
# async def config1(ctx, find_curso):
#     member = ctx.author
#     cursos = fenix_client.get_degrees()
#     for i in range(len(cursos)):
#         if cursos[i]['acronym'] == find_curso:
#             id = cursos[i]['id']
#             name = cursos[i]['name']
#     await ctx.send(name)
#     await ctx.send('Id: ' + id)
#     cadeiras = fenix_client.get_degree_courses(id)
#     #await member.create_dm()
#     for i in range(len(cadeiras)):
#         id_cadeiras[cadeiras[i]['acronym']] = cadeiras[i]['id']
#         await member.dm_channel.send(cadeiras[i]['name'] + ' (' + cadeiras[i]['acronym'] + ') ' + '->Id: ' + cadeiras[i]['id'])


@bot.command(name='new_url', help='Este comando envia por mensagem direta um novo link de autenticação do Fénix')
async def get_new_url(ctx):
    message = ctx.message
    await message.delete(delay=None)
    member = ctx.author   
    await member.create_dm()
    url = fenix_client.get_authentication_url()
    await member.dm_channel.send(f'Olá {member.name}, segue este link para concluíres a tua autenticação')
    await member.dm_channel.send(url)





   
# @bot.command(name='teste1', help='Comando de teste')
# async def dbtests(ctx):
#     message = ctx.message
#     await message.delete(delay=None)
#     guild = ctx.guild
#     member = ctx.author
#     users = session.query(discordUser).all()
#     for x in users:
#         if (str(x.discordUsername[:-2]) == str(member)):
#             r = requests.post(f'https://fenix.tecnico.ulisboa.pt/oauth/refresh_token?client_id=1132965128044744&client_secret=UceVvflDH0knsARwostsUag1w/UqU5Y8LCKTs2u5aX1Zwa0BcLdSkPpapR7XxbYMyP2MCpZVJ2VKz3Ui1w4yGg==&refresh_token={x.refresh_token}&grant_type=refresh_token')
#             res = json.loads(r.text)
#             user = User(res['access_token'], x.refresh_token, res['expires_in'])
#             x.access_token = res['access_token']
#             x.token_expires = res['expires_in']
#             session.commit()

#             person = fenix_client.get_person(user)
#             string = person['displayName']
#             split = string.split()
#             substring = split[0] + " " + split[-1]
#             print(substring)
#             await member.edit(nick=substring)
            






#             #verificar se já existe este discordUsername já tem codigos de acesso na Database
#             if x.access_token != None:
#                 #print('tens tokens')
#                 #ou seja, se já tiver criado o seu user do fénix, tenho que usar esses códigos para criar novo objeto user
#                 user = User(x.access_token, x.refresh_token, x.token_expires)
#                 person = fenix_client.get_person(user)
#                 string = person['name']
#                 ist_id = person['username']
#                 split = string.split()
#                 substring = split[0] + split[len(split)-1] + '(' + ist_id + ')'
#                 await member.edit(nick=substring)
#                 return
#     print('não deu')
                # name = str(fenix_client.get_person(user)['displayName'])
                # istID = str(fenix_client.get_person(user)['usernamename'])
                # print('olá')

                # await member.edit(nick=(f'{name} {istID}'))
    # for j in range(len(roles)):
    #     if roles[j].name == "NovoMembro":
    #         await member.remove_roles(roles[j], reason=None, atomic=True)





@bot.command(name='cadeiras', help='Este comando dá-te acesso aos canais das cadeiras nas quais estás inscrito.')
async def cadeiras(ctx):
    #delete da mensagem e ir buscar o autor do comando
    message = ctx.message
    await message.delete(delay=None)

    member = ctx.author   
    users = session.query(discordUser).all()
    for x in users:
        if(str(x.discordUsername[:-2]) == str(member)):
            print("Estás na base de dados")

            #verificar se já existe este discordUsername já tem codigos de acesso na Database
            if x.access_token != None:
                print('tens tokens')
                #ou seja, se já tiver criado o seu user do fénix, tenho que usar esses códigos para criar novo objeto user

                r = requests.post(f'https://fenix.tecnico.ulisboa.pt/oauth/refresh_token?client_id=1132965128044744&client_secret=UceVvflDH0knsARwostsUag1w/UqU5Y8LCKTs2u5aX1Zwa0BcLdSkPpapR7XxbYMyP2MCpZVJ2VKz3Ui1w4yGg==&refresh_token={x.refresh_token}&grant_type=refresh_token')
  
                res = json.loads(r.text)
                user = User(res['access_token'], x.refresh_token, res['expires_in'])

                x.access_token = res['access_token']
                x.token_expires = res['expires_in']
                session.commit()


                
                curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)
                person = fenix_client.get_person(user)
    
    

                
                guild = ctx.guild
                roles = guild.roles
                table = pd.read_csv('cadeiras_acronimos.csv')

            
                #remover cadeiras do semestre passado
                for kk in range(len(table['Acronimo usado na guild'])):
                    for role in ctx.message.author.roles:
                        print(str(role))
                        if (table['Acronimo usado na guild'][kk]) == str(role):
                            await member.remove_roles(role, reason=None, atomic=True)
                            
                #dar os roles pedidos            
                for i in range(len(cadeiras['enrolments'])):
                    for k in range(len(table['Nome da cadeira'])):
                        if cadeiras['enrolments'][i]['name'] == table['Nome da cadeira'][k]:
                            await member.create_dm()
                            await member.dm_channel.send('Concedido acesso a ' + table['Acronimo usado na guild'][k])
                            for j in range(len(roles)):
                                if roles[j].name == table['Acronimo usado na guild'][k]:
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
                user = User(res['access_token'], res['refresh_token'], res['expires_in'])
                #print(user)
                curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)
                person = fenix_client.get_person(user)

                #guardar info na database
                x.access_token = res['access_token']
                x.refresh_token = res['refresh_token']
                x.token_expires = res['expires_in']
                session.commit()
                #print(x.access_token)
                guild = ctx.guild
                roles = guild.roles

                table = pd.read_csv('cadeiras_acronimos.csv')
                for i in range(len(cadeiras['enrolments'])):
                    for k in range(len(table['Nome da cadeira'])):
                        if cadeiras['enrolments'][i]['name'] == table['Nome da cadeira'][k]:
                            await member.create_dm()
                            await member.dm_channel.send('Concedido acesso a ' + table['Acronimo usado na guild'][k])
                            for j in range(len(roles)):
                                if roles[j].name == table['Acronimo usado na guild'][k]:
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
                    
    url = fenix_client.get_authentication_url()
    await member.create_dm()
    await member.dm_channel.send('O teu username do Discord não foi registado corretamente. Verifica se escreveste bem. Usa o seguinte link para tentares novamente')
    await member.dm_channel.send(url)
    return


@bot.command(name='remove', help='Este comando retira-te o acesso ao canal de uma cadeira')
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



bot.run(TOKEN)
