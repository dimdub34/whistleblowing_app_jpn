import random
from collections import Counter
from pathlib import Path

from otree.api import *

from whistleblowing_commons.config import Config
from . import understanding

doc = """
Stealing / Taking game
"""

app_name = Path(__file__).parent.name


def get_appropriate():
    return [
        (0, "非常に不適切"),
        (1, "不適切"),
        (2, "やや不適切"),
        (3, "やや適切"),
        (4, "適切"),
        (5, "非常に適切"),
    ]


class C(BaseConstants):
    NAME_IN_URL = "whgame"
    PLAYERS_PER_GROUP = Config.PLAYERS_PER_GROUP
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    reward = models.BooleanField()
    num_of_takers = models.IntegerField()
    num_of_reporters = models.IntegerField()
    society_opinion_majority = models.IntegerField()

    def creating_session(self):
        self.reward = self.session.config.get("reward", False)

        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])

        inactive_group = random.choice(self.get_groups())
        for g in self.get_groups():
            g.active = g != inactive_group

        active_groups = [g for g in self.get_groups() if g.active]
        for g in active_groups:
            players = g.get_players()
            taker = random.choice(players)
            for p in players:
                p.taker = p == taker

    def compute_payoffs(self):
        active_groups = [g for g in self.get_groups() if g.active]
        for g in active_groups:
            players = g.get_players()
            reporters = [p for p in players if not p.taker]
            selected_reporter = random.choice(reporters)
            g.selected_reporter = selected_reporter.id_in_group
            g.reporter_has_reported = selected_reporter.reporting_decision

            if g.taker_has_taken and g.reporter_has_reported:
                g.audit_draw = random.uniform(0, 1)
                g.taker_audited = g.audit_draw < Config.AUDIT_PROBABILITY

        self.num_of_takers = sum([g.taker_has_taken for g in active_groups])
        self.num_of_reporters = sum(
            [p.reporting_decision for p in self.get_players() if p.group.active and not p.taker])

        soc_op_maj = [p.society_opinion for p in self.get_players()]
        soc_op_maj_count = Counter(soc_op_maj)
        self.society_opinion_majority = int(soc_op_maj_count.most_common(1)[0][0])

        for p in self.get_players():
            p.compute_payoffs()


def creating_session(subsession: Subsession):
    subsession.creating_session()


class Group(BaseGroup):
    active = models.BooleanField()
    taker_has_taken = models.BooleanField(initial=False)
    selected_reporter = models.IntegerField()
    reporter_has_reported = models.BooleanField(initial=False)
    audit_draw = models.FloatField()
    taker_audited = models.BooleanField(initial=False)


class Player(BasePlayer):
    # understanding questionnaire
    game_q1_faults = models.IntegerField()
    game_q2_faults = models.IntegerField()
    game_q3_faults = models.IntegerField()
    game_q4_faults = models.IntegerField()
    game_total_faults = models.IntegerField()

    taker = models.BooleanField()
    taking_decision = models.BooleanField(
        label="パッシブグループからECUを盗みますか？",
        widget=widgets.RadioSelectHorizontal,
        choices=[
        [True, "はい"],
        [False, "いいえ"],
    ],
    )
    estimation_reporting = models.IntegerField(
        label="青プレイヤーが赤プレイヤーを報告する可能性をどの程度だと思いますか：",
        min=0,
        max=100,
    )
    reporting_decision = models.BooleanField(
        label="赤プレイヤーを報告しますか？",
        widget=widgets.RadioSelectHorizontal,
        choices=[
        [True, "はい"],
        [False, "いいえ"],
        ],
    )
    audit_draw = models.FloatField()
    audit = models.BooleanField()
    payoff_ecu = models.FloatField()

    # Questions
    taker_motivation = models.LongStringField(
        label="（赤プレイヤーとして）あなたの決定の動機を教えてください："
    )
    reporter_motivation = models.LongStringField(
        label="（青プレイヤーとして）赤プレイヤーを報告する／しない決定の動機を教えてください："
    )
    personal_opinion = models.IntegerField(
        label="赤プレイヤーを報告することが適切かどうか、他者の意見とは独立に、あなた自身の意見で評価してください。"

              "「適切」とは、あなたが個人的に「正しい」「道徳的」と考える行動を意味します。"
              "基準は他者の意見ではなく、あなた自身の正直な意見です。"
              "正解・不正解はなく、この質問への回答による追加報酬もありません。",


        choices=get_appropriate(),
        widget=widgets.RadioSelect,
    )
    society_opinion = models.IntegerField(
        label = f"次に、社会全体の意見を評価し、ご自身の意見とは独立に、" 
              f"レッドプレイヤーを報告することが適切かどうかを判断してください。『適切』な行動とは、" 
              f"多くの人が『正しい』または『道徳的である』と認めるであろう行動を意味します。 " 
              f"したがって基準となるのはあなた個人の意見ではなく、社会の意見に対するあなたの評価です。 " 
              f"できるだけ正確にお答えください。この質問では、あなたの回答に応じて、" 
              f"実験の他の部分で得られる報酬に加えて {Config.SOCIETY_OPTION_PAYOFF} ECU を獲得できる可能性があります。 " 
              f"他の参加者の回答が、この質問に対するあなたの報酬に影響します。 " 
              f"最後に、この質問に対して最も多くの参加者が選んだ回答を決定します。 " 
              f"あなたがその多数回答と同じ回答をした場合、{Config.SOCIETY_OPTION_PAYOFF} ECU を獲得します。"
              f"例：あなたが「やや適切」と評価し、この部屋の多くの参加者も同じ評価をした場合、この質問で"

              f"{Config.SOCIETY_OPTION_PAYOFF} ECUを獲得します。"
              f"注：全参加者は同じ説明を受けています。",
        choices=get_appropriate(), widget=widgets.RadioSelect)

    def compute_payoffs(self):
        # --- Active group ---
        if self.group.active:
            txt_final = (
                f"あなたのグループはランダムにアクティブグループとして選ばれました。"
                f"あなたはグループ内で{'赤' if self.taker else '青'}プレイヤーでした。"
            )

            if self.taker:  # Red Player
                if self.taking_decision:  # Taker
                    txt_final += "あなたはパッシブグループからECUを盗むことを選びました。"

                    if self.group.reporter_has_reported:  # Reported
                        txt_final += "選ばれた青プレイヤーはあなたを報告しました。"

                        if self.group.taker_audited:  # Audited
                            txt_final += f"あなたは監査され、{Config.STEALING_PENALTY} ECUの罰金を科されました。"
                            self.payoff_ecu = Config.STEALING_AMOUNT - Config.STEALING_PENALTY

                        else:  # Not Audited
                            txt_final += "あなたは監査されませんでした。"
                            self.payoff_ecu = Config.STEALING_AMOUNT

                    else:  # Not Reported
                        txt_final += "あなたは報告されませんでした。"
                        self.payoff_ecu = Config.STEALING_AMOUNT

                else:  # Not Taker
                    txt_final += "あなたはパッシブグループからECUを盗まないことを選びました。"
                    self.payoff_ecu = 0

            else:  # Blue Player
                # Defensive initialization for all Blue Player branches.
                self.payoff_ecu = 0

                if self.reporting_decision:  # Reporter
                    txt_final += "あなたは赤プレイヤーを報告することを選びました。"

                    # Case 1: Blue Player is selected.
                    if self.group.selected_reporter == self.id_in_group:
                        txt_final += "あなたは報告者として選ばれました。"

                        if self.group.taker_has_taken:  # Taker stole
                            txt_final += "赤プレイヤーはパッシブグループからECUを盗みました。"
                            self.payoff_ecu = -Config.REPORTING_COST

                            if self.group.taker_audited:  # Audited
                                txt_final += "赤プレイヤーは監査され、罰金を科されました。"

                                if self.subsession.reward:  # With reward
                                    txt_final += f"あなたは{Config.REPORTING_REWARD} ECUの報酬を受け取りました。"
                                    self.payoff_ecu += Config.REPORTING_REWARD

                            else:  # Not audited
                                txt_final += "赤プレイヤーは監査されませんでした。"

                        else:  # Taker did not steal
                            txt_final += "赤プレイヤーはECUを盗みませんでした。"

                    # Case 2: Blue Player is not selected.
                    else:
                        txt_final += "あなたは報告者として選ばれませんでした。"

                        # Keep payoff at 0, but still inform the player about the Red decision.
                        if self.group.taker_has_taken:
                            txt_final += "赤プレイヤーはパッシブグループからECUを盗みました。"

                        else:
                            txt_final += "赤プレイヤーはECUを盗みませんでした。"

                else:  # Not Reporter
                    txt_final += "あなたは赤プレイヤーを報告しないことを選びました。"

        # --- Passive group ---
        else:
            txt_final = "あなたのグループはランダムにパッシブグループとして選ばれました。"

            if self.subsession.num_of_takers > 0:  # At least one taker
                if self.subsession.num_of_takers == 1:
                    txt_final += f"{self.subsession.num_of_takers}人の赤プレイヤーがあなたのグループからECUを盗みました。"
                else:
                    txt_final += f"{self.subsession.num_of_takers}人の赤プレイヤーがあなたのグループからECUを盗みました。"
            else:
                txt_final += "赤プレイヤーは誰もあなたのグループからECUを盗みませんでした。"
            self.payoff_ecu = -self.subsession.num_of_takers * Config.STEALING_LOSS_INDIV

        game_payoff = self.payoff_ecu

        # -- payoff for norm (question society_opinion) ---
        txt_final += (
            "<br>"
            f"社会の意見に関する質問で、あなたは<i>{get_appropriate()[self.society_opinion][1]}</i>と回答しました。"

            f"参加者の多数派は<i>{get_appropriate()[self.subsession.society_opinion_majority][1]}</i>と回答しました。"

        )

        norm_payoff = 0
        if self.society_opinion == self.subsession.society_opinion_majority:
            norm_payoff = Config.SOCIETY_OPTION_PAYOFF
            self.payoff_ecu += norm_payoff
            txt_final += f" あなたはこの質問で{Config.SOCIETY_OPTION_PAYOFF} ECUを獲得します。"

        txt_final += (
            "<br>"
            f"実験パート2でのあなたの報酬は {self.payoff_ecu} ECU です "
            f"(ゲーム: {game_payoff} ECU + 意見: {norm_payoff} ECU)。"
        )
        self.participant.vars[app_name] = dict(
            txt_final=txt_final,
            payoff_ecu=self.payoff_ecu,
            payoff=self.payoff_ecu * self.session.config["real_world_currency_per_point"])


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            instructions_template_path="whistleblowing_game/InstructionsTemplate.html",
            instructions_template_title="パート2 - 説明",
            en=True,
            fr=False,
            **Config.get_parameters()
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **Config.get_parameters(),
            en=True,
            fr=False,
        )


class Instructions(MyPage):
    template_name = "global/Instructions.html"


class InstructionsWaitMonitor(MyPage):
    template_name = "global/InstructionsWaitMonitor.html"

    @staticmethod
    def is_displayed(player):
        return Instructions.is_displayed(player)


class InstructionsWaitForAll(WaitPage):
    wait_for_all_groups = True
    template_name = "global/InstructionsWaitPage.html"

    @staticmethod
    def vars_for_template(player: Player):
        return MyPage.vars_for_template(player)


class Understanding(MyPage):
    template_name = "global/Understanding.html"
    form_model = "player"
    form_fields = [f"game_q{i}_faults" for i in range(1, 5)]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        parameters = Config.get_parameters()
        parameters.update(reward=player.subsession.reward)
        existing.update(understanding=understanding.get_understanding(parameters))
        return existing

    @staticmethod
    def js_vars(player: Player):
        existing = MyPage.js_vars(player)
        existing["understanding"] = Understanding.vars_for_template(player)["understanding"]
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            app_dict = player.participant.vars.setdefault(app_name, {})
            app_dict["is_bot"] = True
            for i in range(1, 5):
                setattr(player, f"game_q{i}_faults", random.randint(0, 2))
        player.game_total_faults = sum(
            getattr(player, f"game_q{i}_faults") for i in range(1, 5)
        )


class UnderstandingWaitForAll(WaitPage):
    wait_for_all_groups = True


class GroupRole(MyPage):
    pass


class DecisionTaking(MyPage):
    form_model = "player"
    form_fields = ["taking_decision"]

    @staticmethod
    def is_displayed(player):
        return player.group.active and player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            app_dict = player.participant.vars.setdefault(app_name, {})
            app_dict["is_bot"] = True
            player.taking_decision = random.choice([True, False])
        player.group.taker_has_taken = player.taking_decision


class EstimationReportingByTaker(MyPage):
    form_model = "player"
    form_fields = ["estimation_reporting"]

    @staticmethod
    def is_displayed(player: Player):
        return player.group.active and player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            app_dict = player.participant.vars.setdefault(app_name, {})
            app_dict["is_bot"] = True
            player.estimation_reporting = random.randint(0, 100)


class DecisionReporting(MyPage):
    form_model = "player"
    form_fields = ["reporting_decision"]

    @staticmethod
    def is_displayed(player):
        return player.group.active and not player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            app_dict = player.participant.vars.setdefault(app_name, {})
            app_dict["is_bot"] = True
            player.reporting_decision = random.choice([True, False])


class Questionnaire(MyPage):
    form_model = "player"

    @staticmethod
    def get_form_fields(player: Player):
        fields = []
        if player.group.active:
            if player.taker:
                fields.append("taker_motivation")
            else:
                fields.append("reporter_motivation")
        fields.extend(["personal_opinion", "society_opinion"])
        return fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            app_dict = player.participant.vars.setdefault(app_name, {})
            app_dict["is_bot"] = True
            fields = Questionnaire.get_form_fields(player)
            if "taker_motivation" in fields:
                player.taker_motivation = "盗む決定についての説明"
            if "reporter_motivation" in fields:
                player.reporter_motivation = "報告する決定についての説明"
            player.personal_opinion = random.randint(0, 5)
            player.society_opinion = random.randint(0, 5)


class BeforeFinalWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.compute_payoffs()


class Final(MyPage):
    pass


page_sequence = [
    Instructions, InstructionsWaitForAll,
    # InstructionsWaitMonitor,
    Understanding, UnderstandingWaitForAll,
    GroupRole,
    DecisionTaking, EstimationReportingByTaker,
    DecisionReporting,
    Questionnaire,
    BeforeFinalWaitForAll, Final,
]
