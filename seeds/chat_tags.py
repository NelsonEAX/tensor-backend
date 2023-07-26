from datetime import timedelta
from random import randrange

from app.models.models import ChatType, UserRole
from .const import created_at, today, dt_format
from .user_chats import users

GROUP = ChatType.group.value
EVENT = ChatType.event.value

chat_default_field = {
    'created_at': created_at,
    'updated_at': created_at,
    'deleted_at': None
}

chat_avatars = [
    'static/chats/_GBeIPlQcbc.jpg',
    'static/chats/aJfmsA9nIwk.jpg',
    'static/chats/hcdvaW6eGbs.jpg',
    'static/chats/Kg022rBpLxk.jpg',
    'static/chats/n7rX58RMAg0.jpg',
    'static/chats/neural_image_6-750x586.jpg',
    'static/chats/neural_image_10-750x429.jpg',
    'static/chats/PJ6TMaFZmik.jpg',
    'static/chats/yYlRo1QOfDE.jpg',
    'static/chats/zRS8iqW76Fg.jpg'
]

chat_externals = [
    {
        'title': 'Базовая студенческая группа',
        'description': 'Здесь студенты общаются',
    },
    {
        'title': 'Встреча первая',
        'description': 'Здесь студенты обсуждают макет',
        'datetime': (today.replace(hour=16) + timedelta(days=10)).strftime(dt_format),
        'duration': 3600,
        'location': {
            "longitude": 56.831645,
            "latitude": 60.607778
        }
    },
    {
        'title': 'Встреча вторая',
        'description': 'Здесь студенты обсуждают реализацию',
        'datetime': (today.replace(hour=16) - timedelta(days=10)).strftime(dt_format),
        'duration': 3600,
        'location': {
            "longitude": 56.831645,
            "latitude": 60.607778
        }
    },
    {
        "title": "Я собираюсь сделать ему предложение, от которого он не сможет отказаться",
        "location": {
            "longitude": 121.825597,
            "latitude": -15.728856
        },
        "description": "Ну, вот ещё одна неприятность, в которую ты меня втянул!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Переписчик однажды попытался опросить меня. Я съел его печень с бобами и хорошим кьянти",
        "location": {
            "longitude": 13.429856,
            "latitude": -33.144874
        },
        "description": "Сыграй это, Сэм. Сыграй 'As Time Goes By.' (Сыграй, Сэм, сыграй… “В память о былых временах”)",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "В конце концов, завтра — другой день!",
        "location": {
            "longitude": -39.5792,
            "latitude": 64.260408
        },
        "description": "Держи своих друзей близко. А врагов ещё ближе",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Тебе нужна будет лодка побольше",
        "location": {
            "longitude": 148.677476,
            "latitude": 0.231669
        },
        "description": "Шейн. Шейн. Вернись!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Лучший друг парня — это его мать",
        "location": {
            "longitude": -45.503753,
            "latitude": 28.509249
        },
        "description": "Хьюстон, у нас проблема",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я вернусь",
        "location": {
            "longitude": 96.439416,
            "latitude": 75.901918
        },
        "description": "В конце концов, завтра — другой день!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Тебе нужна будет лодка побольше",
        "location": {
            "longitude": 168.474395,
            "latitude": -30.553288
        },
        "description": "Да пребудет с тобой Сила!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Моя прелесть",
        "location": {
            "longitude": 5.71356,
            "latitude": 9.279644
        },
        "description": "То, из чего сделаны мечты",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Инопланетянин звонить домой",
        "location": {
            "longitude": 80.986201,
            "latitude": -21.77197
        },
        "description": "О, нет, это не самолёты. Это Красота убила Чудовище.",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Шейн. Шейн. Вернись!",
        "location": {
            "longitude": 11.984709,
            "latitude": -53.343167
        },
        "description": "Нагрудные знаки? Нет у нас никаких знаков! Не нужны нам никаких знаков! Я не должен показывать вам никакие чёртовы знаки!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я тут иду! Я тут иду!",
        "location": {
            "longitude": 77.687972,
            "latitude": -6.456333
        },
        "description": "Бонд. Джеймс Бонд",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я вижу мёртвых людей",
        "location": {
            "longitude": -43.871402,
            "latitude": -2.854938
        },
        "description": "Построй, и они придут",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Правда тебе не по зубам",
        "location": {
            "longitude": -110.789235,
            "latitude": 49.59534
        },
        "description": "Честно говоря, моя дорогая, мне наплевать",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Ко мне обращаются “Мистер Тиббс”",
        "location": {
            "longitude": 87.95967,
            "latitude": -42.004154
        },
        "description": "Луи, мне кажется, это начало прекрасной дружбы",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я вижу мёртвых людей",
        "location": {
            "longitude": -146.316265,
            "latitude": 77.772505
        },
        "description": "В данном случае мы имеем отсутствие взаимопонимания",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Обожаю запах напалма по утрам!",
        "location": {
            "longitude": -13.403495,
            "latitude": 58.841149
        },
        "description": "Держи своих друзей близко. А врагов ещё ближе",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Оно живое! Живое!",
        "location": {
            "longitude": -103.154683,
            "latitude": -71.517675
        },
        "description": "Шейн. Шейн. Вернись!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Держи своих друзей близко. А врагов ещё ближе",
        "location": {
            "longitude": 52.969349,
            "latitude": -77.698517
        },
        "description": "Валяй, порадуй меня!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "В конце концов, завтра — другой день!",
        "location": {
            "longitude": -29.486222,
            "latitude": -8.156344
        },
        "description": "Вы знаете как свистеть, не так ли, Стив? Вы просто соединяете губы и дуете",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Оно живое! Живое!",
        "location": {
            "longitude": 75.709809,
            "latitude": 31.791487
        },
        "description": "Я зол, как чёрт, и я больше не собираюсь это терпеть!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Да пребудет с тобой Сила!",
        "location": {
            "longitude": 155.237889,
            "latitude": -48.859704
        },
        "description": "Миссис Робинсон, вы пытаетесь меня соблазнить, не так ли?",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я была твоя уже на «здрасьте»",
        "location": {
            "longitude": -77.905429,
            "latitude": 21.358852
        },
        "description": "Стелла! Эй, Стелла!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Тебе нужна будет лодка побольше",
        "location": {
            "longitude": -147.748343,
            "latitude": -76.946194
        },
        "description": "Бонд. Джеймс Бонд",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Жадность, за отсутствием более подходящего слова — это хорошо",
        "location": {
            "longitude": -32.71811,
            "latitude": 80.737825
        },
        "description": "Открой двери модуля, Хал",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Переписчик однажды попытался опросить меня. Я съел его печень с бобами и хорошим кьянти",
        "location": {
            "longitude": -130.768381,
            "latitude": -43.055556
        },
        "description": "Никто не задвинет Малышку в угол.",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Carpe diem. Ловите момент, мальчики. Сделайте свою жизнь экстраординарной",
        "location": {
            "longitude": 96.359831,
            "latitude": -53.425196
        },
        "description": "Арестуйте обычных подозреваемых",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "То-то, у меня такое ощущение, что мы больше не в Канзасе",
        "location": {
            "longitude": -97.788151,
            "latitude": -76.301553
        },
        "description": "Луи, мне кажется, это начало прекрасной дружбы",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Сыграй это, Сэм. Сыграй 'As Time Goes By.' (Сыграй, Сэм, сыграй… “В память о былых временах”)",
        "location": {
            "longitude": 134.974481,
            "latitude": 76.144564
        },
        "description": "Да пребудет с тобой Сила!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я тут иду! Я тут иду!",
        "location": {
            "longitude": -61.982939,
            "latitude": 70.357647
        },
        "description": "Никто не плачет в бейсболе!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Ну, вот ещё одна неприятность, в которую ты меня втянул!",
        "location": {
            "longitude": -123.607839,
            "latitude": 70.184293
        },
        "description": "Я — король мира!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Моя прелесть",
        "location": {
            "longitude": -137.720325,
            "latitude": -18.455928
        },
        "description": "Держи своих друзей близко. А врагов ещё ближе",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Это ты мне сказал?",
        "location": {
            "longitude": -66.711914,
            "latitude": 38.060302
        },
        "description": "Я собираюсь сделать ему предложение, от которого он не сможет отказаться",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Нагрудные знаки? Нет у нас никаких знаков! Не нужны нам никаких знаков! Я не должен показывать вам никакие чёртовы знаки!",
        "location": {
            "longitude": 112.498559,
            "latitude": 21.014517
        },
        "description": "Ла-дии-да, ла-дии-да",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я достиг этого, мам! Я на вершине мира!",
        "location": {
            "longitude": 171.313464,
            "latitude": 66.819527
        },
        "description": "Почему бы вам как-нибудь не прийти и не навестить меня?",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Бог мне свидетель, — я никогда больше не буду голодать",
        "location": {
            "longitude": 70.519757,
            "latitude": 60.986789
        },
        "description": "Тебе нужна будет лодка побольше",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я тут иду! Я тут иду!",
        "location": {
            "longitude": -90.738448,
            "latitude": 13.105765
        },
        "description": "Мне — то же, что и ей",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я собираюсь сделать ему предложение, от которого он не сможет отказаться",
        "location": {
            "longitude": 111.641628,
            "latitude": 31.773377
        },
        "description": "Нет ничего лучше, чем быть дома",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Стелла! Эй, Стелла!",
        "location": {
            "longitude": -74.813916,
            "latitude": 30.799445
        },
        "description": "Открой двери модуля, Хал",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я хочу побыть одна",
        "location": {
            "longitude": -51.880995,
            "latitude": 22.53001
        },
        "description": "Арестуйте обычных подозреваемых",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Хорошо, г-н Демилль, я готова для крупного плана",
        "location": {
            "longitude": -117.321923,
            "latitude": -38.216789
        },
        "description": "Честно говоря, моя дорогая, мне наплевать",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Бог мне свидетель, — я никогда больше не буду голодать",
        "location": {
            "longitude": -29.46096,
            "latitude": -78.9557
        },
        "description": "Сыграй это, Сэм. Сыграй 'As Time Goes By.' (Сыграй, Сэм, сыграй… “В память о былых временах”)",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Валяй, порадуй меня!",
        "location": {
            "longitude": 84.707044,
            "latitude": -50.992958
        },
        "description": "Я чувствую жажду — жажду скорости!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Честно говоря, моя дорогая, мне наплевать",
        "location": {
            "longitude": -164.245046,
            "latitude": 8.442984
        },
        "description": "Да пребудет с тобой Сила!",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Вы знаете как свистеть, не так ли, Стив? Вы просто соединяете губы и дуете",
        "location": {
            "longitude": -179.603786,
            "latitude": 73.114282
        },
        "description": "Бог мне свидетель, — я никогда больше не буду голодать",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Что ж, у каждого свои недостатки",
        "location": {
            "longitude": -5.633349,
            "latitude": -13.220149
        },
        "description": "Миссис Робинсон, вы пытаетесь меня соблазнить, не так ли?",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Ко мне обращаются “Мистер Тиббс”",
        "location": {
            "longitude": -82.426481,
            "latitude": -38.618212
        },
        "description": "Держи своих друзей близко. А врагов ещё ближе",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Я достиг этого, мам! Я на вершине мира!",
        "location": {
            "longitude": -128.4674,
            "latitude": -54.655218
        },
        "description": "Мы грабим банки",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Почему бы вам как-нибудь не прийти и не навестить меня?",
        "location": {
            "longitude": -15.693636,
            "latitude": 41.40103
        },
        "description": "Лучший друг парня — это его мать",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "Стелла! Эй, Стелла!",
        "location": {
            "longitude": -114.183273,
            "latitude": 54.758062
        },
        "description": "У нас всегда будет Париж",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    },
    {
        "title": "У нас всегда будет Париж",
        "location": {
            "longitude": 137.376948,
            "latitude": 12.51382
        },
        "description": "Правда тебе не по зубам",
        "datetime": (today.replace(hour=randrange(24)) + timedelta(days=randrange(100))).strftime(dt_format)
    }
]

chats = [
    {'id': '233a2f62-64c6-4130-addf-eb2c62ced681', 'parent_id': None, 'type': GROUP},
    {'id': '7990ad79-9bbc-44f2-8cce-2e091faf370f', 'parent_id': '233a2f62-64c6-4130-addf-eb2c62ced681', 'type': EVENT},
    {'id': '9dc5fd35-1828-4c81-abc4-7fb96dd6c563', 'parent_id': '233a2f62-64c6-4130-addf-eb2c62ced681', 'type': EVENT},
    {'id': '40b6c7d6-4e12-4889-8cce-eddfd33b976a', 'parent_id': None, 'type': EVENT},
    {'id': 'f3b4c4f5-483d-48a1-aaed-c4e2d1c89471', 'parent_id': None, 'type': GROUP},
    {'id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'parent_id': None, 'type': GROUP},
    {'id': '36e10978-9a77-488b-abe9-330b940b4469', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '89d5163a-1107-481e-abca-8e424b8b34ca', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '04c3b4c6-411d-4382-a035-f7e25bc28bcd', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': EVENT},
    {'id': 'e69b9c39-a419-4d28-9979-9cad5e4b032f', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '1ace8b3f-e784-47b6-ac21-60713e1cb0a5', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '9851c8cd-de12-4b18-9b83-8d73a65898d2', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': EVENT},
    {'id': '8af898be-295c-4c32-94c2-78244c840c4e', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '95a5651b-a5de-49d0-a510-ababb7791afc', 'parent_id': '8ca3e05d-3e83-4d93-ac05-498f559f5351', 'type': GROUP},
    {'id': '8a807918-5836-4f40-bb49-81fa03f6ca37', 'parent_id': None, 'type': GROUP},
    {'id': 'f4821c08-87ed-4bfd-a65f-7024b8b7e616', 'parent_id': None, 'type': EVENT},
    {'id': 'fdea169c-9cf2-466a-867a-b9521a2ba35f', 'parent_id': None, 'type': GROUP},
    {'id': '90cd774f-783b-4493-8d6b-290b9f85c8c2', 'parent_id': None, 'type': EVENT, 'deleted_at': created_at},
    {'id': 'f625e9ba-9b36-4e9d-86b0-fcf78691d6a2', 'parent_id': None, 'type': GROUP, 'deleted_at': created_at},
    {'id': '2be73cce-46c2-41b8-909a-21e98761fdc3', 'parent_id': None, 'type': EVENT},
    {'id': '3c460adb-47d1-451e-85bf-bbede975758f', 'parent_id': None, 'type': GROUP},
    {'id': '31946692-e515-434e-9fc3-20e5349bab6c', 'parent_id': None, 'type': GROUP},
    {'id': '052e1c29-66ce-40b2-8e14-c8133576516e', 'parent_id': None, 'type': GROUP},
    {'id': 'fec8edce-54b9-4a8c-ae3a-6c6f1d1a8cc9', 'parent_id': None, 'type': EVENT},
    {'id': '2f6c3d77-5b4a-4a3c-b398-8b456e116e57', 'parent_id': 'fec8edce-54b9-4a8c-ae3a-6c6f1d1a8cc9', 'type': GROUP},
    {'id': '6938c606-8eee-4989-9375-83f84cd05cf0', 'parent_id': 'fec8edce-54b9-4a8c-ae3a-6c6f1d1a8cc9', 'type': EVENT},
    {'id': '4d6e36e5-93a0-47a6-b332-384aac9cf1dd', 'parent_id': 'fec8edce-54b9-4a8c-ae3a-6c6f1d1a8cc9', 'type': GROUP},
    {'id': '13c33a62-5eb7-4626-9d03-b99fde79b37b', 'parent_id': None, 'type': GROUP},
    {'id': 'f4deff05-b39f-49f3-a829-1c913fa0840a', 'parent_id': None, 'type': EVENT},
    {'id': '88aee842-5551-4c97-9011-e7089586b592', 'parent_id': None, 'type': GROUP},
    {'id': 'aaac4401-91e9-4602-ae49-3f3131a4c937', 'parent_id': None, 'type': GROUP},
    {'id': 'a8f53617-aff4-4dcd-b59c-cf31c34c308a', 'parent_id': None, 'type': EVENT},
    {'id': '39026026-75be-432a-a64c-2f478d6f8d45', 'parent_id': None, 'type': GROUP},
    {'id': 'f153622f-d5a2-44fd-922f-0efe366b714b', 'parent_id': None, 'type': GROUP},
    {'id': '11fd579c-fffb-4695-bb54-4b0153e9b3d2', 'parent_id': None, 'type': GROUP, 'deleted_at': created_at},
    {'id': '6646037c-2ca1-4261-add1-6a2773060186', 'parent_id': None, 'type': GROUP, 'deleted_at': created_at},
    {'id': '5427f7ee-5132-45a5-aef1-e9305fbe5340', 'parent_id': None, 'type': EVENT},
    {'id': '45a02ca4-401c-4a28-aeb5-d53728c2547f', 'parent_id': None, 'type': GROUP},
    {'id': '4a519b6a-27cf-4972-ace4-2545d4525363', 'parent_id': None, 'type': GROUP},
    {'id': 'a20a9396-c4b2-4727-ba23-7a3becda2691', 'parent_id': None, 'type': GROUP},
    {'id': '6ad95cd1-0bf1-430a-8c11-351d0c16777d', 'parent_id': None, 'type': EVENT},
    {'id': '6386285b-c341-4e10-820a-5e8ca5b24e0c', 'parent_id': None, 'type': GROUP},
    {'id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'parent_id': None, 'type': GROUP},
    {'id': '99584a65-f41a-4f9e-a870-7fc02b9dd14e', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': EVENT},
    {'id': 'df3b3b99-e405-46d3-8dae-2a08ce56998b', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': EVENT},
    {'id': '2eb983f5-de97-4051-bab4-1b021182e064', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': GROUP},
    {'id': 'ef8cf32e-e04a-4f77-82f9-6cc81484ee44', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': GROUP},
    {'id': '7b535fdc-df93-4a86-a332-be809cb5fe1a', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': EVENT},
    {'id': '454d0162-3cdc-468c-aa64-5c8248979cb9', 'parent_id': 'a347f34b-0432-4015-b952-e50bd1bb8a91', 'type': EVENT},
    {'id': '7662c600-60fc-4149-bf78-fa1ad18d7767', 'parent_id': None, 'type': GROUP},
    {'id': 'f7189637-4217-46ef-9883-5c810733f0b1', 'parent_id': None, 'type': EVENT},
    {'id': '5763cadd-62ef-4a8b-a86e-4c6b1f068a72', 'parent_id': None, 'type': EVENT},
    {'id': '973d198b-16d1-4a5a-b77a-24d825583fed', 'parent_id': None, 'type': EVENT}
]

user_chats = [
    {'user_id': users[1]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.admin.value},
    {'user_id': users[2]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[3]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[4]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[5]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[7]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[8]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[1]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[2]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[3]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[4]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    # {'user_id': users[5]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[7]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[8]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.admin.value},
    {'user_id': users[1]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[2]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[3]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[4]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[5]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.admin.value},
    # {'user_id': users[7]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[8]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
]


def get_fake_chat_item():
    """Генератор, который возвращает один объект для вставки в базу"""
    for i in range(len(chats)):
        chat = chats[i]
        avatar = chat_avatars[i % 10]
        chat['external'] = chat_externals[i]
        chat['external']['avatar'] = avatar
        chat['external']['img'] = avatar
        chat = chat_default_field | chat
        yield chat
