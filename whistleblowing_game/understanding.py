def get_understanding(parameters):
    understanding = [
        dict(
            question="赤プレイヤーがパッシブグループからECUを盗んだ場合、何が起こりますか？",
            propositions=[
                f"赤プレイヤーは{parameters['STEALING_AMOUNT']} ECUを得て、パッシブグループは"
                f"{parameters['STEALING_LOSS']} ECUを失います。",
                f"赤プレイヤーは{parameters['STEALING_LOSS']} ECUを得て、パッシブグループは"
                f"{parameters['STEALING_AMOUNT']} ECUを失います。",
                f"赤プレイヤーは{parameters['STEALING_PENALTY']} ECUを得て、パッシブグループは"
                f"{parameters['REPORTING_COST']} ECUを失います。",
            ],
            solution=0
        ),
        dict(
            question="赤プレイヤーがECUを盗み、選ばれた青プレイヤーが赤プレイヤーを報告した場合、何が起こりますか？",
            propositions=[
                f"赤プレイヤーが罰せられた場合、{parameters['STEALING_PENALTY']} ECUの罰金を支払います。"
                f"青プレイヤーは{parameters['REPORTING_COST']} ECUの報告コストを支払います。",
                f"赤プレイヤーが罰せられた場合、{parameters['STEALING_PENALTY']} ECUの罰金を支払います。"
                f"青プレイヤーは{parameters['REPORTING_COST']} ECUの報告コストを支払い、"
                f"{parameters['REPORTING_REWARD']} ECUの報酬を受け取ります。",
                "赤プレイヤーが罰せられなかった場合、青プレイヤーは報告コストを支払いません。",
            ],
            solution=1 if parameters['reward'] else 0,
        ),
        dict(
            question="一方の青プレイヤーが赤プレイヤーを報告し、もう一方が報告しなかった場合、何が起こりますか？",
            propositions=[
                "両方の決定が実行されます。",
                "赤プレイヤーは自動的に罰せられます。",
                "コンピュータがランダムに一方の青プレイヤーの決定を選んで実行します。",
            ],
            solution=2
        ),
    ]

    for i, q in enumerate(understanding, start=1):
        q["question_id"] = i
    return understanding
