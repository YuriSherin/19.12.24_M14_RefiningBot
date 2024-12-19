from imghdr import tests

import info
import keyboard
from user_state import UserState

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


bot = Bot(info.token_tg_bot)      # создаем объект бота
dp = Dispatcher(bot, storage=MemoryStorage())   # создаем объект диспетчера


@dp.message_handler(commands=['start'])         # отслеживаем команду старт
async def start(message:types.Message):
    """Функция выполняет команды старт.
    Выводит приветствие и две кнопки"""
    msg = f'Привет {message["from"]["first_name"]}!'
    await message.reply(msg, reply_markup=keyboard.kb_start)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    """Функция при клике по кнопке Купить выводит описание и картинку четырех продуктов,
      и показывает inline keyboard с текстами Продукт 1, Продукт 2, Продукт 3, Продукт 4."""
    for i in range(1, 5):
        s = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        with open(f'images/product{i}.jpg', 'rb') as img:
            await message.answer_photo(img, s)
    await message.answer('Выберите продукт для покупки',  reply_markup=keyboard.kb_buy)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    """Асинхронная функция обратного вызова выводит сообщение"""
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()     # обязательно закрываем сам вызов call


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    """Функция при клике по кнопке Рассчитать выводит сообщение
    и показывает inline keyboard с текстами
    Рассчитать норму калорий и Формулы расчёта"""
    await message.answer('Выберите опцию', reply_markup=keyboard.kb_calc)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    """Функция обратного вызова при клике на кнопку Рассчитать норму калорий
    выводит сообщение и удаляет ReplyKeyboard"""
    msg = (f'{call.message["chat"]["first_name"]}! Сейчас я помогу Вам рассчитать суточную норму потребления калорий.\n'
           f'\nВведите свой возраст, лет:')
    await call.message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    await UserState.AGE.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    """Функция обратного вызова при клике по кнопке Формулы расчёта
    выводит сообщение с формулами расчета"""
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора:\n\b'\
        'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'\
        'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.message_handler(text='Информация')          # клик по кнопке информация
async def inform(message:types.Message):
    """Функция выполняет команду вывода информации"""
    msg = inforatin = ('Для расчета суточной нормы потребления калорий используется формула Миффлина-Сан Жеора\n'\
             '\nФормула Миффлина-Сан Жеора – это одна из самых последних формул расчета калорий '\
             'для оптимального похудения или сохранения нормального веса.'\
             '\nОна была выведена в 2005 году и все чаще стала заменять классическую формулу Харриса-Бенедикта.\n'\
             '\nУпрощенный вариант формулы Миффлина-Сан Жеора:'\
             '\nдля мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'\
             '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await message.answer(msg)


@dp.message_handler(state=UserState.AGE)
async def set_growth(message: types.Message, state:FSMContext):
    """Функция проверяет на корректность введенный пользователем возраст,
    сохраняет его в машине состояний и предлагает пользователю ввести свой рост.
    При выявлении ошибки просит пользователя повторить ввод своего возраста"""
    age = message.text      # возраст
    try:
        if not age.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
            msg = 'Ошибка! Неверно ввели возраст! Для указания своего возраста используйте только цифровые символы.\n'\
                   '\nВведите свой возраст, лет:'
            raise ValueError(msg)

        if int(age) < 13 or int(age) > 80:
            msg = 'Ошибка! Неверно ввели возраст! Возраст указывается в диапазоне от 13 до 80 лет.\n'\
            '\nВведите свой возраст, лет:'
            raise ValueError(msg)

        # если возраст введен корректно
        await state.update_data(AGE=age)
        await message.answer('Введите свой рост, см:')
        await UserState.GROWTH.set()

    except ValueError as e:     # выводим сообщение об ошибке введенных данных и просим повторить ввод
        await message.answer(e)
        await UserState.AGE.set()



@dp.message_handler(state=UserState.GROWTH)  # декоратор, указывает, что функция будет реагировать на state=UserState.growth
async def set_weight(message, state):
    """Функция проверяет на корректность введенный пользователем рост,
    сохраняет его в машине состояний и предлагает пользователю ввести свой вес.
    При выявлении ошибки просит пользователя повторить ввод своего роста"""
    growth = message.text   # рост
    try:
        if not growth.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
            msg = 'Ошибка! Неверно ввели рост! Для указания своего роста используйте только цифровые символы.\n' \
                  '\nВведите свой рост, см.:'
            raise ValueError(msg)

        if int(growth) < 100 or int(growth) > 250:
            msg = 'Ошибка! Неверно ввели свой рост! Укажите рост в диапазоне от 100 до 250 см.\n' \
                  '\nВведите свой рост, см.:'
            raise ValueError(msg)

        # если рост введен корректно
        await state.update_data(GROWTH=growth)
        await message.answer('Введите свой вес, кг.:')
        await UserState.WEIGHT.set()

    except ValueError as e:     # выводим сообщение об ошибке введенных данных и просим повторить ввод
        await message.answer(e)
        await UserState.GROWTH.set()


@dp.message_handler(state=UserState.WEIGHT)  # декоратор, указывает, что функция будет реагировать на state=UserState.weight
async def send_calories(message, state):
    """Функция проверяет на корректность введенный пользователем вес,
    сохраняет его в машине состояний и на основании введенных пользователем данных
    производит расчет количества суточной нормы потребления калорий.
    При выявлении ошибки просит пользователя повторить ввод своего роста"""
    weight = message.text       # вес
    try:
        if not weight.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
            msg = 'Ошибка! Неверно ввели вес! Для указания своего веса используйте только цифровые символы.\n' \
                  '\nВведите свой вес, кг.:'
            raise ValueError(msg)

        if int(weight) < 30 or int(weight) > 150:
            msg = 'Ошибка! Неверно ввели свой вес! Укажите вес в диапазоне от 30 до 150 кг.\n' \
                  '\nВведите свой вес, кг.:'
            raise ValueError(msg)

        await state.update_data(WEIGHT=weight)
        data = await state.get_data()  # получим наши данные из машины состояний

        # получим из машины состояний введенные ранее значения
        age = int(data['AGE'])
        growth = int(data['GROWTH'])
        weight = int(data['WEIGHT'])

        # рассчитаем суточную норму потребления калорий для мужчин и для женщин
        calories_men = 10 * weight + 6.25 * growth - 5 * age + 5
        calories_women = 10 * weight + 6.25 * growth - 5 * age - 161

        # сформируем сообщение для пользователя и выведем его в Телеграмм
        msg = f'Суточная норма калорий:\n    Для мужчин: {str(calories_men)},\n    Для женщин: {str(calories_women)}'
        await message.answer(msg)

        await state.finish()  # очистим данные в UserState и завершим работу с машиной состояний
        await message.answer('\nДля повторения расчета введите команду "/start"')

    except ValueError as e:     # выводим сообщение об ошибке введенных данных и просим повторить ввод
        await message.answer(e)
        await UserState.GROWTH.set()


@dp.message_handler()  # декоратор для обработки любых текстовых сообщений
async def all_messages(message):
    """Асинхронный метод отправки эхо-сообщений"""
    # msg = message.text[::-1]
    msg = 'Команда не определена. Введите команду "/start", что бы начать общение'
    await message.answer(msg)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
