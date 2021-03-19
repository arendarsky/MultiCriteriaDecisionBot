import command_names
from telegram import KeyboardButton, ReplyKeyboardMarkup

main_menu_keyboard = [[KeyboardButton(command_names.pareto)],
                      [KeyboardButton(command_names.weighted_sum)],
                      [KeyboardButton(command_names.ideal_point)]]
reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                      resize_keyboard=True,
                                      one_time_keyboard=True)