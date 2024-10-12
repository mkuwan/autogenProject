import autogen
from autogen import AssistantAgent, UserProxyAgent
import streamlit as st
import asyncio

class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        # with st.chat_message(sender.name):
        #     st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)

config_list = autogen.config_list_from_json(
    env_or_file="pages/LLM_CONFIG_LIST.json",
)

filter_codellama = {"model": ["codellama"]}
filter_codegemma = {"model": ["codegemma"]}
filter_llama31 = {"model": ["llama3.1"]}
filter_mistral = {"model": ["mistral-nemo-instruct-2407"]}
filter_rakuten = {"model": ["rakutenai-7b-chat"]}

writer_task1 ="""
ある書店チェーンのシステム開発を考えています。
売上、受発注、棚卸、入金に関するシステムを実装したいです。
そのための要件定義を提案してください。
"""

reviewer_task1 = """
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
必ず日本語で会話は行ってください
"""

writer_task2 = """
Reviewerからのフィードバックを受けて、要件定義書を再作成してください。
要件定義書は日本語で記述し、Markdown形式で提出してください。
フロー図や図式に関しては必ずMermaid形式で記述し、他のWebサイト等やリンクを利用しないでください。
"""

writer_task_last = """
Reviewerからのフィードバックを受けて、要件定義書を再作成して[最終案]という文言を付与して提出してください。
要件定義書は日本語で記述し、Markdown形式で提出してください。
フロー図や図式に関しては必ずMermaid形式で記述し、他のWebサイト等やリンクを利用しないでください。
"""

reviewer_task2 = """
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
必ず日本語で会話は行ってください
"""

with st.container():
    # for message in st.session_state["messages"]:
    #    st.markdown(message)

    user_input = st.chat_input("Give some goal for the agent ...")
    if user_input:
        with st.chat_message("User"):
            st.markdown(user_input)

        llm_config = {
            "timeout": 600,
            "config_list": autogen.filter_config(config_list, filter_mistral),
            "cache_seed": None,
            "temperature": 0,
            "price": [0, 0],
        }

        writer = TrackableAssistantAgent(
            name="Writer",
            llm_config=llm_config,
            max_consecutive_auto_reply=2,
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
            - データモデル(テーブル形式で記述してください)
            - ユーザーインターフェース
            - エラー処理
            - バックアップ
            - セキュリティ
            - パフォーマンス
            - ログ管理
            - 非機能要件
            ドキュメントはMarkdown形式で記述してください。
            フロー図やクラス図、モデル、その他の図に関しては必ずMarkdownもしくはMermaid形式で記述し、他のWebサイト等やリンクを利用しないでください。
            テーブル形式のものはMarkdownのテーブル形式で記述してください。
            画像生成は行わないでください。
            修正や指摘が与えられた場合は全文を修正して再提出してください。
            """,
        )

        Reviewer = TrackableAssistantAgent(
            name="Reviewer",
            llm_config=llm_config,
            max_consecutive_auto_reply=2,
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

        user_proxy = TrackableUserProxyAgent(
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

        user_proxy.initiate_chats(
            [
                {
                    "chat_id": 0,
                    "recipient": writer,
                    "message": user_input,
                    "clear_history": True,
                    "silent": False,
                    "max_turns": 1,
                    "summary_method": "last_msg"
                },
                {
                    "chat_id": 1,
                    "recipient": Reviewer,
                    "message": reviewer_task1,
                    "clear_history": False,
                    "silent": False,
                    "max_turns": 1,
                    "summary_method": "last_msg"
                },
                {
                    "chat_id": 2,
                    "recipient": writer,
                    "message": writer_task2,
                    "clear_history": False,
                    "silent": False,
                    "max_turns": 1,
                    "summary_method": "last_msg"
                },
                {
                    "chat_id": 3,
                    "recipient": Reviewer,
                    "message": reviewer_task2,
                    "clear_history": False,
                    "silent": False,
                    "max_turns": 1,
                    "summary_method": "last_msg"
                },
                {
                    "chat_id": 4,
                    "recipient": writer,
                    "message": writer_task_last,
                    "clear_history": False,
                    "silent": False,
                    "max_turns": 1,
                    "summary_method": "last_msg"
                }
            ],
        )
        # # Create an event loop
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        #
        # # Define an asynchronous function
        # async def initiate_chat():
        #     await user_proxy.a_initiate_chats(
        #         [
        #             {
        #                 "chat_id": 0,
        #                 "recipient": writer,
        #                 "message": user_input,
        #                 "clear_history": True,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 1,
        #                 "recipient": Reviewer,
        #                 "message": reviewer_task1,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 2,
        #                 "recipient": writer,
        #                 "message": writer_task2,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 3,
        #                 "recipient": Reviewer,
        #                 "message": reviewer_task2,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 4,
        #                 "recipient": writer,
        #                 "message": writer_task2,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 5,
        #                 "recipient": Reviewer,
        #                 "message": reviewer_task2,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             },
        #             {
        #                 "chat_id": 6,
        #                 "recipient": writer,
        #                 "message": writer_task2,
        #                 "clear_history": False,
        #                 "silent": False,
        #                 "max_turns": 1,
        #                 "summary_method": "last_msg"
        #             }
        #         ],
        #     )
        #
        # # Run the asynchronous function within the event loop
        # loop.run_until_complete(initiate_chat())
