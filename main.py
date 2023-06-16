import sqlite3
import webbrowser
import android
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.checkbox import CheckBox
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.utils import platform
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

connection.commit()


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.layout = RelativeLayout()

        Window.size = (360, 640)

        background_image = Image(source='c5f7fbcf8a07fceda73df7c1618a46bf.jpg')
        self.layout.add_widget(background_image)

        self.label = Label(text='\nДобро пожаловать в приложение для \n                  медитации и йоги!',
                           font_size=24,
                           size_hint=(None, None),
                           size=(360, 640),
                           pos_hint={'center_x': 0.5, 'center_y': 0.8},
                           color=(1,1,1))
        self.layout.add_widget(self.label)

        # Флажки с метками
        checkbox_layout1 = BoxLayout(orientation='horizontal',
                                     size_hint=(None, None),
                                     size=(245, 120),
                                     pos_hint={'center_x': .5, 'center_y': 0.3})

        label1 = Label(text='Вам есть 16 лет', size_hint=(None, None), size=(200, 50), font_size=18)
        self.checkbox1 = CheckBox(active=False, size_hint=(None, None), size=(10, 50))
        checkbox_layout1.add_widget(label1)
        checkbox_layout1.add_widget(self.checkbox1)
        self.layout.add_widget(checkbox_layout1)

        checkbox_layout2 = BoxLayout(orientation='horizontal',
                                     size_hint=(None, None),
                                     size=(300, 50),
                                     spacing=40,
                                     pos_hint={'center_x': 0.6, 'center_y': 0.2},
                                     padding=(10, 0, 10, 0))
        self.checkbox2 = CheckBox(active=False, size_hint=(None, None), size=(50, 50))
        label2 = Label(text='Написать персональные данные', size_hint=(None, None), size=(200, 50),font_size=18)
        checkbox_layout2.add_widget(label2)
        checkbox_layout2.add_widget(self.checkbox2)
        self.layout.add_widget(checkbox_layout2)

        self.agree_button = Button(text='Принять и Начать',
                                   font_size=22,
                                   size_hint=(None, None),
                                   size=(300, 50),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.agree_button.bind(on_press=self.switch_to_registration_screen)
        self.layout.add_widget(self.agree_button)

        self.add_widget(self.layout)

    def switch_to_registration_screen(self, instance):
        if not self.checkbox1.active or not self.checkbox2.active:
            popup = Popup(title='Ошибка',
                          content=Label(text='Примите условия конфиденциальности'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            return


        self.manager.current = 'registration'

class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        background_image = Image(source='6fab43555298da3d44f7df81cab89527.jpg')
        self.add_widget(background_image)
        self.layout = GridLayout(cols=1,spacing=15, padding=(50, 50))

        self.label = Label(text='\n                     \nРегистрация и Вход\n     \n', font_size='25sp', bold=True, color=('white'),
                           size_hint=(1, None), height=5)
        self.layout.add_widget(self.label)

        self.label = Label(text='\n             \nВведите свой логин и пароль',font_size=('20sp'),bold=True,color=('white'),
                           size_hint=(2,None),height=100)
        self.layout.add_widget(self.label)

        self.layout.add_widget(Label(text='Логин:', font_size='19sp',size_hint=(0.3, None), height=30))
        self.username_input = TextInput(multiline=False, hint_text='Введите логин',
                                        size_hint=(0.7, None), height=75)
        self.layout.add_widget(self.username_input)

        self.layout.add_widget(Label(text='Пароль:', font_size='19sp', size_hint=(0.3, None), height=30))
        self.password_input = TextInput(multiline=False, password=True, hint_text='Введите пароль',
                                        size_hint=(0.7, None), height=75)
        self.layout.add_widget(self.password_input)

        self.login_button = Button(text='Войти', size_hint=(0.3, None), height=75)
        self.login_button.bind(on_press=self.login_user)
        self.layout.add_widget(self.login_button)

        self.layout.add_widget(Label())

        self.register_button = Button(text='Зарегистрироваться', size_hint=(0.3, None), height=75)
        self.register_button.bind(on_press=self.register_user)
        self.layout.add_widget(self.register_button)

        self.logout_button = Button(text='Выйти', size_hint=(0.3, None), height=75)
        self.logout_button.bind(on_press=self.logout_user)
        self.layout.add_widget(self.logout_button)

        self.add_widget(self.layout)

    def animate_button(self, button):
        animation = Animation(size=(button.width*1.1, button.height*1.1), duration=0.1) + Animation(size=(button.width, button.height), duration=0.1)
        animation.start(button)

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        self.animate_button(instance)

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        self.switch_to_registration_screen(user)


    def logout_user(self, instance):
        self.manager.current = 'welcome'

    def switch_to_registration_screen(self, user):
        if user:
            self.manager.current = 'main_menu'
        else:
            popup = Popup(title='Ошибка',
                          content=Label(text='Неправильное имя пользователя или пароль'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        background_image = Image(source='ac7cd019ba3d3015f2d2ac3dfb544ea4.jpg')
        self.add_widget(background_image)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(40))
        self.add_widget(self.layout)

        self.label = Label(text='Главное меню', font_size='30sp', bold=True,size_hint=(0.3, None), height=75,
                           pos_hint={'center_x': 0.5, 'top': 1})
        self.layout.add_widget(self.label)
        button_box = BoxLayout(orientation='vertical', spacing=dp(5))

        self.option_spinner = Spinner(
            text='Выберите опцию',
            values=('Медитация Аудио', 'Цитата для мотивации', 'Йога'),bold=True,
            font_size=dp(20),
            background_color=(0.4, 0.7, 0.9, 1),
            background_normal='pngtree-dark-green-background-nature-texture-image_739055.jpg',
            size=(200, 70),size_hint=(0.8, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        button_box.add_widget(self.option_spinner)

        button_box.add_widget(BoxLayout(size_hint=(0.5, 0.1)))  # Добавляем пустой виджет в качестве разделителя

        self.switch_screen_button = Button(
            text='Перейти',bold=True,
            font_size=dp(24),
            background_color=(0.4, 0.7, 0.9, 1),
            background_normal='images1.jpg',
            background_down='button_background.png',
            color=(1, 1, 1, 1),

            size=(280, 80),size_hint=(0.8, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.switch_screen_button.bind(on_press=self.switch_screen)
        button_box.add_widget(self.switch_screen_button)


        self.website_button = Button(
            text='Посетить веб-сайт',
            font_size=dp(20),
            background_color=(0.4, 0.7, 0.9, 1),
            background_normal='images.jpg',
            background_down='button_background.png',
            color=(1, 1, 1, 1),
            size=(280, 60),size_hint=(0.7, None), height=60,
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.website_button.bind(on_press=self.open_website)
        button_box.add_widget(self.website_button)

        self.layout.add_widget(button_box)
    def switch_screen(self, instance):
        option = self.option_spinner.text
        if option == 'Медитация Аудио':
            self.manager.current = 'meditation_audio'
        elif option == 'Цитата для мотивации':
            self.manager.current = 'as'
        elif option == 'Йога':
            self.manager.current = 'yoga'

    def open_website(self, instance):
        website_url = 'https://wemeditate.com/ru'
        if platform == 'android':
            android.open_url(website_url)
        else:
            webbrowser.open(website_url)

class MeditationAudioScreen(Screen):
    def __init__(self, **kwargs):
        super(MeditationAudioScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        self.background = Image(source='1654277903_4-celes-club-p-anime-oboi-vertikalnie-krasivie-4.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        self.label = Label(text='Медитация Аудио', font_size=dp(30),bold=True, height=75,
                           size_hint=(1, 0.2),
                           pos_hint={'top': 0.99})
        self.layout.add_widget(self.label)

        self.start_button1 = Button(text='Старт музыка 1', size_hint=(.7, None), height=50, font_size=20,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.start_button1.bind(on_press=lambda instance: self.play_audio(instance, 1))
        self.start_button1.bind(on_release=lambda instance: self.animate_button(instance))
        self.layout.add_widget(self.start_button1)

        self.start_button2 = Button(text='Старт музыка 2', size_hint=(.7, None), height=50, font_size=20,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.start_button2.bind(on_press=lambda instance: self.play_audio(instance, 2))
        self.start_button2.bind(on_release=lambda instance: self.animate_button(instance))
        self.layout.add_widget(self.start_button2)

        self.start_button3 = Button(text='Старт музыка 3', size_hint=(.7, None), height=50, font_size=20,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.start_button3.bind(on_press=lambda instance: self.play_audio(instance, 3))
        self.start_button3.bind(on_release=lambda instance: self.animate_button(instance))
        self.layout.add_widget(self.start_button3)

        separator = Widget(size_hint=(1, 0.1))
        self.layout.add_widget(separator)

        self.stop_button = Button(text='Стоп', size_hint=(.5, None), height=60, font_size=22,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.stop_button.bind(on_press=self.stop_audio)
        self.stop_button.bind(on_release=lambda instance: self.animate_button(instance))
        self.layout.add_widget(self.stop_button)

        self.back_button = Button(text='Назад', size_hint=(.9, None), height=70, font_size=25,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.back_button.bind(on_press=self.switch_to_main_menu_screen)
        self.back_button.bind(on_release=lambda instance: self.animate_button(instance))
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        self.sound1 = SoundLoader.load('audio1.wav')
        self.sound2 = SoundLoader.load('audio2.wav')
        self.sound3 = SoundLoader.load('audio3.wav')

    def play_audio(self, instance, audio_number):
        if audio_number == 1 and self.sound1.state == 'stop':
            self.sound1.play()
        elif audio_number == 2 and self.sound2.state == 'stop':
            self.sound2.play()
        elif audio_number == 3 and self.sound3.state == 'stop':
            self.sound3.play()

    def stop_audio(self, instance):
        if self.sound1.state == 'play':
            self.sound1.stop()
        if self.sound2.state == 'play':
            self.sound2.stop()
        if self.sound3.state == 'play':
            self.sound3.stop()

    def switch_to_main_menu_screen(self, instance):
        self.sound1.stop()
        self.sound2.stop()
        self.sound3.stop()
        self.manager.current = 'main_menu'

    def animate_button(self, button):
        animation = Animation(size=(button.width * 1.9, button.height * 1.9), duration=0.5) + Animation(
            size=(button.width, button.height), duration=0.5)
        animation.start(button)

class RecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super(RecommendationScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        self.background = Image(source='eberhard-grossgasteiger-eZF9nZKBev8-unsplash.jpg', allow_stretch=True,
                                keep_ratio=False)
        self.layout.add_widget(self.background)

        self.label = Label(text='Цитата для мотивации',font_size='30sp', bold=True, size_hint=(1, 0.2),
                           pos_hint={'top': 0.99})
        self.layout.add_widget(self.label)

        self.recommendation_label = Label(
            text='''            "Стремись не к тому, чтобы\n добиться успеха,а к тому, чтобы\n твоя жизнь имела смысл", \n                                 – Альберт Эйнштейн.\n
            "Возможности не приходят\n сами — вы создаете их".\n                                           – Крис Гроссер.\n
            "Дышите. Поверьте в свою силу.\n Идите за своими мечтами." \n                                   – Харуки Мураками.\n
            "Ленивый художник никогда не \nсоздавал шедевров."\n                                      – Акбар Нурболат.\n
            ''',
            font_size='19sp',bold=True, size_hint=(1, 0.7), valign='top', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.recommendation_label)

        self.back_button = Button(text='Назад', size_hint=(None, None), size=(180, 50), font_size=25,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.back_button.bind(on_press=self.switch_to_main_menu_screen)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def switch_to_main_menu_screen(self, instance):
        self.manager.current = 'main_menu'

recommendation_screen = RecommendationScreen()

class YogaScreen(Screen):
    def __init__(self, **kwargs):
        super(YogaScreen, self).__init__(**kwargs)
        background_image = Image(source='1619512233_12-phonoteka_org-p-prostoi-fon-na-telefon-16.jpg')
        self.add_widget(background_image)

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Йога', font_size='30sp', bold=True, size_hint=(1, 0.9),
                           pos_hint={'top': 2})

        self.layout.add_widget(self.label)

        self.images = [
            {'image': Image(source='prana-first-website.png'), 'content': 'Прана - это древняя концепция, описывающая \nпоток жизненной энергии, '
                                                                                'который является \n'
                                                                                '           основой для всех живых существ.'},
            {'image': Image(source='1.png'), 'content': 'Уттхита Триконасана или Поза вытянутого\n'
                                                              'треугольника - является основополагающей\n                                 позой в йоге.'},
            {'image': Image(source='3.png'), 'content': 'Йога от головной боли - занятия йогой\nпозволяют'
                                                              ' уравновесить гормональный фон,'
                                                              '\nулучшить работу органов исистем организма.'},
            {'image': Image(source='4.png'), 'content': 'Хатха-йога - это учение о психофизической\nгармонии,'
                                                              'достигаемой с помощью физических\n'
                                                              '             средств воздействия на организм.'}
        ]

        self.current_image_index = 0
        self.layout.add_widget(self.images[self.current_image_index]['image'])

        self.content_label = Label(text=self.images[self.current_image_index]['content'], font_size=19,bold=True,)
        self.layout.add_widget(self.content_label)

        self.next_button = Button(text='Следующее фото', size_hint=(None, None), size=(240, 55), height=70,
                                  font_size=25,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.next_button.bind(on_press=self.show_next_image)
        self.layout.add_widget(self.next_button)

        self.spacer1 = Widget()  # Spacer между "Следующее фото" и "Назад"
        self.layout.add_widget(self.spacer1)

        self.back_button = Button(text='Назад', size_hint=(None, None), size=(360, 55), height=65,
                                  font_size=25,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.back_button.bind(on_press=self.switch_to_main_menu_screen)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def show_next_image(self, instance):
        self.current_image_index += 1

        if self.current_image_index >= len(self.images):
            self.current_image_index = 0

        if len(self.layout.children) > 1:
            self.layout.remove_widget(self.layout.children[-2])

        self.layout.add_widget(self.images[self.current_image_index]['image'], index=len(self.layout.children) - 1)

        self.content_label.text = self.images[self.current_image_index]['content']

    def switch_to_main_menu_screen(self, instance):
        self.manager.current = 'main_menu'


class MeditationApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(WelcomeScreen(name='welcome'))
        screen_manager.add_widget(RegistrationScreen(name='registration'))
        screen_manager.add_widget(MainMenuScreen(name='main_menu'))
        screen_manager.add_widget(MeditationAudioScreen(name='meditation_audio'))
        screen_manager.add_widget(RecommendationScreen(name='as'))
        screen_manager.add_widget(YogaScreen(name='yoga'))
        return screen_manager


if __name__ == '__main__':
    MeditationApp().run()