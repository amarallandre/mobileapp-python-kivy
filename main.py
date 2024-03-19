from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from functions import user_register, log_in, lost_password

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
    def forget_pass(self, senha, cpf):
        lost_password(self, senha, cpf)
class DashboardScreen(Screen):
    def on_enter(self, *args):
        # Acessando o nome de usuário logado
        nome_usuario_logado = MDApp.get_running_app().root.get_screen('login').nome_usuario_logado
        self.ids.lbdashboard.text = f"Bem-vindo, {nome_usuario_logado}"
class AboutUserScreen(Screen):
    pass

class ChangeAboutScreen(Screen):
    pass

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
    pass

class HourScreen(Screen):
    pass

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