import random
from pathlib import Path

from otree.api import *

doc = """
Questionnaires
"""
app_name = Path(__file__).parent.name


def relevant_likert():
    return [
        (0, "まったく関係ない（この要素は私の善悪判断と無関係である）"),
        (1, "あまり関係ない"),
        (2, "少し関係がある"),
        (3, "やや関係がある"),
        (4, "とても関係がある"),
        (5, "非常に関係がある"),
    ]


def agreement_likert():
    return [
        (0, "強く反対する"),
        (1, "やや反対する"),
        (2, "少し反対する"),
        (3, "少し賛成する"),
        (4, "やや賛成する"),
        (5, "強く賛成する"),
    ]


class C(BaseConstants):
    NAME_IN_URL = "whquest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # ----- questionnaire 1 -----
    fairness_1 = models.IntegerField(
        label="... 誰かが不公平に行動したかどうか",
        choices=relevant_likert(), widget=widgets.RadioSelect())
    fairness_2 = models.IntegerField(
        label="... 誰かが自分の権利を奪われたかどうか", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    fairness_3 = models.IntegerField(
        label="正義は社会にとって最も重要な要件である", choices=agreement_likert(),
        widget=widgets.RadioSelect())
    loyalty_1 = models.IntegerField(
        label="... 誰かが自分の集団を裏切るような行動をしたかどうか", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    loyalty_2 = models.IntegerField(
        label="... 誰かが忠誠心を欠いていたかどうか", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    loyalty_3 = models.IntegerField(
        label="人は、たとえ家族が悪いことをしたとしても家族に忠実であるべきだ",
        choices=agreement_likert(), widget=widgets.RadioSelect())
    morally_good_person = models.IntegerField(
        label="客観的に見て、より道徳的に優れた人物はどちらだと思いますか？",
        choices=[
            (1, "公平で正義を重んじ、偏見なく判断する人"),
            (0, "忠実で誠実、献身的で信頼できる人"),
        ], widget=widgets.RadioSelect())
    friend_choice = models.IntegerField(
        label="あなたはどちらのタイプの人と友達になりたいですか？",
        choices=[
            (1, "他者に対して公平で正義を重んじ、家族や友人への影響に関係なく偏見なく判断する人"),

            (0, "家族や友人に忠実で誠実、献身的で信頼でき、外部の人への影響に関係なく行動する人"),

        ], widget=widgets.RadioSelect())
    # ----- questionnaire 2 -----
    share_friend_stranger = models.IntegerField(
        label=f"あなたの{cu(1000)}のうち、友人にいくら渡しますか？残りはあなたの国の見知らぬ人に渡されます。",

        min=0,
        max=1000,
    )

    # ----- demographics -----
    age = models.IntegerField(
        label="あなたの年齢を教えてください。",
        choices=range(16, 121))
    gender = models.StringField(
        label="あなたの性別を教えてください。",
        choices=[
            ("F", "女性"),
            ("M", "男性"),
            ("NB", "ノンバイナリー"),
            ("NSP", "回答したくない"),
        ], widget=widgets.RadioSelect())
    highest_diploma = models.IntegerField(
        label="あなたが修了した最終学歴を教えてください。",
        choices=[
            (0, "学歴なし"),
            (1, "初等教育"),
            (2, "中等教育"),
            (3, "学士号"),
            (4, "修士号"),
            (5, "博士号以上"),
        ], widget=widgets.RadioSelect())


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):

    @staticmethod
    def js_vars(player: Player):
        return dict(fill_auto=player.session.config.get("fill_auto", False))


class Questionnaire1(MyPage):
    form_model = "player"
    form_fields = ["fairness_1", "fairness_2", "loyalty_1", "loyalty_2", "fairness_3", "loyalty_3",
                   "morally_good_person", "friend_choice"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            fields = [field for field in Questionnaire1.form_fields
                      if "fairness" in field or "loyalty" in field]
            for field in fields:
                setattr(player, field, random.randint(0, 5))
            player.morally_good_person = random.randint(0, 1)
            player.friend_choice = random.randint(0, 1)


class Questionnaire2(MyPage):
    form_model = "player"
    form_fields = ["share_friend_stranger"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.share_friend_stranger = random.randint(0, 1000)


class Demographics(MyPage):
    form_model = "player"
    form_fields = ["gender", "age", "highest_diploma"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.gender = random.choice(["M", "F", "NB", "NSP"])
            player.age = random.randint(16, 120)
            player.highest_diploma = random.randint(0, 5)


page_sequence = [Questionnaire1, Questionnaire2, Demographics]
