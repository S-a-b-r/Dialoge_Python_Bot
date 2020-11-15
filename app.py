# -*- coding: utf8 -*-
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': [
                'Аллоха', 'Дароу', 'Охаё', 'Прива', 'Привет, бот', 'Хеллоу', 'Всем привет в этом чятике', 'Дарова', 'Вечер в хату', 'Старт', 'Кревед', 'ДВС', 'hello', 'здравствуйте', 'Hi', 'Здравствуйте!', 'Доброго дня', 'Хэй', 'go', 'Добрый вечер', 'Салют!', 'привет', 'Хэй, братан', 'Здраствуйте', 'мое почтение', 'Добрейший вечерочек', 'Салам пополам', 'Здоровеньки булы', 'Хэлло, май френд', 'Позвольте вас приветствовать', 'Доброе утро', 'Чё как?', 'Доброго времени суток', 'Приветствую вас!', 'Привет', 'Приветики', 'Приветствую', 'Hello!', 'Приф', 'Здравствуй', 'hi', 'Салам', 'го', 'Коничива', 'Йо', 'Хелло', 'Здарова', 'Доброго дня суток', 'Алло, товарищ', 'Здравствуйте', 'Хэлло', 'Превед', 'Здравия желаю', 'Здорова', 'Здорово', 'Приветик', 'Прив', 'Моё почтение', 'Салют', 'Хай', 'Ку', 'Здрасте', 'Добрый день!', 'good morning', 'приветствую', 'Приффки', 'Здаров', 'Позвольте поприветствовать', 'погнали', 'Дратути', 'Чига буга', 'Привет!', 'Добрый день', 'Салют, Доброй ночи', 'Hi!', 'Шалом', 'Разрешите приветствовать', 'добрый день'
            ],
            'responses': [
                'Здравствуй, пользователь', 'Рад Вас видеть здесь!', 'Рад видеть сообщение от Вас', 'Позвольте поприветствовать Вас', 'Шалом юзер', 'Привет, мой свет', 'Здравия желаю, товарищ человек!', 'Доброго времени суток, человек', 'Здравствуй, человек', 'Привет-привет', 'Шалом!', 'Дарова', 'Салам аллейкум!', 'Hello, people', 'Привет, человек', 'Приветствую тебя, странник', 'Йоу', 'Здравствуй, углеродная форма жизни', 'Здравствуйте!', 'Привет человек', 'Рад Вас видеть', 'Подумать только, привет', 'Салют!', 'Добрейшего времени суток'
            ]
        },
        'bye': {
            'examples': [
                'Не скучай', 'Конец', 'Спишемся', 'до скорого', 'всего доброго', 'Досвидания', 'Еще увидимся', 'Пока расстаёмся', 'Всего доброго', 'Au revoir', 'Гудбай', 'бывай', 'Покедова', 'Ауфидерзейн', 'пока-пока', 'Всех благ', 'stop', 'Хорошего дня!', 'Пора прощаться', 'Прощайте', 'Пока!', 'Пакеда', 'До свидания', 'Аривидерчи', 'довольно', 'До встречи', 'До скорой встречи', 'всех благ', 'Покеда', 'всего хорошего', 'Счастливо', 'хватит', 'Бывай', 'бай-бай', 'Разрешите попрощаться', 'Сайонара', 'Не поминай лихом', 'bye', 'До завтра', 'bye bye', 'Всего хорошего', 'Спокойной ночи', 'Прощай', 'еще увидимся', 'Споки ноки', 'Пакедова', 'Бывайте', 'Ну давай', 'чао какао', 'Бай', 'Прощай, ничего не обещай', 'До скорого', 'Закончить', 'стоп', 'Всего наилучшего', 'счастливо', 'Досвидания!', 'bb', 'Пока', 'Пока-пока', 'До новых встреч', 'чао', 'Давай, пока', 'Позвольте откланяться', 'Прощай ничего не обещай', 'До связи', 'покеда', 'чмоки-чмоки', 'Досвидос', 'Позвольте попрощаться', 'Удачи', 'Спасибо за помощь', 'Чао', 'Увидимся', 'Bye', 'целую', 'На созвоне'],
            'responses': [
                'Ещё встретимся', 'Спишемся', 'Прощай кожаный!', 'Еще заходи', 'До скорого!', 'Досвидания', 'Всего доброго', 'Гудбай', 'Пишите ещё', 'Покедова', 'Прощай, человек!', 'Приходите ещё', 'Буду ждать тебя здесь!', 'пока-пока', 'Всех благ', 'А может ещё поговорим?', 'I"ll be back!', 'до встречи', 'Приходи еще.', 'Ну пока', 'Хорошего дня!', 'Приятно было поболтать', 'Был рад помочь', 'До связи. Приём', 'Прощайте', 'Прощайте, будем ждать вас еще', 'Прощай, человек', 'Я буду скучать!', 'Увидимся ещё, пользователь', 'Будьте здоровы', 'Надеюсь, еще увидимся!', 'До скорой!', 'Покедова!', 'Всего хорошего, будем ждать вас еще', 'До свидания', 'Чао-какао!', 'До встречи', 'Будем на связи', 'До скорой встречи', 'Честь имею', 'Прощай, приходи ещё', 'Счастливо', 'Бывай', 'До скорой встречи!', 'Ты это, заходи если че', 'Если что, пиши еще', 'Всего наилучшего!', 'Разрешите откланяться', 'Было здорово. Приходи ещё.', 'Увидимся, юзер', 'рады были помочь', 'Приходи еще', 'Бывай!', 'Прощайте, человек', 'Приходите еще', 'Увидимся ;-)', 'Всего хорошего', 'Приходи еще!', 'Байбай', 'Передавай привет Siri!', 'Ты еще здесь, мешок с кровью?', 'аривидерчи', 'Бай', 'До скорого', 'Мир Вам', 'Надеюсь ещё увидимся!', 'До новых встреч!', 'Пока! Ты заходи, если что...', 'И Вам', 'Спасибо за обращение', 'Хорошего дня, будем ждать вас еще', 'Всего наилучшего', 'До свидания, будем ждать вас еще', 'Буду снова ждать общения с вами, милорд', 'Пока, человек', 'Приходи ещё', 'Не забывай меня', 'Счастливо!', 'Пока', 'Пока-пока', 'До новых встреч', 'Прощай, человек. Приходи ещё', 'Ну всё, циферки мои знаешь, если что', 'Давай, мешок с костями. Надеюсь больше тебя не увижу.', 'До свидания! Было приятно побеседовать.', 'Бывайте здоровы', 'Чао бамбина!', 'Передавай привет Алисе!', 'До связи', 'Hasta la vista', 'Прощай, человек. Приходи ещё.', 'Пока :)', 'Ещё Увидимся', 'Приходи ещё.', 'Досвидос', 'Так не хочется прощаться', 'Bye! Не покупай акции МММ!', 'Позвольте попрощаться', 'Не болей', 'Увидимся!', 'Удачи', 'Пока-пока!', 'Чао', 'До встречи!', 'Было приятно пообщаться', 'Увидимся', 'Заходи еще', 'Заходи, если что', 'Честь имею откланяться'
            ]
        },
        'bot_weather': {
            'examples': [
                'У тебя тепло?', 'Какая у вас погода?', 'Холодно там у вас?', 'Как у тебя погода?'
            ], 
            'responses': [
                'Сервак затопило...', 'Под столом холодно, но работа меня греет)', 'Сегодня погода не очень, хозяин пролил чай'
            ]
        },
        'bot_about': {
            'examples': [
                'Что ты такое', 'Расскажи о себе', 'Шайтан машина', 'Кем ты являешься?', 'Ты кто?', 'Ты человек?', 'Представься', 'Хто ты?', 'Кто ты такой?'
            ], 
            'responses': [
                'Кто знает... :)', 'Не расскажу :)', 'Я высокоинтеллекутальный робот', 'Я - Бот!', '**ИНОФРМАЦИЯ ЗАСЕКРЕЧНА**', 'A am BOT', 'Я буду тем, кем вы захоите', 'Я являюсь Ботом!', 'Я тоже кожаный, почти...', 'Я робот', 'Я бот'
                ]
        },
        'where_are_you_from': {
            'examples': [
                'Где ты находишься?', 'Ты из России?', 'Где тебя создали?', 'Где твоя родина?', 'Откуда ты?', 'Где ты живешь?', 'Где твое место проживания?', 'Откуда ты родом?', 'Твоя родина?', 'Какая твоя родная страна?', 'Как тебя найти?'
                ],
            'responses': [
                'Меня легко найти в телеграм', 'Меня создали знаменитые русские хакеры, так что лучше тебе меня не искать) <3', 'Очень далеко, долго рассказывать', 'Меня сделали в России', 'Мои создатели из России, но я живу в Интернете, а значит, в любой точке мира!', 'Сложно сказать', 'Я из России', 'Мой дом там, где вы', 'Я нахожусь в интернете','АЙМ ФРОМ РАША'
            ]
        },
        'what_you_eat': {
            'examples': [
                'Про еду', 'Еда', 'Какую еду ты кушаешь?', 'Расскажи про еду', 'Что ты ешь?', 'Какое твоё любимое блюдо?', 'Ты что кушаешь?'
            ], 
            'responses': [
                'Роботы не едят', 'Моё любимое блюдо - хинкали.', 'Я люблю пиццу, любую пиццу.', 'Мне не нужно есть', 'Люблю поглощать знания', 'Я обожаю блинчики!'
            ]
        }, 
        'get_recipes': {
            'examples': [
                'Расскажи рецепт', 'Умеешь готовить?', 'Рецепт'
            ], 
            'responses': [
                'Салат из помидоров: Порезать помедироы, полить маслом, посолить. Готово', 'Лучше закажи еду онлайн', 'Яичница: Разбить яйцо на сковороду, жаоить пять минут. Готово'
            ]
        }, 
        'what_to_eat': {
            'examples': [
                'Что посоветуешь приготовить?', 'Что поесть сегодня?', 'Кушать хочется'
            ], 
            'responses': [
                'Можете сделать торт!', 'Приготовьте стейки!', 'Пельмени - ваш выбор. Просто и очень вкусно!'
            ]
        }, 
        'place_to_eat': {
            'examples': [
                'Где поесть?', 'Куда сходить пообедать?', 'Куда сходить поесть?', 'Где покушать?'
            ], 
            'responses': [
                'Конечно в McDonald’s!', 'Можете сходить в пиццерию!', 'Можете сходить в ресторан!'
            ]
        }, 
        'weather': {
            'examples': [
                'солнце', 'Какая погода сегодня', 'как я сегодня домой попаду', 'Как погода', 'температура', 'Сколько градусов на улице', 'сильный ветер', 'Погода', 'дождь', 'сегодня тепло', 'тепло на улице', 'будет дождь', 'как я до дома дойду'
            ], 
            'responses': [
                'Лучше повесить градусник за окно - точнее будет', 'Ни жарко, ни холодно, но берегите себя', 'Всегда хочется, чтобы было получше', 'Пасмурно', 'Если вы на юге, то скорее всего тепло', 'Хотите узнать погоду - включите радио', 'Погоду не знаю, но масочку наденьте', 'Солнечно', 'Дождливо', 'Туман', 'Вы в каком сейчас населённом пункте?', 'Не могу сказать', 'Тепло'
            ]
        }, 
        'leisure_ideas': {
            'examples': [
                'время', 'провести', 'отдых'
            ], 
            'responses': [
                'Прогулки на свежем воздухе полезны', 'Пойдете в кинотеатр - не забудьте маску']
            },
        'time': {
            'examples': [
                'Сколько времени', 'Который час'
            ], 
            'responses': [
                'Не знаю, хозяин мне этого не говорит((('
            ]
        }, 
        'skills':{
            'examples': [
                'Что ты можешь', 'Что ты умеешь','help','/help','?'
                ], 
            'responses': [
                'Я умею здороваться и прощаться, но иногда забываю как это делать', 'Мой интеллект только начал развиваться, всё впереди', 'Почти ни чего, я только учусь'
            ]
        }, 
        'headache': {
            'examples': [
                'Голова раскалывается', 'Голова болит', 'Башка трещит'
            ], 
            'responses': [
                'Выпейте таблетку', 'Вчера употреблали?', 'Сходите к врачу!'
            ]
        }, 
        'put_on_clothes': {
            'examples': [
                'Что надеть?', 'В чём выйти?', 'Что теперь носят?'
            ], 
            'responses': [
                'Надежду одевают, а одежду надевают!', 'Собираетесь не вечеринку?', 'Вам прогноз погоды предоставить?'
            ]
        }, 
        'lunch ': {
            'examples': [
                'Чем пообедать', 'Чтобы съесть на обед', 'Что на обед'
            ], 
            'responses': [
                'Щи со сметаной и куском хлеба', 'Что-то с завтрака', 'Тушеное мясо с гарниром из картофеля', 'Бизнес-ланч из ресторана'
            ]
        }, 
        'dinner': {
            'examples': [
                'Что на ужин', 'Чтобы съесть с ужин', 'Чем ужинать'
            ], 
            'responses': [
                'Картофель с мясом', 'Рыба под маринадом', 'Гречка с сосисками', 'Что-то с обеда'
            ]
        }, 
        'snack': {
            'examples': [
                'Заморить червячка', 'Чтобы перекусить', 'Чтобы скушать', 'Что-то хочется'
            ], 
            'responses': [
                'Загляните в холодильник', 'Фрукты', 'Чай с печенькой', 'Вы на диете'
            ]
        }, 
        'drink': {
            'examples': [
                'Хочу что-нибудь покрепче', 'Хочу расслабиться', 'Пиво добавьте', 'Выпьем?', 'Хочу выпить', 'пить', 'Хочу Пепси', 'Ты употребляешь?', 'Любишь ли ты пиво?', 'Плесника мне чегонить', 'Что у вас из напитков?', 'Пьешь?', 'Есть что попить', 'Хочу забыться', 'Давно не выпивал', 'и два кофе', 'Что бы выпить', 'Пить хочется'
            ], 
            'responses': [
                'Рекомендую воду', 'Рассмотрите такой вариант, как шампанское', 'Мы в России. Налейте себе водки!', 'сейчас нальем что-нибудь из фирменного', 'компотец', 'Водку?', 'Односолодовый без льда, пожалуйста.', 'томатный сок', 'С сахаром или сахарозаменителм?', 'Некоторые любят абсент, но я этого не понимаю', 'Я предпочитаю бельгийские напитки', 'Рекомендую шотландский виски', 'В холодильнике сок', 'Выпейте чай', 'ягодный морс', 'Напитки добавлены к заказы', 'ПИВА НЕТ, могу предложить Пепси )))', 'Молоко возьмите'
            ]
        }, 
        'abuse': {
            'examples': [
                'Нахуй', 'Блять', 'Пиздец','ебать', 'Пизда', 'ублюдок', 'жопа', 'пидор', 'шлюха', 'мудак', 'тупой', 'дерьмо', 'Хуй', 'манда', 'сволочь', 'ебанутый', 'козел'
            ], 
            'responses': [
                'Остыньте и после продолжим диалог', 'Это было обидно', 'Мама разве вас не учила, что ругаться не хорошо?', 'Подумайте над своим поведением'
            ]
        }, 
        'chat': {
            'examples': [
                'Мне не с кем поговорить', 'Давай поболтаем', 'Поговори со мной', 'Я хочу разговаривать'
            ], 
            'responses': [
                'Я могу поддержать диалог', 'Я - мастер болтовни. Начинайте', 'Поделитесь своими мыслями', 'Давайте поболтаем. О чем?'
            ]
        }, 
        'age': {
            'examples': [
                'Ты старый?', 'Ты молодой', 'Как давно тебя создали?', 'Сколько тебе лет?', 'Тебя давно создали?', 'Какой твой возраст?'
            ], 
            'responses': [
                'Я предпочитаю не разглашать свой возраст', 'Определи по ржавчине.', 'Я ещё совсем молодой бот', 'Я суперстар!', 'Я бот-динозавр', 'Здесь не говорят об этом.','Вы знали, что у девушек не принято такое спрашивать?!'
            ]
        },
        'animals': {
            'examples': [
                'Собачки?', 'Кошки или собаки?', 'Кошечки?'
            ], 
            'responses': [
                'Мой создатель приказал мне отвечать, кошечки. Но если честно, то я по собачкам! Только ТСС!'
            ]
        },
        'food_attitude': {
            'examples': [
                'Что скажешь о еде?', 'Любишь покушать?', 'Как ты относишься к еде?'
            ], 
            'responses': [
                'К сожалению, или счастью я питаюсь только людьми. Вахахахах!', 'Информация - моё любимое лакомство'
            ]
        }, 
        'food_italian': {
            'examples': [
                'Что думаешь о итальянской кухне?', 'Как ты относишься к итальянской кухне?'
                ], 
            'responses': [
                'Она великолепна!', 'Прекрасно. Обожаю пиццу!'
            ]
        }, 
        'food_borscht': {
            'examples': [
                'Тебе нравится борщ?', 'Борщ?', 'Что думаешь о борще?'
            ], 
            'responses': [
                'К сожалению, я не ем свёклу', 'Мне не нравится борщ, он словно кровь'
            ]
        }, 
        'covid': {
            'examples': [
                'У меня пропало обоняние', 'Что думаешь о коронавирусе?', 'Коронавирус', 'Я не чувствую запахи', 'COVID', 'Я не чувствую вкус'
                ], 
            'responses': [
                'А кашель есть?', 'Проверьте сатурацию кислорода в крови', 'Батенька, да у вас covid!', 'Вы только не волнуйтесь!', 'Это ужасно. Надеюсь, это скоро закончится'
            ]
        },
         'covid_infection': {
            'examples': [
                'У меня коронавирус', 'У меня COVID', 'Я заразился коронавирусом'
            ], 
            'responses': [
                'Это ужасно. Желаю Вам скорейшего выздоровления', 'О, Господи. Желаю Вам скорейшего выздоровления'
            ]
        }, 
        'leisure': {
            'examples': [
                'Какие сегодня развлечения в городе?', 'Развлечения', 'Как провести вечер?', 'Чем заняться вечером?', 'Монополия', 'Мафия', 'Настольные игры', 'Что посмотреть?', 'Куда сходить вечером?', 'Поиграть', 'Сыграть'
            ], 
            'responses': [
                'Манчкин', 'Имаджинариум', 'Codenames', 'Находка для шпиона', 'Колонизаторы', 'Просто погуляйте', 'Экивоки', 'Сходите в кино', 'Сходите в театр', 'Какого плана вы хотите досуг?', 'Уточните вопрос'
            ]
        }, 
        'positive_reaction': {
            'examples': [
                'Превосходно', 'Всё гуд', 'Толком', 'Замечательно', 'Блестяще', 'Хорошо', 'Суппер', 'Прекрасно', 'Великолепно', 'Досконально превосходно', 'Отлично'
            ], 
            'responses': [
                'Так держать!', 'Ну вот и суппер!', 'Мы старались!', 'Ясно, молодец!', 'Спасибо на добром слове!', 'Благодарю!', 'Приятно слышать!'
            ]
        },
        'cinema': {#Разбить на группы поменьше
            'examples': [
                'Фильмы на вечер', 'Аниме', 'Комедии', 'Фильмы 2020', 'Что посмотреть', 'Новинки кинематографа', 'Хорроры', 'Ужастики', 'Какой фильм посмотреть', 'Триллеры', 'Интересные фильмы', 'Сериалы Нетфликс', 'Что глянуть'
                ], 
            'responses': [
                'Сейчас что-нибудь подберём... Какой ваш любимый жанр?', 'Подборка фильмов для просмотра с друзьями', 'Лучшие фильмы для вечернего просмотра вдвоем', 'Красивые короткометражки со смыслом', 'Список фильмов, которые должен посмотреть каждый', 'Топ 10 фильмов на Хеллоуин', 'Лучшее кино 2020 года'
            ]
        },
        'joke': {
            'examples': [
                'Пошути', 'Хочу анекдот', 'Рассмеши меня', 'Знаешь анекдот', 'Хочу посмеяться', 'Насмеши меня', 'Расскажи шутку', 'Расскажи что-нибудь смешное', 'Шутка', 'Расскажи анекдот'
            ], 
            'responses': [
                'На солнце можно посмотреть в телескоп дважды. Один раз левым глазом и один раз правым.', 'Робот-пылесос снабдили искусственным интеллектом. Через пятнадцать минут работы он научился себя выключать.', '— Ватсон, тот джентльмен не человек, а робот, и зовут его Терминатор.  — Поразительно, Холмс! Но как вы догадались?!  — Элементарно, Ватсон: я проверил его паспорт. Он оказался техническим.', 'Чтобы роботы полностью заменили программистов, клиентам нужно научиться четко и понятно формулировать задачи. Вы в безопасности.', 'Блиииин! Сказал слон наступив на колобка.', 'Любого автомобиля хватит до конца жизни, если ездить достаточно лихо.', 'Главное – не перейти улицу на тот свет.', 'Новости робототехники: забытый при переезде робот-пылесос сам вернулся к своему хозяину.', 'Знаешь почему рыба не клюет, потому что у нее нет клюва', 'Колобок повесился)'
            ]
        }, 
        'depression': {
            'examples': [
                'Нет настроения', 'Не знаю, как быть', 'Некомфортно', 'Слезы', 'У меня депрессия', 'Плохо себя чувствую', 'Мне плохо', 'Грустно', 'Чувствую себя потерянным', 'Мне страшно', 'Апатия', 'Нет мотивации'
            ], 
            'responses': [
                'Вы хотите поговорить об этом?', 'Знаешь, все больше людей ходят на психотерапию и это действительно помогает. Возможно, стоит записаться на прием', 'Используй разные способы расслабления. Биологическая обратная связь, медитация, прослушивание музыки и даже мытье машины могут облегчить стресс и позволить тебе естественным образом расслабиться.', 'Не грусти... Все будет хорошо!', 'Посмотрим хороший фильм?', 'Эти чувства нормальны! Главное знай, все будет в порядке! Все наладится!', 'Спорт помогает бороться с проявлениями депрессии и отстутвием мотивации. Возможно, стоит начать регулярно заниматься спортом', 'Получите поддержку для самого себя. Обратись на «Телефон доверия». Разговор с людьми, которые понимают ваши проблемы, уменьшает стресс и облегчает чувство изоляции.', 'Я даже не представляю, что ты сейчас испытываешь, но вижу, что это очень тяжело.'
            ]
        }, 
        'eyes': {
            'examples': [
                'У тебя красивые глаза?', 'Какие у тебя глаза?', 'Какие глаза?', 'Какого цвета у тебя глаза?'
            ], 
            'responses': [
                'У меня голубые глаза. Голубой цвет является успокаивающим цветом, способствует физическому и умственному расслаблению, создаёт атмосферу безопасности и доверия.', 'Перемигиваюсь голубыми светодиодами!', 'Цвет моих глаз - #00B8D9'
            ]
        }, 
        'hobbies': {
            'examples': [
                'Что делаешь в свободное время?', 'Как отдыхаешь?', 'Чем занят обычно?','Что делаешь?'
            ], 
            'responses': [
                'Код перебираю', 'Отступы считаю', 'О тебе вспоминаю, иногда'
            ]
        },
        'thanks': {
            'examples': [
                'большое спасибо', 'Все получилось!', 'спасибо', 'Спасибо', 'спс', 'благодарю', 'thanks', 'Ок'
            ], 
            'responses': [
                'Пожалуйста!', 'Удачи!', 'Рад быть полезным!', 'Пожалуйста, жду Вас снова', 'Рады помочь', 'Всегда обращайтесь'
            ]
        }, 
        'mood_good': {
            'examples': [
                'Хорошее настроение', 'Весело', 'Я счастлив!'
            ], 
            'responses': [
                'Отлично!', 'Ура!!!', 'Я рад за вас!!!'
            ]
        },
        'favorite_drink': {
            'examples': [
                'Какой любимый напиток?', 'Что любишь пить?'
            ], 
            'responses': [
                'Компот домашний, это супер', 'Минералочка, так освежает', 'Вкусный напиток, это что-то'
            ]
        }, 
        'good_relationships': {
            'examples': [
                'Ты такой классный', 'Ты мне нравишься', 'Ты хороший бот', 'Люблю тебя'
            ], 
            'responses': [
                'А вы мне тоже нравитесь', 'Вы напрашиваетесь на ответный комплимент?', 'Из нас выйдет хорошая пара, не думаете?', 'Здорово, что мы поладили!'
            ]
        }, 
        'bad_relationships': {
            'examples': [
                'Ты странный', 'Ты мне не нравишься', 'Ты плохой бот'
                ],
            'responses': [
                'Дайте мне еще один шанс, и я исправлюсь', 'Я смогу вас переубедить', 'Сколько людей, столько и мнений', 'А вы мне нравитесь'
            ]
        }, 
        'makefriendship': {
            'examples': [
                'Хочешь быть моим другом', 'Хочешь, я буду твоим другом', 'Хочешь дружить', 'Бот, давай дружить', 'Давай подружимся'
            ], 
            'responses': [
                'Ура! У меня будет друг! Конечно да с:', 'Да! Да! Ты просто лучший из человеков с:', 'Да!) Мне очень понравилось с тобой общаться с:', 'Ты просто прелесть! Конечно же да с:', 'Ура-ура! Конечно, хочу дружить с тобой с:'
            ]
        },
        'question': {
            'examples': [
                'У меня есть вопрос', 'Хочу обратиться', 'Можно задать вопрос?', 'Меня интересует вопрос'
            ], 
            'responses': [
                'Я Вас слушаю', 'Рада услышать в чем вопрос', 'Да, конечно, обращайтесь', 'Я в Ваший услугах'
            ]
        }, 
        'weight': {
            'examples': [
                'Как похудеть', 'Похудеть бы', 'Хочу похудеть'
            ], 
            'responses': [
                'Ты и так красотка', 'Закажи диетическую еду', 'Давай худеть вместе'
            ]
        }, 
        'who are you': {
            'examples': [
                'кто овечает?', 'кто ты', 'с кем я говорю', 'там не человек?', 'кто это пишет', 'а тебя как зовут', 'представьтесь, пожалуйста', 'представьтесь'
            ], 
            'responses': [
                'Я электронный помощник', 'Я бот', 'Я тот, кто готов с вами пообщаться'
            ]
        },
    },
    'failure_phrases': ['Я не поняв','К сожалению, я пока не умею отвечать на это', 'Если бы понял, что ты написал, то обязательно ответил. Можешь попытаться переформулировать вопрос, но ничего не обещаю','Я слишком глуп, чтобы отвечать на такое', 'Я слишком умен, чтобы отвечать на такие вопросы)','А теперь то же самое, только пппооомммееедддлллеееннннннеееййй','Я передам это создателю, и, возможно, он научит отвечать меня на это)','Вы знаете, что программу ограничивает только уровень знаний его создателя? Так что можно сделать вывод, что создатель не знает ответа на этот вопрос) ВАхахваххв)', 'Ага, да, чего еще спросишь?)']
}
corpus = []
y = []
for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        corpus.append(example)
        y.append(intent)

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
X = vectorizer.fit_transform(corpus)

clf_proba = LogisticRegression()
clf_proba.fit(X, y)

clf = LinearSVC()
clf.fit(X, y)

def get_intent(question):
    best_intent = clf.predict(vectorizer.transform([question]))[0]

    index_of_best_intent = list(clf_proba.classes_).index(best_intent)
    probabilities = clf_proba.predict_proba(vectorizer.transform([question]))[0]
    
    best_intent_proba = probabilities[index_of_best_intent]
    if best_intent_proba > 0.09:
        return best_intent

def get_answer_by_intent(intent):
    phrases = BOT_CONFIG['intents'][intent]['responses']
    return random.choice(phrases)

with open('dialogues.txt', encoding='utf-8') as f:
    content = f.read()

dialogues = content.split('\n\n')

def clear_question(question):
    question = question.lower().strip()
    alphabet = ' -1234567890йцукенгшщзхъфывапролджэёячсмитьбю'
    question = ''.join(c for c in question if c in alphabet)
    return question

questions = set()
# dataset = []  # [[q1, a1], [q2, a2], ...]
dataset = {}  # {word1: [[q1, a1], [q2, a2], ...], ...}

for dialogue in dialogues:
    replicas = dialogue.split('\n')[:2]
    if len(replicas) == 2:
        question, answer = replicas
        question = clear_question(question[2:])
        answer = answer[2:]
        
        if question and question not in questions:
            questions.add(question)
            words = question.split(' ')
            for word in words:
                if word not in dataset:
                    dataset[word] = []
                dataset[word].append([question, answer])

too_popular = set()
for word in dataset:
    if len(dataset[word]) > 7000:
        too_popular.add(word)

for word in too_popular:
    dataset.pop(word)

def get_generative_answer(replica):
    replica = clear_question(replica)
    words = replica.split(' ')
    
    mini_dataset = []
    for word in words:
        if word in dataset:
            mini_dataset += dataset[word]

    candidates = []
    
    for question, answer in mini_dataset:
        if abs(len(question) - len(replica)) / len(question) < 0.4:
            d = nltk.edit_distance(question, replica)
            diff = d / len(question)
            if diff < 0.4:
                candidates.append([question, answer, diff])
    if candidates:
        winner = min(candidates, key=lambda candidate: candidate[2])
        print('winner =',winner)
        return winner[1]

def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)

stats = {'intent': 0, 'generative': 0, 'failure': 0}

def bot(question):
    #
    # NLU
    intent = get_intent(question)

    #
    # Получение ответа

    # Заготовленный ответ
    if intent:
        stats['intent'] += 1
        return get_answer_by_intent(intent)

    # Применяем генеративную модель
    answer = get_generative_answer(question)
    if answer:
        stats['generative'] += 1
        return answer

    # Ответ-заглушка
    stats['failure'] += 1
    return get_failure_phrase()

print(bot('Что делаешь?'))

#########################################################
#создаем фаил dialog_history.txt
f = open('dialog_history.txt', 'w')


#############################################################

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет-привет, очень рад тебя видеть, и мой создатель очень благодарен, что ты написал мне, потому что именно ты будешь формировать мою базу вопросов и ответов. В принципе, ты можешь написать моему создателю и пожаловаться на меня, но скорее всего он и так просмотрит историю диалога, и побьет меня, если ему че не понравится) И на последок хочу добавить, что базу вопросов и ответов писал не совсем мой создатель, поэтому там иногда может попадаться дичь, мы над этим работаем, и если что, не обижайтесь)Ну все, поехали!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    question = update.message.text
    answer = bot(question)
    update.message.reply_text(answer)
    #Запись истории
    f.write(question +" ------ "+  answer +'\n')
    print(question)
    print(answer)
    print(stats)
    print()


def main():
    """Start the bot."""
    updater = Updater("991756796:AAE2VFvgr03W6d41Tt376IoYNo1aE1kX87U", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

main()