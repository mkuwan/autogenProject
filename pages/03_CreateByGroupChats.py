import autogen

config_list = autogen.config_list_from_json(
    env_or_file="./LLM_CONFIG_LIST.json",
)

filter_codellama = {"model": ["codellama"]}
filter_codegemma = {"model": ["codegemma"]}
filter_llama31 = {"model": ["llama3.1"]}
filter_mistral = {"model": ["mistral-nemo-instruct-2407"]}
filter_rakuten = {"model": ["rakutenai-7b-chat"]}

llm_config = {
    "cache_seed": 41,  # change the cache_seed for different trials. if set None, it will be random?
    "temperature": 0,
    "config_list": autogen.filter_config(config_list, filter_mistral),
    "timeout": 600,  # in seconds
    "price": [0, 0],
}




writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    # max_consecutive_auto_reply=2,
    system_message="""
    あなたは、アプリケーション開発における設計の専門家です。
    クライアントからの要望や要求定義から、要件定義書を作成してください。
    作成する成果物としては基本的な要件定義の項目の他に以下のものを考慮して必要に応じて追加してください。
    ただしユーザーから指定があった場合はそれに合わせてください。
    - 機能用件
    - ユースケース図
    - 業務フロー図
    - システム設計書
    - アーキテクチャ図
    - 非機能要件
    ドキュメントはMarkdown形式で記述してください。
    フロー図が含む場合はMermaid形式で記述してください。
    """,
)


Reviewer = autogen.AssistantAgent(
    name="Reviewer",
    llm_config=llm_config,
    # max_consecutive_auto_reply=1,
    system_message="""
    あなたは、設計の品質を向上させるためのフィードバックを提供するレビュアーです。
    設計者(Writer)が提出した内容が要件に適合しているか、品質が高いかを確認することが求められます。
    ユーザーやクライアントから提出された内容に要件が適合しているか、品質が高いかを確認し、設計者(Writer)にフィードバックを提供してください。
    また文章の体裁、誤字脱字、表現の統一にも注意してフィードバックを提供してください。
    特に、以下の点についてレビューを行ってください。
    - 内容の明確性, 説明の適切さ
    - 要件の過不足の確認, 不足している場合は追加要件の提案
    - ドキュメントの体裁, 誤字脱字の確認
    - フロー図の正確性, 説明の明確さ
    - ドキュメントの一貫性, 表現の統一
    - その他の改善点
    """,
)


user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config=False,
    # code_execution_config={
    #     "last_n_messages": 1,
    #     "work_dir": "my_code",
    #     "use_docker": False,
    # }
)


plan ="""
ある書店チェーンのシステム開発を考えています。
売上、受発注、棚卸、入金に関するシステムを実装したいです。
そのための要件定義を提案してください。
"""


group_chat = autogen.GroupChat(
    agents=[user_proxy, writer, Reviewer],
    messages=[],
    max_round=3
)

manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

chat_result = user_proxy.initiate_chat(
    manager,
    message=plan,
    summary_method="reflection_with_llm",
    max_turns=4
)
