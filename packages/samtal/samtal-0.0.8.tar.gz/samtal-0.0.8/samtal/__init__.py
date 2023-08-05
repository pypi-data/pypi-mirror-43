import os

from samtal.adapters.answer_sqlite import SqlAnswerRepository
from samtal.adapters.conversation_mattermost import MattermostConversationProvider
from samtal.core.bot import Bot
from samtal.core.questions import load_questions_from_file
from samtal.core.team_members import load_members_from_file

ROOT_DIR = os.path.dirname(__file__)


def abs_path(rel_path: str):
    path = ROOT_DIR
    if not (rel_path.startswith("/") or rel_path.startswith("\\")):
        path += "/"

    return path + rel_path


def default_bot(
        mattermost_host: str,
        mattermost_bot_user: str,
        mattermost_bot_password: str,
        question_yml_file: str = "default/questions.yml",
        members_yml_file="default/members.yml",
        sqlite_db: str = ":memory:") -> Bot:
    questions = load_questions_from_file(abs_path(question_yml_file))
    members = load_members_from_file(abs_path(members_yml_file))

    answer_repository = SqlAnswerRepository("sqlite", filename=sqlite_db)
    conversation_provider = MattermostConversationProvider(host=mattermost_host,
                                                           login=mattermost_bot_user,
                                                           password=mattermost_bot_password)

    return Bot(answer_repository, conversation_provider, members, questions)
