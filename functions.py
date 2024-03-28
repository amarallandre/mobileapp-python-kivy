from datetime import datetime
import threading
from kivy.clock import Clock, mainthread
import mysql.connector
from kivy.properties import Clock
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp


lista2 = []
HORARIOS_SELECIONADOS = []

# Conexão com database MYSQl
def db_connect():
    connection = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'appmed',
    }

    connect = mysql.connector.connect(**connection)
    return connect

# Função de registro de usuario
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



# Função login
def log_in(self, cpf, senha):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if cpf == "":
            self.ids.lblogin.text = "Insira CPF"
        elif senha == "":
            self.ids.lblogin.text = "Insira Senha"
        else:
            query = "SELECT cpf, senha, nome, id FROM usuarios WHERE cpf = %s"

            cursor.execute(query, (cpf,))
            resultado = cursor.fetchone()

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

# Função esqueceu sua senha
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
            query = "UPDATE usuarios SET senha = %s WHERE cpf = %s"

            cursor.execute(query, (new_password, cpf_info))
            connect.commit()

            if cursor.rowcount > 0:
                self.ids.lbredfsenha.text = "Senha redefinida com sucesso"
            else:
                self.ids.lbredfsenha.text = "CPF não encontrado"


    except mysql.connector.Error as error:
        print("Erro ao fazer troca de senha", error)
        self.ids.lbredfsenha.text = "Erro ao fazer troca de senha, cpf incorreto"

# função de trocar as informaçoes na dashboard ja logado
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


# Função registrar paciente
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

# Função voltar para tela de login
def callbackplantao(self, *args):
  MDApp.get_running_app().root.current = 'login'

# Função salvar data selecionada através do calendario(Plantão)
def on_save3(self, instance, value, date_range):
    data_inicio = date_range[0].strftime('%Y-%m-%d')
    data_fim = date_range[-1].strftime('%Y-%m-%d')
    self.ids.data2.text = f'{data_inicio} - {data_fim}'

# Função que fecha o calendario(Plantão)
def on_cancel3(self, instance, value):
  self.ids.data2.text = "Você cliclou em cancelar"

# Função de abrir o calendario(Plantão)
def show_data_picker3(self):
  date_dialog = MDDatePicker(mode="range")
  date_dialog.bind(on_save=self.on_save3, on_cancel=self.on_cancel3)
  date_dialog.open()

# Função de salvar o plantão na database
def create_post_hour(self, cpf_funcionario, data_intervalo, horario, horario2):
    try:
        # Conectar ao banco de dados
        connect = db_connect()
        cursor = connect.cursor()

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

            query = "INSERT INTO plantao (cpf, data_inicio, data_fim, horario_inicio, horario_fim) VALUES (%s, %s, %s, %s, %s)"
            dados = (cpf_funcionario, data_inicio, data_fim, horario, horario2)

            cursor.execute(query, dados)

            connect.commit()
            self.ids.lbregister_hour.text = "Registro realizado com sucesso"

    except mysql.connector.Error as error:
        print("Erro ao inserir registro:", error)
        self.ids.lbregister_hour.text = "Erro ao inserir registro. Por favor, tente novamente mais tarde."

# Função que cria os medicamentos e salva na database
def create_post_meds(self, nome_med, quantidade, id_med):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if nome_med == "":
            self.ids.lbmeds.text = "Insira medicamento"
        elif quantidade == "":
            self.ids.lbmeds.text = "Insira quantidade maior que 0"
        elif id_med == "":
            self.ids.lbmeds.text = "Insira o id do med"
        else:
            query = "INSERT INTO medicamentos (nome, quantidade, id_meds) VALUES (%s, %s, %s)"
            dados = (nome_med, quantidade, id_med)

            cursor.execute(query, dados)

            connect.commit()
            self.ids.lbmeds.text = "Registro realizado com sucesso"


    except mysql.connector.Error as error:
        print("Erro ao inserir registro:", error)
        self.ids.lbmeds.text = "Erro ao inserir registro. Por favor, tente novamente mais tarde."


# Função de remover mmedicamentos da database
def create_delete(self, nome_med, quantidade, id_med):
    quantidade = int(quantidade)
    try:
        connect = db_connect()
        cursor = connect.cursor()

        if nome_med == "":
            self.ids.lbmeds.text = "Insira um nome valido"
        elif quantidade == "":
            self.ids.lbmeds.text = "Insira uma quantidade válida"
        elif id_med == "":
            self.ids.lbmeds.text = "Insira o ID do medicamento"
        else:
            query = "UPDATE medicamentos SET quantidade = %s WHERE id_meds = %s"
            dados = (quantidade, id_med)

            cursor.execute(query, dados)
            connect.commit()
            self.ids.lbmeds.text = "Quantidade atualizada com sucesso"

    except mysql.connector.Error as error:
        print("Erro ao atualizar quantidade:", error)
        self.ids.lbmeds.text = "Erro ao atualizar quantidade. Por favor, tente novamente mais tarde."


stop = threading.Event()

def on_stop(self):
    self.stop.set()

def on_enter(self):
    self.start_second_thread()

def start_second_thread(self):
    threading.Thread(target=self.load_data).start()


# Pega as informações da database mostra como uma tabela nna screen
def load_data(self, *args):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM medicamentos')
        data = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        values = [list(row) for row in data]

        self.data_table(cols, values)

    except mysql.connector.Error as error:
        print("Erro ao carregar dados:", error)

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

    self.data_table(cols, values)


@mainthread
def data_table(self, cols, values):
    self.data_tables = MDDataTable(
        pos_hint={'center_y': 0.5, 'center_x': 0.5},
        size_hint=(0.9, 0.6),
        column_data=[
            (col, dp(40))
            for col in cols
        ],
        row_data=values,
        check=True
    )

    self.add_widget(self.data_tables)


# registra as consultas
def registrar_consulta(self, especialidade, data, id_paciente):
    id_paciente = int(id_paciente)
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
        res = cursor.fetchone()

        if not res:
            self.ids.lbcheckin.text = "paciente não cadastrado"
        elif not data:
            self.ids.lbcheckin.text = "Insira uma data"
        else:
            if especialidade == "":
                self.ids.lbcheckin.text = "Insira especialidade"
            else:
                query = "INSERT INTO consultas (especialidade, id_paciente, data) VALUES (%s, %s, %s)"
                dados = (especialidade, id_paciente, data)
                cursor.execute(query, dados)
                connect.commit()
                self.ids.lbcheckin.text = "Registro realizado com sucesso"
    except mysql.connector.Error as error:
        print("Erro ao inserir registro:", error)
        self.ids.lbcheckin.text = "Erro ao inserir registro. Por favor, tente novamente mais tarde."

def on_save(self, instance, value, date_range):
  self.ids.data.text = str(value)

def on_cancel(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

# Cria o calendario
def show_data_picker(self):
  date_dialog = MDDatePicker(year=2022, month=6, day=17)
  date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
  date_dialog.open()

# Agendar retirada
def agenda_retirada(self, medicamento, data, id_paciente2):
    id_paciente2 = int(id_paciente2)
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM medicamentos WHERE nome = %s AND quantidade > 0", (medicamento,))
        medicamento_existe = cursor.fetchone()

        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id_paciente2,))
        paciente_existe = cursor.fetchone()

        if not medicamento_existe:
            self.ids.lbcheckout.text = "Medicamento não cadastrado ou quantidade insuficiente"
        elif not paciente_existe:
            self.ids.lbcheckout.text = "Paciente não cadastrado"
        elif not data:
            self.ids.lbcheckout.text = "Insira uma data"
        else:
            query = "INSERT INTO retirada (nome_medicamento, id_paciente, data) VALUES (%s, %s, %s)"
            dados = (medicamento, id_paciente2, data)
            cursor.execute(query, dados)
            connect.commit()
            self.ids.lbcheckout.text = "Registro realizado com sucesso"
    except mysql.connector.Error as error:
        print("Erro ao inserir registro:", error)
        self.ids.lbcheckout.text = "Erro ao inserir registro. Por favor, tente novamente mais tarde."


def on_save2(self, instance, value, date_range):
  self.ids.data.text = str(value)

def on_cancel2(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

def show_data_picker2(self):
  date_dialog = MDDatePicker(year=2022, month=6, day=17)
  date_dialog.bind(on_save=self.on_save2, on_cancel=self.on_cancel2)
  date_dialog.open()


on_stop5 = threading.Event()

def on_stop(self):
  self.on_stop5.set()

def on_enter7(self):
  self.start_second_thread()

def start_second_thread5(self):
  threading.Thread(target=self.load_data).start()

def load_data5(self, *args):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM pacientes')
        data = cursor.fetchall()
        # Processar os dados recebidos e atualizar a interface do usuário
        cols = [col[0] for col in cursor.description]
        values = [list(row) for row in data]

        self.data_table(cols, values)

    except mysql.connector.Error as error:
        print("Erro ao carregar dados:", error)

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

    self.data_table(cols, values)
@mainthread
def data_table5(self, cols, values):
  self.data_tables = MDDataTable(
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols
    ],
    row_data=values,
    check=True
  )

  self.add_widget(self.data_tables)


stop2 = threading.Event()

def on_stop2(self):
  self.stop2.set()

def on_enter4(self):
  self.start_second_thread()

def start_second_thread2(self):
  threading.Thread(target=self.load_data).start()

def load_data2(self, *args):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM consultas')
        data = cursor.fetchall()
        # Processar os dados recebidos e atualizar a interface do usuário
        cols = [col[0] for col in cursor.description]
        values = [list(row) for row in data]

        self.data_table(cols, values)

    except mysql.connector.Error as error:
        print("Erro ao carregar dados:", error)

    finally:
        # Fechar conexão com o banco de dados
        if connect.is_connected():
            cursor.close()
            connect.close()

    self.data_table(cols, values)

@mainthread
def data_table2(self, cols, values):
  self.data_tables = MDDataTable(
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols
    ],
    row_data=values,
    check=True
  )

  self.add_widget(self.data_tables)


stop3 = threading.Event()

def on_stop3(self):
  self.stop3.set()

def on_enter5(self):
  self.start_second_thread()

def start_second_thread3(self):
  threading.Thread(target=self.load_data).start()

def load_data3(self, *args):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM retirada')
        data = cursor.fetchall()
        # Processar os dados recebidos e atualizar a interface do usuário
        cols = [col[0] for col in cursor.description]
        values = [list(row) for row in data]

        self.data_table(cols, values)

    except mysql.connector.Error as error:
        print("Erro ao carregar dados:", error)

    finally:
        # Fechar conexão com o banco de dados
        if connect.is_connected():
            cursor.close()
            connect.close()

    self.data_table(cols, values)

@mainthread
def data_table3(self, cols, values):
  self.data_tables = MDDataTable(
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols
    ],
    row_data=values,
    check=True
  )

  self.add_widget(self.data_tables)


stop4 = threading.Event()


def on_stop4(self):
    self.stop4.set()


def on_enter6(self):
    self.start_second_thread()


def start_second_thread4(self):
    threading.Thread(target=self.load_data).start()


def load_data4(self, *args):
    cols = None
    values = None
    try:
        connect = db_connect()
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM plantao')
        data = cursor.fetchall()
        # Processar os dados recebidos e atualizar a interface do usuário
        cols = [col[0] for col in cursor.description]
        values = [list(row) for row in data]

    except mysql.connector.Error as error:
        print("Erro ao carregar dados:", error)

    finally:
        # Fechar conexão com o banco de dados
        if connect.is_connected():
            cursor.close()
            connect.close()

    if cols is not None and values is not None:
        self.data_table(cols, values)

def on_check_press(self, instance_table, current_row):
    HORARIOS_SELECIONADOS.append(current_row[0])

# Remove um plantao selecionado da tabela
def on_remove_duty_button_release(self):
    try:
        connect = db_connect()
        cursor = connect.cursor()

        # Supondo que a primeira coluna seja a chave primária (id) do item
        item_id = HORARIOS_SELECIONADOS[0]
        cursor.execute("DELETE FROM plantao WHERE id = %s", (item_id,))
        connect.commit()
        print("Item removido com sucesso.")

        # Atualizar a tabela após a remoção do item
        self.load_data()

    except mysql.connector.Error as error:
        print("Erro ao remover item:", error)

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()



@mainthread
def data_table4(self, cols, values):
    self.data_tables = MDDataTable(
        pos_hint={'center_y': 0.5, 'center_x': 0.5},
        size_hint=(0.9, 0.6),
        column_data=[
            (col, dp(40))
            for col in cols
        ],
        row_data=values,
        check=True
    )

    self.data_tables.bind(on_check_press=self.on_check_press)
    self.add_widget(self.data_tables)