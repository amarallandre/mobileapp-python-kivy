from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from functions import user_register, log_in, lost_password, change_about, patient_register

Window.size = (350, 580)

global screen

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
    pass

class CheckoutScreen(Screen):
    pass

class MedsScreen(Screen):
    pass

class ActivitiesScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class ScheduleScreen(Screen):
    pass
class TakeoffScreen(Screen):
    pass

class PacientScreen(Screen):
    pass

class RegisterPacients(Screen):
    def register_patient(self, nome2, cpf2):
        patient_register(self, nome2, cpf2)

class HourScreen(Screen):
    def callbackplantao(self, *args):
        from functions import callbackplantao
        callbackplantao(self, *args)

    def on_save3(self, instance, value, date_range):
        from functions import on_save3
        on_save3(self, instance, value, date_range)

    def on_cancel3(self, instance, value):
        from functions import on_cancel3
        on_cancel3(self, instance, value)

    def show_data_picker3(self):
        from functions import show_data_picker3
        show_data_picker3(self)

    def registraPlantao(self, cpf_funcionario, data2, horario, horario2):
        from functions import create_post_hour
        create_post_hour(self, cpf_funcionario, data2, horario, horario2)


class DutyScreen(Screen):
    pass

class VerifyMedsScreen(Screen):
    pass

class ControlMedsScreen(Screen):
    pass


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
        kv = Builder.load_file("loginscreen.kv")
        screen = kv
        return screen

if __name__ == '__main__':
    MedApp().run()