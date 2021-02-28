# server
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from urllib import parse
# database
from database import Session, engine, Base, discordUser


Base.metadata.create_all(engine)
session = Session()

# Server ------------------------------------

PORT = 80


class StaticServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        filename = 'form.html'

        with open(filename, 'rb') as fh:
            html = fh.read()
            self.wfile.write(html)

    def do_POST(self):
        parsed_path = parse.urlparse(self.path)
        message = parsed_path.query
        code = message[5:]
        content_length = int(self.headers['Content-Length'])
        data_input = bytes.decode(
            self.rfile.read(content_length), 'iso-8859-1')
        print(data_input)
        u = data_input[8:]

        if '&#' in u:
            message = 'O seu username contém caracteres especiais não reconhecidos por este servidor. Pedimos desculpa por este incómodo. Por favor contacte um membro do NEEC de forma a proceder à resolução deste problema.'
            self.send_response(200)

            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

            return

        # contar o número de "#" e guardar a posição do último em pos
        cnt = 0
        pos = -1
        existe = False
        for caracter in u:
            if (caracter == "#"):
                pos = cnt
                existe = True
            cnt += 1    
# or not u[-4:].isdigit()
        
        # cortar a string 4 posições depois do último "#"

        u = u[:(pos + 5)]
    
        print(len(u))

        #se não existir cardinal ou se os 4 últimos caracteres não forem números, o username foi mal inserido
        if not existe or not u[-4:].isdigit():
            message = 'O seu usarname do Discord termina com um # seguido de 4 dígitos. Por favor verifique se escreveu bem e tente novamente.'

            self.send_response(200)

            self.send_header('Content-Type',
                            'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

            return

        # verificar se o tamanho excede 32 caracteres + #1234 = 37

        if (len(u) >= 37 or len(u)< 7):
            message = 'O username que inseriu não é permitido pelo Discord. Por favor verifique se escreveu bem e tente novamente.'

            self.send_response(200)

            self.send_header('Content-Type',
                            'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

            return


        # verificar se já está na database, e eleminá-lo nesse caso
        users = session.query(discordUser).all()
        for x in users:
            # print(len(str(x.discordUsername[:-2])))
            # print(len(str(u[:-2])))
            # print(x.discordUsername)
            if(str(x.discordUsername) == str(u) or str(x.discordUsername) == str(u)):
                print('igual')
                print(x)
                session.delete(x)
                session.commit()

        # print (u)
        #user = discordUser(u, None, None, None, code)
        # session.add(user)
        # session.commit()

        connection = engine.raw_connection()
        cursor = connection.cursor()

        # para encontrar o maior id
        cursor.execute('SELECT id FROM "discordUsers" WHERE id >= all (SELECT id FROM "discordUsers")')
        result = cursor.fetchone()

        for x in result:
            
            
            var = x
            var += 1
            cursor.execute('INSERT INTO "discordUsers" VALUES (%(id)s,%(du)s,%(at)s,%(rt)s,%(te)s,%(fc)s);', {
                                "id": var, "du": u, "at": None, "rt": None, "te": None, "fc": code})
            connection.commit()
            cursor.close()


        

        message = 'Boa! Agora só falta usar o comando !cadeiras e terá acesso a tudo!!'

        self.send_response(200)

        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=StaticServer):
    server_address = ("", PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


while True:
    run()
