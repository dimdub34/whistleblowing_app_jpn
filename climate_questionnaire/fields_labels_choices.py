# ======================================================================================================================
#
# Scale Choices
#
# ======================================================================================================================
def get_scale_action():
    return [
        [-2, "まったくそう思わない"],
        [-1, "-1"],
        [0, "どちらともいえない"],
        [1, "1"],
        [2, "とてもそう思う"]
        ]


def get_scale_policy():
    return [
        [-2, "強く反対する"],
        [-1, "やや反対する"],
        [0, "賛成でも反対でもない"],
        [1, "やや賛成する"],
        [2, "強く賛成する"]
    ]


def get_scale_certainty():
    return [
        [-2, "非常に確信がない"],
        [-1, "確信がない"],
        [1, "確信がある"],
        [2, "非常に確信がある"],
    ]


def get_scale_frequency_info():
    return [
        [5, "毎日"],
        [4, "週に2回"],
        [3, "週に1回"],
        [2, "月に2回"],
        [1, "月に1回"],
        [0, "まったくない"]
    ]


def get_scale_expectations():
    return [
        [-2, "非常に起こりそうにない"],
        [-1, "あまり起こりそうにない"],
        [1, "やや起こりそう"],
        [2, "非常に起こりそう"]
    ]


def get_scale_agreement():
    return [
        [-2, "強く不同意"],
        [-1, "やや不同意"],
        [0, "どちらともいえない"],
        [1, "やや同意"],
        [2, "強く同意"]
    ]


def get_scale_income():
    return [
        [0, "0〜1250ドル"],
        [1, "1250〜2000ドル"],
        [2, "2000〜4000ドル"],
        [3, "4000〜6000ドル"],
        [4, "6000〜8000ドル"],
        [5, "8000〜12,500ドル"],
        [6, "12,500ドル以上"],
        [999, "回答したくない"]
    ]


def get_scale_education():
    return [
        [0, "初等教育または前期中等教育"],
        [1, "後期中等教育"],
        [2, "大学以外の高等教育"],
        [3, "学士課程"],
        [4, "大学院課程（修士・博士）"],
        [999, "回答したくない"]
    ]


def get_options_bdm():
    return [
        ['A', '選択肢A'],
        ['B', '選択肢B']
    ]


# ======================================================================================================================
#
# DYNAMIC CHOICES METHODS
#
# ======================================================================================================================
def climate_exists_choices(player):
    return [
        [True, "はい"],
        [False, "いいえ"]
    ]


def policy_fight_choices(player):
    return [
        [1, "はい"],
        [0, "いいえ"],
        [-1, "わからない／回答したくない"]
    ]


def expectations_policy_household_choices(player):
    return [
        [-2, "大きく損をする"],
        [-1, "損をする"],
        [0, "どちらでもない"],
        [1, "得をする"],
        [2, "大きく得をする"],
    ]


def agreement_policy_choices(player):
    return get_scale_policy()


def climate_knowledge_choices(player):
    return [
        [0, "まったくない"],
        [1, "少しある"],
        [2, "ある程度ある"],
        [3, "かなりある"],
        [4, "非常にある"]
    ]


def info_freq_choices(player):
    return get_scale_frequency_info()


def climate_info_freq_choices(player):
    return get_scale_frequency_info()


def climate_threat_choices(player):
    return [
        [3, "非常に深刻な脅威である"],
        [2, "やや深刻な脅威である"],
        [1, "まったく脅威ではない"],
        [0, "わからない"]
    ]


def limit_flying_choices(player): return get_scale_action()


def limit_driving_choices(player): return get_scale_action()


def electric_vehicle_choices(player): return get_scale_action()


def limit_beef_choices(player): return get_scale_action()


def limit_heating_choices(player): return get_scale_action()


def tax_flying_choices(player): return get_scale_policy()


def tax_fossil_choices(player): return get_scale_policy()


def ban_polluting_choices(player): return get_scale_policy()


def subsidy_lowcarbon_choices(player): return get_scale_policy()


def climate_fund_choices(player): return get_scale_policy()


def expectations_droughts_choices(player): return get_scale_expectations()


def expectations_eruptions_choices(player): return get_scale_expectations()


def expectations_sea_choices(player): return get_scale_expectations()


def expectations_agriculture_choices(player): return get_scale_expectations()


def expectations_living_choices(player): return get_scale_expectations()


def expectations_migration_choices(player): return get_scale_expectations()


def expectations_conflicts_choices(player): return get_scale_expectations()


def expectations_extinction_choices(player): return get_scale_expectations()


def expectations_policy_economy_choices(player): return get_scale_agreement()


def expectations_policy_cc_choices(player): return get_scale_agreement()


def income_choices(player): return get_scale_income()


def education_choices(player): return get_scale_education()


def choice_1_choices(player): return get_options_bdm()


def choice_2_choices(player): return get_options_bdm()


def choice_3_choices(player): return get_options_bdm()


def choice_4_choices(player): return get_options_bdm()


def choice_5_choices(player): return get_options_bdm()


def choice_6_choices(player): return get_options_bdm()


def choice_7_choices(player): return get_options_bdm()


# ======================================================================================================================
#
# FIELDS LABELS
#
# ======================================================================================================================
class Lexicon:
    climate_exists_label = "気候変動は実在する現象だと思いますか？"
    narrative_elicitation_label = (
        "あなたの意見では、先ほどの文章で説明された事実（世界の平均気温の上昇や極端気象の増加など）は何によって説明されると思いますか？ <br><br>"
        "気候変動に起因するとされるこれらの事実の<b>原因</b>を述べ、それらの原因がどのようにこれらの事実に影響し、互いにどのようにつながっている可能性があるのかを<b>説明</b>してください。<br><br>"
        "文章で、あなたの考えを完全な文で説明してください。正しい答え・間違った答えはありません。あなたの率直で個人的な意見をお書きください。<br>"
        "[160文字以上]"
    )


    narrative_confidence_label = (
        "0（まったく自信がない）から100（非常に自信がある）の尺度で、前の質問で述べた説明についてどの程度自信がありますか？"
    )
    confidence_policy_label = (
        "0（まったく自信がない）から100（非常に自信がある）の尺度で、前の質問で述べた「政府が取るべき対策・解決策」に関する回答についてどの程度自信がありますか？"
)

    policy_fight_label = "あなたの意見では、あなたの国は気候変動に取り組むべきだと思いますか？"
    policy_narrative_label = "その理由を説明してください。"
    expectations_policy_economy_label = "私が述べた解決策は、国の経済や雇用に良い影響を与えると思う。"
    expectations_policy_cc_label = "私が述べた解決策は、気候変動の影響を抑制または軽減するのに役立つと思う。"
    expectations_policy_household_label = "私が述べた解決策によって、私の世帯は経済的に得をするか損をするか。"
    agreement_policy_label = "あなたが述べた解決策に賛成しますか、それとも反対しますか？"
    climate_knowledge_label = "気候変動について、あなたはどの程度知識があると思いますか？"
    rank_coal_label = "石炭火力発電所の順位"
    rank_gas_label = "ガス火力発電所の順位"
    rank_nuclear_label = "原子力発電所の順位"
    info_freq_label = (
        "過去3か月間に、どの程度の頻度で情報やニュースを得ましたか？<br>"
        "ここでいう情報・ニュースとは、国内・国際・地域のニュースやその他のニュース事実を指します。")
    use_tv_label = "テレビ（例：全国ニュース、ケーブルニュース）"
    use_newspapers_label = "新聞（紙媒体）"
    use_radio_label = "ラジオまたはポッドキャスト"
    use_social_label = "ソーシャルメディア"
    use_online_label = "ニュースサイトまたはニュースアプリ"
    use_newsletters_label = "ニュースレターまたはメール購読"
    climate_info_freq_label = (
        "過去3か月間に、<b>気候変動</b>に関する情報やニュースをどの程度の頻度で得ましたか？<br>"
        "ここでいう情報・ニュースとは、国内・国際・地域のニュースやその他のニュース事実を指します。")
    use_tv_climate_label = "テレビ（例：全国ニュース、ケーブルニュース）"
    use_newspapers_climate_label = "新聞（紙媒体）"
    use_radio_climate_label = "ラジオまたはポッドキャスト"
    use_social_climate_label = "ソーシャルメディア"
    use_online_climate_label = "ニュースサイトまたはニュースアプリ"
    use_newsletters_climate_label = "ニュースレターまたはメール購読"
    climate_threat_label = "今後20年間で、気候変動はあなたの国の人々にとって脅威になると思いますか？"
    expectations_droughts_label = "深刻な干ばつや熱波"
    expectations_eruptions_label = "火山噴火の増加"
    expectations_sea_label = "海面上昇"
    expectations_agriculture_label = "農業生産の低下"
    expectations_living_label = "生活水準の低下"
    expectations_migration_label = "移住の増加"
    expectations_conflicts_label = "武力紛争の増加"
    expectations_extinction_label = "人類の絶滅"
    limit_flying_label = "飛行機の利用を減らす"
    limit_driving_label = "自動車の利用を減らす"
    electric_vehicle_label = "電気自動車を利用する"
    limit_beef_label = "牛肉の消費を減らす"
    limit_heating_label = "暖房・冷房の使用を減らす"
    income_label = (
        "あなたの世帯について、平均的な月間の手取り収入（税金・控除後）はどの程度だと思いますか？<br>"
        "給与、年金、家族手当、失業給付、その他の定期的な収入を含めてお答えください。"
    )
education_label = "あなたが達成した最終学歴はどれですか？"

    @staticmethod
    def _get_field_label(field_name):
        content = getattr(Lexicon, f"{field_name}_label", None)
        if content:
            return content
        return f"Label for '{field_name}' not found"

    @staticmethod
    def get_fields_labels(field_names: list):
        fields_labels = dict()
        for field in field_names:
            fields_labels[field] = Lexicon._get_field_label(field)
        return fields_labels
