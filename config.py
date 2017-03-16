# -*- coding: utf-8 -*-
import sqlite3
token = '305251163:AAGfP_HDUiRgOsUfDDMJIvdJC5KCImzSmw4'
log_password = 'master 000000'


class Configuration (object):
    def __init__(self):
     pass

     self.main_hello = "Приветствую, пользователь, я NerruBot, \n" \
                       "Я помогу тебе решать организационные вопросы \n" \
                       "Вот список команд: \n" \
                       "/admin - чтобы стать админом \n" \
                       "/add_phone - добавить или изменить телефон \n" \
                       "/add_address- добавить или изменить адрес \n" \
                       "/phone - найти номер телефона человека \n" \
                       "/address - найти адрес человека \n" \
                       "/achieve_list - список ачивок человека \n" \
                       "/schedule - расписание на день \n" \
                       "/help - помощь \n" \
                       "/now - что и где сейчас происходит \n" \
                       "/quest - режим квеста \n" \


     self.admin_main_text = "Вы теперь админ \n" \
                            "/user - чтобы стать обычным пользователем \n" \
                            "/achieve - чтобы добавить ачивку \n" \
                            "/alarm - срочное сообщенье всем \n" \
                            "/add_event - чтобы добавить событие \n" \
                            "/language - изменить язык для всех юзеров (не баг, а фича)"
     self.admin_text = "/user - чтобы стать обычным пользователем \n" \
                        "/achieve - чтобы добавить ачивку \n" \
                       "/alarm - срочное сообщенье всем \n" \
                       "/add_event - чтобы добавить событие \n" \
                       "/add_event - чтобы добавить событие \n" \
                       "/language - изменить язык для всех юзеров (не баг, а фича)"
     self.add_phone_and_address = "Пожалуйста добавьте свой адрес и телефон \n" \
                                  "/add_phone - чтобы добавить или изменить телефон \n" \
                                  "/add_address - чтобы добавить или изменить адрес"
     self.admin_write_any = "Пожалуйста, введите логин и пароль после команды"
     self.admin_wrong = "Логин или пароль неверны"
     self.user_now = "Вы теперь обычный пользователь"
     self.address_ok = "Адрес был успешно обновлен"
     self.phone_ok = "Телефон был успешно обновлен"
     self.need_admin =  "Войдите c логином и паролем админа"
     self.achieve_guy = "Введите имя в формате Имя Фамилия"
     self.achieve ="Введите название ачивки"
     self.achieve_descr="Введите описание ачивки"
     self.get_achieve = "получил/получила ачивку"
     self.type_error = "Ошибка! Сожалею, что это произошло, поправим. Пожалуйста, воспользуйтесь справкой /help и следуйте иснтрукциям по вводу"
     self.achieve_exist = "Такая ачивка у этого пользователя уже есть"
     self.add_starttime = "Введите время начала события в формате: ЧЧ-ММ"
     self.add_endtime = "Введите время конца события в формате: ЧЧ-ММ"
     self.event_name = "Введите название события"
     self.event_descr = "Введите описание события"
     self.event_exist = "Такое мероприятие уже существует"
     self.add_date = "Введите дату события ГГГГ-ММ-ДД"
     self.event_added = "Событие успешно добавлено"
     self.schedule = "Расписание на день: \n"
     self.event_address = "Где проходит мероприятие?"
     self.now = "Сейчас будет мероприятие '"
     self.now1 = "Сейчас проходит мероприятие '"
     self.user_not_exist = "Такого пользователя не существует :( "
     self.at = "C"
     self.till = " до "
     self.address = "Местоположение"
     self.no_slash="Пожалуйста не используйте /"
     self.enter_something = "Пожалуйста после команды введите пробел и информацию"
     self.phone_enter = "Введите номер телефона"
     self.address_enter = "Введите адрес"
     self.log_enter = "Введите логин и пароль в формате Логин Пароль"
     self.data_exist = "Данных нет в системе"
     self.alarm = "Введите срочное сообщение"
     self.nothing = "Ничего сейчас не идет :("
     self.team_login = "Введите логин команды"
     self.team_pass = "Введите пароль команды"
     self.ok = "Правильно"
     self.not_ok = "Неправильно"
     self.quest = "Квест завершен, поздравляю!)"
     self.big_letter = "Пожалуйста, начинайте ваши ответы с заглавной буквы"
     self.admin_bool=False
     self.language = False


    def change_language (self):
            if self.language==0:
                self.main_hello = "Hello, master, I am Nerru Bot, \n" \
                                  "I will help you to solve organisation problems\n" \
                                  "Here are some things that I can do: \n" \
                                 "/admin - you can be an admin \n" \
                                 "/add_phone - to add or change your phone number \n" \
                                 "/add_address - to add or change address \n" \
                                 "/phone - find somebody's phone number \n" \
                                 "/address - find somebody's address \n" \
                                 "/achieve_list - list of smbd achievements \n" \
                                 "/schedule - day's schedule \n" \
                                  "/help - help \n"

                self.admin_main_text = "You are in admin mod now \n" \
                                  "/user - to go back to user mode \n" \
                                  "/achieve - to add achieve \n" \
                                  "/add_event - to add event in schedule \n" \
                                  "/alarm - to send message everybody \n" \
                                  "/language - to change language for all users (not bag, feature) \n"
                self.admin_text = "/user - to go back to user mode \n" \
                                  "/achieve - to add achieve \n" \
                                  "/alarm - to send message everybody \n" \
                                  "/language - to change language for all users (not bag, feature) \n" \
                                  "/add_event - to add event in schedule"
                self.add_phone_and_address = "Please add your phone number and address using \n" \
                                        "/add_phone - to add or change your phone number \n" \
                                        "/add_address - to add or change address "
                self.admin_write_any = "Please add login and password after command"
                self.admin_wrong = "Login or password is wrong"
                self.user_now = "You are in user's mod now"
                self.address_ok =  "Address was successfully updated"
                self.phone_ok =  "Phone was successfully updated"
                self.need_admin = "You need to be an admin to do this"
                self.achieve_guy = "Please enter name and surname like Name Surname"
                self.achieve = "Enter name of achievement"
                self.achieve_descr = "Enter description of achievement"
                self.get_achieve = "got achievement"
                self.type_error = "Error! I am sorry, that it happened. Please use /help"
                self.achieve_exist = "This achieve already exist"
                self.add_starttime = "Enter event's start time in format: HH:MM"
                self.add_endtime = "Enter event's end time in format: HH:MM"
                self.event_name = "Enter name of event"
                self.event_descr = "Enter event's description"
                self.event_exist = "This event has already exist"
                self.add_date = "Enter date of event YYYY-MM-DD"
                self.event_added = "Event successfully added"
                self.schedule = "Day schedule: \n"
                self.event_address = "Where is event?"
                self.usen_not_exist = "This user doesn't exist :( "
                self.now = "Now it gonna be '"
                self.now1 = "Now it is '"
                self.at = "From"
                self.till = " to "
                self.address = "Place"
                self.no_slash = "Please, don't use /"
                self.enter_something = "Please, after command enter space and information"
                self.phone_enter = "Enter phone number"
                self.log_enter = "Enter login and password like Login Password"
                self.address_enter = "Enter address"
                self.data_exist = "There is no such data"
                self.alarm = "Enter message"
                self.nothing = "Nothing is happening now :("
                self.team_login = "Enter team login"
                self.ok = "Right"
                self.not_ok = "Wrong"
                self.team_pass = "Enter team password"
                self.quest = "Quest has ended, congratulations!)"
                self.big_letter = "Pls, start messages from title letter"
                self.language = 1

            elif (self.language==1):
                self.main_hello = "Приветствую, пользователь, я NerruBot \n" \
                                  "Я помогу тебе решать организационные вопросы \n" \
                                  "Вот список команд: \n" \
                                 "/admin - чтобы стать админом \n" \
                                 "/add_phone phone - добавить или изменить телефон \n" \
                                 "/add_address address - добавить или изменить адрес \n" \
                                 "/phone - найти номер телефона человека \n" \
                                 "/address - найти адрес человека \n" \
                                 "/achieve_list - список ачивок человека \n" \
                                 "/schedule - расписание на день \n" \
                                  "/help - помощь \n"
                self.admin_main_text = "Вы теперь админ \n" \
                                  "/user - чтобы стать обычным пользователем \n" \
                                  "/achieve - чтобы добавить ачивку \n" \
                                  "/language - изменить язык для всех юзеров (не баг, а фича)\n"\
                                  "/add_event - чтобы добавить событие"
                self.admin_text = "/user - чтобы стать обычным пользователем \n" \
                                  "/achieve - чтобы добавить ачивку \n" \
                                  "/alarm - срочное сообщенье всем \n" \
                                  "/language - изменить язык для всех юзеров (не баг, а фича)\n" \
                                  "/add_event - чтобы добавить событие"
                self.add_phone_and_address = "Пожалуйста добавьте свой адрес и телефон \n" \
                                        "/add_phone - чтобы добавить или изменить телефон \n" \
                                        "/add_address - чтобы добавить или изменить адрес "
                self.admin_write_any = "Пожалуйста, введите логин и пароль после команды"
                self.admin_wrong = "Логин или пароль неверны"
                self.user_now = "Вы теперь обычный пользователь"
                self.address_ok = "Адрес был успешно обновлен"
                self.phone_ok = "Телефон был успешно обновлен"
                self.need_admin = "Войдите c логином м паролем админа"
                self.achieve_guy = "Введите имя в формате Имя Фамилия"
                self.achieve = "Введите название ачивки"
                self.achieve_descr = "Введите описание ачивки"
                self.get_achieve = "получил/получила ачивку"
                self.type_error = "Ошибка! Сожалею, что это произошло, поправим. Пожалуйста, воспользуйтесь справкой /help и следуйте иснтрукциям по вводу"
                self.achieve_exist = "Такая ачивка у этого пользователя уже есть"
                self.add_starttime = "Введите время начала события в формате: ЧЧ-ММ"
                self.add_endtime = "Введите время конца события в формате: ЧЧ-ММ"
                self.event_name = "Введите название события"
                self.event_descr = "Введите описание события"
                self.event_exist = "Такое мероприятие уже существует"
                self.add_date = "Введите дату события ГГГГ-ММ-ДД"
                self.event_added = "Событие успешно добавлено"
                self.schedule = "Расписание на день: \n"
                self.event_address = "Где проходит мероприятие?"
                self.usen_not_exist = "Такого пользователя не существует :( "
                self.now = "Сейчас будет мероприятие '"
                self.now1 = "Сейчас проходит мероприятие '"
                self.at = "C"
                self.till = " до "
                self.address = "Местоположение"
                self.no_slash = "Пожалуйста не используйте"
                self.enter_something = "Пожалуйста после команды введите пробел и информацию"
                self.phone_enter = "Введите номер телефона"
                self.log_enter = "Введите логин и пароль в формате Логин Пароль"
                self.address_enter = "Введите адрес"
                self.data_exist = "Данных нет в системе"
                self.alarm = "Введите срочное сообщение"
                self.nothing = "Ничего сейчас не идет :("
                self.ok = "Правильно"
                self.team_login = "Введите логин команды"
                self.team_pass = "Введите пароль команды"
                self.not_ok = "Неправильно"
                self.quest = "Квест завершен, поздравляю!)"
                self.big_letter = "Пожалуйста, начинайте ваши ответы с заглавной буквы"
                self.language = 0



    def bd_on (self):

        self.conn_db = sqlite3.connect('GoTo.sqlite')
        self.conn_db_cursor = self.conn_db.cursor()

    def bd_of (self):
        self.conn_db.commit()
        self.conn_db.close()