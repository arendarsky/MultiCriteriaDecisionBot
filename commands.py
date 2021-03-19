import command_names
import multi_criteria_methods as mcm
import data_interactions as di


def get_result(chat_id, method, tg_bot):
    df = di.get_df(chat_id)
    rdf = method(df)
    path = di.save_result(chat_id, rdf)
    send_result_file(chat_id, path, tg_bot)


def send_result_file(chat_id, path, tg_bot):
    f = open(path, "r")
    tg_bot.send_document(chat_id=chat_id, document=f, filename="result.csv")
    f.close()


def pareto(update, context):
    get_result(update.effective_chat.id, mcm.pareto_set, context.bot)


def weighted_sum(update, context, weights):
    df = di.get_df(update.effective_chat.id)
    rdf = mcm.weighted_sum(df, weights)
    path = di.save_result(update.effective_chat.id, rdf)
    send_result_file(update.effective_chat.id, path, context.bot)


def weighted_sum_message(update, context):
    df = di.get_df(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Укажите веса (" + str(
        len(df.columns)) + " штук) для критериев одним сообщением в формате \"[0.1, 0.2, ...]\"")


def ideal_point(update, context):
    get_result(update.effective_chat.id, mcm.ideal_point_method, context.bot)


commands = {
    command_names.pareto: pareto,
    command_names.weighted_sum: weighted_sum_message,
    command_names.ideal_point: ideal_point
}
