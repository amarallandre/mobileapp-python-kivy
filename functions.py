import mysql.connector
from kivy.properties import Clock
from kivymd.app import MDApp



def db_connect():
    connection = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'appmed',
    }

    connect = mysql.connector.connect(**connection)
    return connect


def user_register(self, nome, cpf, senha):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if nome == "":
            self.ids.lbregister.text = "Insira nome"

        elif cpf == "":
            self.ids.lbregister.text = "Insira CPF"

        elif senha == "":
            self.ids.lbregister.text = "Insira Senha"

        elif len(cpf) < 11:
            self.ids.lbregister.text = "CPF inválido, tente novamente"

        elif len(senha) < 10:
            self.ids.lbregister.text = "Senha precisa de pelo menos 10 caracteres"

        else:
            query = "INSERT INTO usuarios (nome, cpf, senha) VALUES (%s, %s, %s)"
            data = (nome, cpf, senha)

            cursor.execute(query, data)
            connect.commit()
            self.ids.lbregister.text = "Usuário registrado com sucesso"

    except mysql.connector.Error as error:
        print("Erro ao inserir usuário:", error)
        self.ids.lbregister.text = "Erro ao inserir usuário. Por favor, tente novamente mais tarde."




def log_in(self, cpf, senha):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if cpf == "":
            self.ids.lblogin.text = "Insira CPF"
        elif senha == "":
            self.ids.lblogin.text = "Insira Senha"
        else:
            # Construa a consulta SQL para verificar as credenciais do usuário
            query = "SELECT cpf, senha, nome FROM usuarios WHERE cpf = %s"

            # Execute a consulta SQL apenas com o CPF
            cursor.execute(query, (cpf,))
            resultado = cursor.fetchone()

            # Verifique se o usuário foi encontrado e se a senha está correta
            if resultado:
                cpf_banco, senha_banco, nome_usuario = resultado
                if senha == senha_banco:
                    self.ids.lblogin.text = "Logado com sucesso! Redirecionando para a tela inicial..."
                    self.nome_usuario_logado = nome_usuario
                    Clock.schedule_once(lambda dt: self.initial_screen(), 3)
                else:
                    self.ids.lblogin.text = "Senha incorreta"
            else:
                self.ids.lblogin.text = "Usuário não encontrado"



    except mysql.connector.Error as error:
        print("Erro ao fazer log-in:", error)
        self.ids.lblogin.text = "Erro ao fazer log-in, usuário ou senha incorretos"


def lost_password(self, senha, cpf):
    cpf_info = self.ids.cpf.text
    new_password = self.ids.new_password.text

    try:
        connect = db_connect()
        cursor = connect.cursor()

        if cpf_info == "":
            self.ids.lbredfsenha.text = "Insira CPF"
        elif new_password == "":
            self.ids.lbredfsenha.text = "Insira Senha"
        elif len(new_password) < 10:
            self.ids.lbredfsenha.text = "Senha precisa de pelo menos 10 caracteres"
        else:
            # Construa a consulta SQL para verificar as credenciais do usuário
            query = "UPDATE usuarios SET senha = %s WHERE cpf = %s"

            # Execute a consulta SQL apenas com o CPF
            cursor.execute(query, (new_password, cpf_info))
            connect.commit()

            if cursor.rowcount > 0:
                self.ids.lbredfsenha.text = "Senha redefinida com sucesso"
            else:
                self.ids.lbredfsenha.text = "CPF não encontrado"

    except mysql.connector.Error as error:
        print("Erro ao fazer troca de senha", error)
        self.ids.lbredfsenha.text = "Erro ao fazer troca de senha, cpf incorreto"

