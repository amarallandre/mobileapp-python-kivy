from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from functions import user_register, log_in, lost_password, change_about, patient_register, create_post_meds, \
    create_delete, registrar_consulta, show_data_picker, on_cancel, on_save, agenda_retirada, \
    on_remove_duty_button_release, on_stop2, data_table, load_data, start_second_thread, on_enter, on_stop, data_table4, \
    on_check_press, load_data4, start_second_thread4, on_enter6, on_stop4, create_post_hour, show_data_picker3, \
    on_cancel3, on_save3, callbackplantao, data_table5, load_data5, start_second_thread5, on_enter7, on_stop5, \
    data_table3, load_data3, start_second_thread3, on_enter5, on_stop3, data_table2, load_data2, start_second_thread2, \
    on_enter4

global screen

Window.size = (350, 580)
screen = ScreenManager()

class SplashScreen(Screen):
    pass
class LoginScreen(Screen):

    def initial_screen(self):
        MDApp.get_running_app().root.current = 'dashboard'
    def login_auth(self, cpf, senha):
        log_in(self, cpf, senha)
class RegisterScreen(Screen):

    def sign_in(self, nome, cpf, senha):
        user_register(self, nome, cpf, senha)

class ForgetPassScreen(Screen):
    def forget_pass(self, cpf, senha):
        lost_password(self, cpf, senha)

class DashboardScreen(Screen):
    def on_enter(self, *args):
        # Acessando o nome de usuário logado
        nome_usuario_logado = MDApp.get_running_app().root.get_screen('login').nome_usuario_logado
        self.ids.lbdashboard.text = f"Bem-vindo, {nome_usuario_logado}"
class AboutUserScreen(Screen):
    def on_enter(self, *args):
        nome_usuario_logado = MDApp.get_running_app().root.get_screen('login').nome_usuario_logado
        self.ids.nomefuncionario.text = f"{nome_usuario_logado}"

        cpf_usuario_logado = MDApp.get_running_app().root.get_screen('login').cpf_usuario_logado
        self.ids.cpffuncionario.text = f"{cpf_usuario_logado}"

        id_usuario_logado = MDApp.get_running_app().root.get_screen('login').id_usuario_logado
        self.ids.idfuncionario.text = f"{id_usuario_logado}"


class ChangeAboutScreen(Screen):
    def editaInfo(self, nome, cpf, senha):
        change_about(self, nome, cpf, senha)
        MDApp.get_running_app().stop()
        MedApp().run()

class PrecheckScreen(Screen):
    pass

class CheckinScreen(Screen):
    def consulta(self, especialidade, data, id_paciente):
        registrar_consulta(self, especialidade, data, id_paciente)

    def on_save(self, instance, value, data_range):
        on_save(self, instance, value, data_range)

    def on_cancel(self, instance, value):
        on_cancel(self, instance, value)

    def data(self):
        show_data_picker(self)


class CheckoutScreen(Screen):
    def retirada(self, medicamento, data, id_paciente2):
        agenda_retirada(self, medicamento, data, id_paciente2)

    def on_save2(self, instance, value, data_range):
        from functions import on_save2
        on_save2(self, instance, value, data_range)

    def on_cancel2(self, instance, value):
        from functions import on_cancel2
        on_cancel2(self, instance, value)

    def data(self):
        from functions import show_data_picker2
        show_data_picker2(self)


class MedsScreen(Screen):
    pass

class ActivitiesScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class ScheduleScreen(Screen):
    def on_stop(self):
        on_stop2(self)

    def on_enter(self):
        on_enter4(self)

    def start_second_thread(self):
        start_second_thread2(self)

    def load_data(self, *args):
        load_data2(self, *args)

    def data_table(self, cols, values):
        data_table2(self, cols, values)
class TakeoffScreen(Screen):
    def on_stop(self):
        on_stop3(self)

    def on_enter(self):
        on_enter5(self)

    def start_second_thread(self):
        start_second_thread3(self)

    def load_data(self, *args):
        load_data3(self, *args)

    def data_table(self, cols, values):
        data_table3(self, cols, values)

class PacientScreen(Screen):
    def on_stop(self):
        on_stop5(self)

    def on_enter(self):
        on_enter7(self)

    def start_second_thread(self):
        start_second_thread5(self)

    def load_data(self, *args):
        load_data5(self, *args)

    def data_table(self, cols, values):
        data_table5(self, cols, values)

class RegisterPacients(Screen):
    def register_patient(self, nome2, cpf2):
        patient_register(self, nome2, cpf2)

class HourScreen(Screen):
    def callbackplantao(self, *args):
        callbackplantao(self, *args)

    def on_save3(self, instance, value, date_range):
        on_save3(self, instance, value, date_range)

    def on_cancel3(self, instance, value):
        on_cancel3(self, instance, value)

    def show_data_picker3(self):
        show_data_picker3(self)

    def registraPlantao(self, cpf_funcionario, data2, horario, horario2):
        create_post_hour(self, cpf_funcionario, data2, horario, horario2)


class DutyScreen(Screen):
    def on_stop(self):
        on_stop4(self)

    def on_enter(self):
        on_enter6(self)

    def start_second_thread(self):
        start_second_thread4(self)

    def load_data(self, *args):
        load_data4(self, *args)

    def on_check_press(self, instance_table, current_row):
        on_check_press(self, instance_table, current_row)

    def on_remove_duty_button_release(self):
        on_remove_duty_button_release(self)

    def data_table(self, cols, values):
        data_table4(self, cols, values)

class VerifyMedsScreen(Screen):
    def on_stop(self):
        on_stop(self)

    def on_enter(self):
        on_enter(self)

    def start_second_thread(self):
        start_second_thread(self)

    def load_data(self, *args):
        load_data(self, *args)

    def data_table(self, cols, values):
        data_table(self, cols, values)

class ControlMedsScreen(Screen):
    def entradaMeds(self, nome_med, quantidade, id_med):
        create_post_meds(self, nome_med, quantidade, id_med)

    def saidaMeds(self, nome_med, quantidade, id_med):
        create_delete(self, nome_med, quantidade, id_med)


screen.add_widget(SplashScreen(name='splash'))
screen.add_widget(LoginScreen(name='login'))
screen.add_widget(ForgetPassScreen(name='esqueci'))
screen.add_widget(RegisterScreen(name='register'))
screen.add_widget(DashboardScreen(name='dashboard'))
screen.add_widget(PrecheckScreen(name='precheck'))
screen.add_widget(CheckinScreen(name='checkin'))
screen.add_widget(CheckoutScreen(name='checkout'))
screen.add_widget(MedsScreen(name='meds'))
screen.add_widget(VerifyMedsScreen(name='verifymeds'))
screen.add_widget(ControlMedsScreen(name='controlmeds'))
screen.add_widget(ActivitiesScreen(name='activities'))
screen.add_widget(RegisterPacients(name='cadastropacientes'))
screen.add_widget(HourScreen(name='hour'))
screen.add_widget(InfoScreen(name='info'))
screen.add_widget(ScheduleScreen(name='schedule'))
screen.add_widget(TakeoffScreen(name='takeoff'))
screen.add_widget(DutyScreen(name='duty'))
screen.add_widget(PacientScreen(name='pacients'))



class MedApp(MDApp):
    def build(self):
        kv = Builder.load_file("screens.kv")
        screen = kv
        return screen

if __name__ == '__main__':
    MedApp().run()