import logging
import os

from samtal.adapters.answer_sqlite import SqlAnswerRepository
from samtal.adapters.conversation_mattermost import MattermostConversationProvider
from samtal.core.bot import Bot, infinite_ticker
from samtal.core.questions import Questions, load_questions_from_file
from samtal.core.team_members import Members, load_members_from_file


def main():
    root_dir = os.path.dirname(__file__)
    print(root_dir)
    questions: Questions = load_questions_from_file(root_dir + "/default/questions.yml")
    members: Members = load_members_from_file(root_dir + "/default/members.yml")

    bot_user = os.environ.get("BOT_USER")
    bot_password = os.environ.get("BOT_PASSWORD")
    db_file = os.environ.get("BOT_DB_FILE", ":memory:")

    answer_repository = SqlAnswerRepository("sqlite", filename=db_file)
    conversation_provider = MattermostConversationProvider(host="framateam.org", login=bot_user,
                                                           password=bot_password)

    bot = Bot(answer_repository, conversation_provider, members, questions)

    bot.run(infinite_ticker)


if __name__ == '__main__':
    logging.root.setLevel(10)
    main()
