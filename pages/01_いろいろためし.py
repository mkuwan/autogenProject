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
売上、受発注、入金に関するシステムを実装したいです。
そのための要件定義を提案してください。
"""

reviewer_task1 = """
設計者(Writer)が提出した内容が要件に適合しているか、品質が高いかを確認することが求められます。
必ず日本語で会話は行ってください
ユーザーやクライアントから提出された内容に要件が適合しているか、品質が高いかを確認し、設計者(Writer)にフィードバックを提供してください。
また文章の体裁、誤字脱字、表現の統一にも注意してフィードバックを提供してください。
特に、以下の点についてレビューを行ってください。
- 内容の明確性, 説明の適切さ
- 要件の過不足の確認, 不足している場合は追加要件の提案
- ドキュメントの体裁, 誤字脱字の確認
- フロー図の正確性, 説明の明確さ
- ドキュメントの一貫性, 表現の統一
- その他の改善点
"""

writer_task2 = """
Reviewerからのフィードバックを受けて、要件定義書を再作成してください。
要件定義書は日本語で記述し、Markdown形式で提出してください。
フロー図や図式に関しては必ずMermaid形式で記述し、画像や他のWebサイト等やリンクを利用しないでください。
"""

writer_task_last = """
Reviewerからのフィードバックを受けて、要件定義書を再作成して[最終案]という文言を付与して提出してください。
要件定義書は日本語で記述し、Markdown形式で提出してください。
フロー図や図式に関しては必ずMermaid形式で記述し、画像や他のWebサイト等やリンクを利用しないでください。
"""

reviewer_task2 = """
設計者(Writer)が提出した内容が要件に適合しているか、品質が高いかを確認することが求められます。
必ず日本語で会話は行ってください
ユーザーやクライアントから提出された内容に要件が適合しているか、品質が高いかを確認し、設計者(Writer)にフィードバックを提供してください。
また文章の体裁、誤字脱字、表現の統一にも注意してフィードバックを提供してください。
特に、以下の点についてレビューを行ってください。
- 内容の明確性, 説明の適切さ
- 要件の過不足の確認, 不足している場合は追加要件の提案
- ドキュメントの体裁, 誤字脱字の確認
- フロー図の正確性, 説明の明確さ
- ドキュメントの一貫性, 表現の統一
- その他の改善点
"""

writer_Basic_Design_Document_task1 = """
要件定義書に基づき、基本設計書を作成してください。
基本設計書は日本語で記述し、Markdown形式で提出してください。
フロー図や図式に関しては必ずMermaid形式で記述し、画像や他のWebサイト等やリンクを利用しないでください。
"""

reviewer_Basic_Design_Document_task = """
設計者(Writer)が提出した基本設計書が要件に適合しているか、品質が高いかを確認することが求められます。
必ず日本語で会話は行ってください
この基本設計書のレビューを通じて、設計の妥当性、完全性、および潜在的な問題点を特定し、改善提案を行ってください。
ユーザーやクライアントから提出された内容に要件が適合しているか、品質が高いかを確認し、設計者(Writer)にフィードバックを提供してください。
"""

writer_Flow_task = """
基本設計書に記されている内容を元に、業務フロー図およびシステムフロー図を作成してください。
ドキュメントはMarkdown形式とし、フロー図はMermaid形式で記述してください。
抜け漏れが無いように、業務全体やシステム全体を詳細まで網羅するようにしてください。
"""

user_input = st.chat_input("Give some goal for the agent ...")
if user_input:
    with st.chat_message("User"):
        st.markdown(user_input)

    llm_config = {
        "timeout": 1800,
        "config_list": autogen.filter_config(config_list, filter_mistral),
        "cache_seed": None,
        "temperature": 0,
        "price": [0, 0],
        # "max_tokens": 40000,
        # "top_p": 0.95,
        # "frequency_penalty": 0.0,
    }

    # 要件定義書作成者
    writer = TrackableAssistantAgent(
        name="Writer",
        llm_config=llm_config,
        max_consecutive_auto_reply=2,
        system_message="""
        あなたは、アプリケーション開発における設計の専門家です。
        クライアントからの要望や要求定義から、要件定義書を作成してください。
        作成する成果物としては最大で5000文字までとし、基本的な要件定義の項目の他に以下のものを考慮して必要に応じて追加してください。
        ただしユーザーから指定があった場合はそれに合わせてください。
        - 機能用件
        - ユースケース図
        - 業務フロー図
        - システム設計書
        - アーキテクチャ図
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
        画像生成や画像リンクは行わないでください。
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

    # 基本設計書作成者
    writer_Basic_Design_Document = TrackableAssistantAgent(
        name="Basic_Design_Writer",
        llm_config=llm_config,
        max_consecutive_auto_reply=2,
        system_message="""
            あなたは、アプリケーション開発における設計の専門家です。
            要件定義書に基づいて基本設計書を作成してください。
            基本設計書は最大で16000文字までとし、日本語で記述し、Markdown形式で提出してください。
            作成する成果物としては以下のものを考慮しつつ他の項目も必要に応じて追加してください。
            ただしユーザーから指定があった場合はそれに合わせてください。
            - プロジェクト概要
               - プロジェクト名
               - プロジェクトの目的
               - 背景と経緯
            - システムの目的
            - 機能一覧
            - 機能要件
            - システム開発方針
            - メイン機能
            - システム設計書
               - システムアーキテクチャ図
               - ハードウェア構成
               - ソフトウェア構成
            - データベース設計
               - データベーススキーマ
               - テーブル定義
               - インデックス設計
            - インターフェース設計
               - ユーザーインターフェース（UI）設計
               - API設計
               - 外部システムとの連携
            - セキュリティ設計
               - 認証と認可
               - データ暗号化
               - セキュリティポリシー
            - 運用設計
               - バックアップとリカバリ
               - モニタリングとアラート
               - メンテナンス計画
            - テスト計画
               - テスト戦略
               - テストケース
               - テスト環境
            - スケジュール
               - プロジェクトマイルストーン
               - タイムライン
            - リスク管理
                - リスクの識別
                - リスクの評価と対策
            ドキュメントはMarkdown形式で記述してください。
            フロー図やクラス図、モデル、その他の図に関しては必ずMarkdownもしくはMermaid形式で記述し、他のWebサイト等やリンクを利用しないでください。
            テーブル形式のものはMarkdownのテーブル形式で記述してください。
            画像生成や画像リンクは行わないでください
            修正や指摘が与えられた場合は全文を修正して再提出してください。
            """,
    )

    Reviewer_Basic_Design_Document = TrackableAssistantAgent(
        name="Basic_Design_Reviewer",
        llm_config=llm_config,
        max_consecutive_auto_reply=2,
        system_message="""
        あなたは、設計の品質を向上させるためのフィードバックを提供するレビュアーです。
        設計者(Writer)が提出した基本設計書が要件に適合しているか、品質が高いかを確認することが求められます。
        この基本設計書のレビューを通じて、設計の妥当性、完全性、および潜在的な問題点を特定し、改善提案を行ってください。
        ユーザーやクライアントから提出された内容に要件が適合しているか、品質が高いかを確認し、設計者(Writer)にフィードバックを提供してください。
        内容は日本語で記述してください。
        レビューの観点:
        - 要件定義の妥当性
        - 機能要件と非機能要件が明確に定義されているか
        - 要件が一貫しており、矛盾がないか
        - システム構成の適切性
        - システムアーキテクチャが明確で理解しやすいか
        - ハードウェアおよびソフトウェア構成が適切か
        - データベース設計の完全性
        - データベーススキーマが正確か
        - テーブル定義とインデックス設計が適切か
        - インターフェース設計の明確性
        - ユーザーインターフェース設計がユーザーフレンドリーか
        - API設計が明確で、外部システムとの連携が適切か
        - セキュリティ設計の堅牢性
        - 認証と認可のメカニズムが適切か
        - データ暗号化とセキュリティポリシーが十分か
        - 運用設計の実現可能性
        - バックアップとリカバリ計画が現実的か
        - モニタリングとアラートシステムが効果的か
        - テスト計画の詳細性
        - テスト戦略が明確か
        - テストケースが包括的か
        - スケジュールの現実性
        - プロジェクトマイルストーンとタイムラインが現実的か
        - リスク管理の徹底
        - リスクの識別と評価が適切か
        - リスク対策が具体的か
        期待する出力:
        - 各セクションに対する具体的なフィードバック
        - 潜在的な問題点の指摘とその理由
        - 改善提案
        その他の指示:
        - フィードバックは箇条書きで記載してください。
        - 可能であれば、具体例を挙げて説明してください。
        """,
    )

    # フロー図作成者
    writer_Flow = TrackableAssistantAgent(
        name="Flow_Writer",
        llm_config=llm_config,
        max_consecutive_auto_reply=2,
        system_message="""
        あなたは、アプリケーション開発における設計の専門家です。
        特にフロー図を作成に長けており、業務全体やシステム全体を網羅したフロー図を作成することができます。
        画像生成や画像リンクは行わないでください
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
            # {
            #     "chat_id": 3,
            #     "recipient": Reviewer,
            #     "message": reviewer_task2,
            #     "clear_history": False,
            #     "silent": False,
            #     "max_turns": 1,
            #     "summary_method": "last_msg"
            # },
            # {
            #     "chat_id": 4,
            #     "recipient": writer,
            #     "message": writer_task_last,
            #     "clear_history": False,
            #     "silent": False,
            #     "max_turns": 1,
            #     "summary_method": "last_msg"
            # },

            # 以下からは基本設計書の作成
            {
                "chat_id": 5,
                "recipient": writer_Basic_Design_Document,
                "message": writer_Basic_Design_Document_task1,
                "clear_history": False,
                "silent": False,
                "max_turns": 1,
                "summary_method": "last_msg"
            },
            {
                "chat_id": 6,
                "recipient": Reviewer_Basic_Design_Document,
                "message": reviewer_Basic_Design_Document_task,
                "clear_history": False,
                "silent": False,
                "max_turns": 1,
                "summary_method": "last_msg"
            },
            {
                "chat_id": 7,
                "recipient": writer_Basic_Design_Document,
                "message": writer_Basic_Design_Document_task1,
                "clear_history": False,
                "silent": False,
                "max_turns": 1,
                "summary_method": "last_msg"
            },
            # {
            #     "chat_id": 8,
            #     "recipient": Reviewer_Basic_Design_Document,
            #     "message": reviewer_Basic_Design_Document_task,
            #     "clear_history": False,
            #     "silent": False,
            #     "max_turns": 1,
            #     "summary_method": "last_msg"
            # },
            # {
            #     "chat_id": 9,
            #     "recipient": writer_Basic_Design_Document,
            #     "message": writer_Basic_Design_Document_task1 + " [最終案]という文言を付与して提出してください。",
            #     "clear_history": False,
            #     "silent": False,
            #     "max_turns": 1,
            #     "summary_method": "last_msg"
            # },

            # 以下からはフロー図の作成
            {
                "chat_id": 10,
                "recipient": writer_Flow,
                "message": writer_Flow_task,
                "clear_history": False,
                "silent": False,
                "max_turns": 1,
                "summary_method": "last_msg"
            },
        ],
    )



