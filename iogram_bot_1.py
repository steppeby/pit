from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
from detskiy_mir_parser import parser
import pandas


# WARNING BROKEN CODE !
# WARNING BROKEN CODE !
# WARNING BROKEN CODE !


TOKEN='#'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id,"Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    await bot.send_message(msg.from_user.id,"Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@dp.message_handler(commands=['parse'])
async def process_parse_command(msg: types.Message):
    #await bot.send_message(msg.from_user.id, 'Начинаю парсить...')
    parser('C:/Users/Jean/PycharmProjects/workspace/venv/')
    #await bot.send_message(msg.from_user.id, 'Выбрал директорию...')
    # with open('C:/Users/Jean/PycharmProjects/workspace/venv/detskiy_mir_data.xlsx') as datafile:
    #await bot.send_message(msg.from_user.id, 'Открыл файл...')
    f = pandas.read_excel('C:/Users/Jean/PycharmProjects/workspace/venv/detskiy_mir_data.xlsx')
    #await bot.send_message(msg.from_user.id, 'Прочитал файл...')
    await bot.send_document(msg.from_user.id,f)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
