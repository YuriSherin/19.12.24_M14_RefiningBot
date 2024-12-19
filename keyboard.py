from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_calc = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(button_calc, button_info)
kb_start.row(button_buy)

kb_calc = InlineKeyboardMarkup(resize_keyboard = True)
button_inline_calc = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_inline_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
kb_calc.row(button_inline_calc, button_inline_formulas)

kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button_inline_buy_product1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_inline_buy_product2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_inline_buy_product3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_inline_buy_product4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb_buy.row(button_inline_buy_product1, button_inline_buy_product2, button_inline_buy_product3, button_inline_buy_product4)