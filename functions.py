from datetime import datetime

import mysql.connector
from kivy.properties import Clock
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker
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
            query = "SELECT cpf, senha, nome, id FROM usuarios WHERE cpf = %s"

            # Execute a consulta SQL apenas com o CPF
            cursor.execute(query, (cpf,))
            resultado = cursor.fetchone()

            # Verifique se o usuário foi encontrado e se a senha está correta
            if resultado:
                cpf_banco, senha_banco, nome_usuario, id_usuario = resultado
                if senha == senha_banco:
                    self.ids.lblogin.text = "Logado com sucesso! Redirecionando para a tela inicial..."
                    self.cpf_usuario_logado = cpf_banco
                    self.nome_usuario_logado = nome_usuario
                    self.id_usuario_logado = id_usuario
                    self.senha_usuario_logado = senha_banco
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


def change_about(self, novo_nome, novo_cpf, nova_senha):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        # Construa a consulta SQL para atualizar os campos nome, cpf e senha
        query = "UPDATE usuarios SET nome = %s, cpf = %s, senha = %s WHERE cpf = %s"

        # Execute a consulta SQL para atualizar os campos nome, cpf e senha
        cursor.execute(query, (novo_nome, novo_cpf, nova_senha, novo_cpf))

        # Commit a transação
        connect.commit()

    except mysql.connector.Error as error:
        print("Erro ao fazer a atualização dos dados do usuário:", error)
        # Aqui você pode manipular o erro de alguma forma, como exibir uma mensagem para o usuário


def change_about(self, nome, cpf, senha):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if cpf == "":
            self.ids.lbchange.text = "Insira um CPF valido"
        elif nome == "":
            self.ids.lbchange.text = "Insira um novo nome"
        elif senha == "":
            self.ids.lbchange.text = "Insira uma nova Senha"
        elif len(senha) < 10:
            self.ids.lbchange.text = "Senha precisa de pelo menos 10 caracteres"
        else:
            # Construa a consulta SQL para atualizar as informações do usuário
            query = "UPDATE usuarios SET nome = %s, cpf = %s, senha = %s WHERE cpf = %s"

            # Execute a consulta SQL
            cursor.execute(query, (nome, cpf, senha, cpf))
            connect.commit()

    except mysql.connector.Error as error:
        print("Erro ao fazer troca de senha", error)
        self.ids.lbredfsenha.text = "Erro ao fazer troca de senha, cpf incorreto"

def patient_register(self, nome2, cpf2):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if nome2 == "":
            self.ids.lbregister_pacient.text = "Insira nome"

        elif cpf2 == "":
            self.ids.lbregister_pacient.text = "Insira CPF"

        elif len(cpf2) < 11:
            self.ids.lbregister_pacient.text = "CPF inválido, tente novamente"

        else:
            query = "INSERT INTO Pacientes (nome, cpf) VALUES (%s, %s)"
            data = (nome2, cpf2)

            cursor.execute(query, data)
            connect.commit()
            self.ids.lbregister_pacient.text = "paciente registrado com sucesso"

    except mysql.connector.Error as error:
        self.ids.lbregister_pacient.text = "Erro ao inserir paciente. Por favor, tente novamente mais tarde."


def callbackplantao(self, *args):
  MDApp.get_running_app().root.current = 'login'

def on_save3(self, instance, value, date_range):
    data_inicio = date_range[0].strftime('%Y-%m-%d')
    data_fim = date_range[-1].strftime('%Y-%m-%d')
    self.ids.data2.text = f'{data_inicio} - {data_fim}'

def on_cancel3(self, instance, value):
  self.ids.data2.text = "Você cliclou em cancelar"

def show_data_picker3(self):
  date_dialog = MDDatePicker(mode="range")
  date_dialog.bind(on_save=self.on_save3, on_cancel=self.on_cancel3)
  date_dialog.open()


def create_post_hour(self, cpf_funcionario, data_intervalo, horario, horario2):
    try:
        # Conectar ao banco de dados
        connect = db_connect()
        cursor = connect.cursor()

        # Verificar se o CPF do funcionário está cadastrado
        cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf_funcionario,))
        res = cursor.fetchone()

        if not res:
            self.ids.lbregister_hour.text = "CPF não cadastrado"
        elif not horario:
            self.ids.lbregister_hour.text = "Insira um horário"
        else:

            datas = data_intervalo.split(" - ")
            data_inicio = datetime.strptime(datas[0], '%Y-%m-%d').strftime('%Y-%m-%d')
            data_fim = datetime.strptime(datas[1], '%Y-%m-%d').strftime('%Y-%m-%d')

            # Inserir o novo registro na tabela Plantao

            query = "INSERT INTO plantao (cpf, data_inicio, data_fim, horario_inicio, horario_fim) VALUES (%s, %s, %s, %s, %s)"
            dados = (cpf_funcionario, data_inicio, data_fim, horario, horario2)

            cursor.execute(query, dados)

            connect.commit()
            self.ids.lbregister_hour.text = "Registro realizado com sucesso"

    except mysql.connector.Error as error:
        print("Erro ao inserir registro:", error)
        self.ids.lbregister_hour.text = "Erro ao inserir registro. Por favor, tente novamente mais tarde."
