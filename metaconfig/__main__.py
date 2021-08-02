# Импортируем необходимые классы из модуля
from metaconfig import IntField, Fieldset, ConfigRoot, ListField, StrField, BoolField, JsonFileConfigIO


# Создадим набор полей, содержащий поля хост и порт
class HostPort(Fieldset):
    # Определим поле host как StrField с названием "Хост", подсказкой "IP адрес" и значеним по-умолчанию 0.0.0.0
    host = StrField(label='Хост', default='0.0.0.0', hint="IP адрес")
    port = IntField(label='Порт', default=11000)


# Создадим другой набор полей
class Server(Fieldset):
    location = StrField(label="Местонахождение сервера", default='', hint="Страна")
    # Используем определенный ранее набор полей с дополнительным пояснением
    connection_data = HostPort(label='Данные для подключения')


# Создадим корневой узел конфигурации 
class Config(ConfigRoot):
    __io_class__ = JsonFileConfigIO('proxy.settings')

    # Объявим список серверов
    proxy_pool = ListField(
            Server(
                label="Прокси-сервер", 
                default={
                    'location': 'USA',
                    'connection_data': {
                        'host': 'proxy.google.com',
                        'port': '3128'
                    }
                }
            ),
            label='Пул прокси-серверов',
            default=[]
        )
    
    # и адрес собственного сервера
    home = Server(
                label='Домашний сервер', 
                default={
                    'location': 'Russia', 
                    'connection_data': {
                        'host': 'home.server.com', 
                        'port': 4123
                    }
                }
            )

    # а так же параметр, разрешающий отключить использование прокси
    use_proxy = BoolField(label='Использовать прокси', default=True)
    

# Проинициализируем получившуюся конфигурацию
config = Config()

# Получим из нее конкретное значение (автокомплиты нам помогут)
print(config.home.location)
# Получим все данные из конфигурации
print(config.as_dataset())
# Получим метаданные о конфигурации
print(config.as_metadata())
# Точечно обновим один из параметров
config.update({'use_proxy': False})


# print(config.as_dataset())
# print(json.dumps(config.as_dataset(), indent=2,ensure_ascii=False))

