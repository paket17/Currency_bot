from auth import token_auth
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from parse_rate import print_usd, print_eur


async def on_startup(_):
    print('Bot is running')


class Form(StatesGroup):
    data = State()


bot = Bot(token_auth, parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Курс USD'))
kb.add(KeyboardButton('Курс EUR'))

kb_u = ReplyKeyboardMarkup(resize_keyboard=True)
kb_u.add(KeyboardButton('USD на сегодня'))
kb_u.add(KeyboardButton('USD по дате'))

kb_e = ReplyKeyboardMarkup(resize_keyboard=True)
kb_e.add(KeyboardButton('EUR на сегодня'))
kb_e.add(KeyboardButton('EUR по дате'))

flag: int = 0


@dp.message_handler(commands=['start', 'help'])
async def desc_mes(message: types.Message):
    await message.answer("Привет! Я бот показывающий курс Евро и Доллара на сегодня и на выбраную дату.",
                         reply_markup=kb)


@dp.message_handler()
async def question(message: types.Message):
    global flag
    if message.text == 'Курс USD':
        await message.answer("Какой курс USD хотите узнать, на сегодня или на выбраную дату?", reply_markup=kb_u)
    elif message.text == 'USD на сегодня':
        await message.answer(print_usd())
        await message.answer('Курс какой валюты хотите узнать?', reply_markup=kb)
    elif message.text == 'USD по дате':
        await message.answer('Укажите дату. Пример - "15.10.2010"\nДля отмены нажмите /cancel',
                             reply_markup=types.ReplyKeyboardRemove())
        flag = 1
        await Form.data.set()

    elif message.text == 'Курс EUR':
        await message.answer("Какой курс EUR хотите узнать, на сегодня или на выбраную дату?", reply_markup=kb_e)
    elif message.text == 'EUR на сегодня':
        await message.answer(print_eur())
        await message.answer('Курс какой валюты хотите узнать?', reply_markup=kb)
    elif message.text == 'EUR по дате':
        await message.answer('Укажите дату. Пример - "15.10.2010"\nДля отмены нажмите /cancel',
                             reply_markup=types.ReplyKeyboardRemove())
        flag = 2
        await Form.data.set()
    else:
        await message.answer('Простите, я не понял вас.\nЯ умею показывать курсы валют, выберите валюту USD или EUR.')


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Курс какой валюты хотите узнать?', reply_markup=kb)


@dp.message_handler(state=Form.data)
async def info(message: types.Message, state: FSMContext):
    try:
        global flag
        async with state.proxy() as data:
            data['data'] = message.text
        await state.finish()
        if flag == 1:
            await message.answer(print_usd(data['data']))
            flag = 0
            await message.answer('Курс какой валюты хотите узнать?', reply_markup=kb)
        elif flag == 2:
            await message.answer(print_eur(data['data']))
            flag = 0
            await message.answer('Курс какой валюты хотите узнать?', reply_markup=kb)

    except IndexError:
        await message.answer('Дата введена не верно, пожалуйста попробуйте еще раз. Пример - "15.10.2010"'
                             '\nДля отмены нажмите /cancel')
        await Form.data.set()
    except ValueError:
        await message.answer('Дата введена не верно, пожалуйста попробуйте еще раз. Пример - "15.10.2010"'
                             '\nДля отмены нажмите /cancel')
        await Form.data.set()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
