from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from crud_functions import initiate_db, get_all_products, seed_db

# Initialize the bot and dispatcher
bot = Bot(token='')  # Замените на ваш действительный токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Initialize the database
initiate_db()


# seed_db()  # Закомментируйте эту строку, если не хотите каждый раз заполнять базу данных

# Define user states for FSM
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Handler for the "Купить" button
@dp.message_handler(text='Купить')  # Обработчик для кнопки "Купить"
async def get_buying_list(message: types.Message):
    products = get_all_products()  # Получаем список продуктов из базы данных

    for name, description, price, image_url in products:
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text=f'Купить {name}', callback_data='product_buying'))

        # Отправка сообщения с фотографией и описанием продукта
        await message.answer_photo(photo=image_url, caption=f"{name}\n{description}\nЦена: {price} рублей",
                                   reply_markup=inline_keyboard)


# Handler for product buying confirmation
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Handler for displaying formula
@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
    await call.answer()


# Handler for starting the calorie input process
@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.answer('Введите свой возраст:')
    await call.answer()


# FSM handler for age input
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.reply('Введите свой рост (в см):')


# FSM handler for growth input
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.reply('Введите свой вес (в кг):')


# FSM handler for weight input and final confirmation
@dp.message_handler(state=UserState.weight)
async def calculate_bmr(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    user_data = await state.get_data()
    age = user_data.get('age')
    growth = user_data.get('growth')
    weight = user_data.get('weight')

    # Простая формула для расчета BMR (можно изменить на более точную)
    bmr = 10 * float(weight) + 6.25 * float(growth) - 5 * int(age) - 161
    await message.reply(f"Ваш BMR: {bmr:.2f} калорий в день.")

    # Завершение состояния
    await state.finish()


# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
