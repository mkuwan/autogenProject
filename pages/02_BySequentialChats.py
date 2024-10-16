import autogen
from autogen import AssistantAgent, UserProxyAgent
import streamlit as st
import asyncio

config_list = autogen.config_list_from_json(
    env_or_file="pages/LLM_CONFIG_LIST.json",
)

filter_codellama = {"model": ["codellama"]}
filter_codegemma = {"model": ["codegemma"]}
filter_llama31 = {"model": ["llama3.1"]}
filter_mistral = {"model": ["mistral-nemo-instruct-2407"]}
filter_rakuten = {"model": ["rakutenai-7b-chat"]}

llm_config = {
    "cache_seed": None,  # change the cache_seed for different trials. if set None, it will be random?
    "temperature": 0,
    "config_list": autogen.filter_config(config_list, filter_mistral),
    "timeout": 600,  # in seconds
    "price": [0, 0],
    "stream": True,
}

if "messages" not in st.session_state:
    print('initialize st.session_state.messages')
    st.session_state["messages"] = []



# 目次
# プロジェクト概要: プロジェクトの目的、背景、範囲、スコープ、成果物、リスク、課題、システム構成図、用語集、
# 機能要件: システム機能の一覧、ユースケース、画面・ユーザーインターフェース、帳票、情報・データ、外部インターフェース、制約事項、
# データ要件: データベース要件一覧、データモデル、データフロー、データの保存、データの保護、データの品質、データセキュリティ、
# 非機能要件: 性能、信頼性、セキュリティ、保守性、運用性、拡張性、移行性、可用性、システムの冗長性・耐障害性、
# 制約条件: 予算、スケジュール、リソース、技術、法規制
# リスク管理: リスク一覧、リスクの定義、リスクの評価、リスクの対応、リスクの監視、リスクの報告、
# テスト計画: テストの範囲、テストの種類、テストの項目、テストの方法、テストのスケジュール、テストの報告、
# 承認と変更管理: 承認プロセス、変更管理プロセス、変更履歴、
# プロジェクト計画: WBS、
# 運用と保守: 運用計画、保守計画、サポート体制、
# トレーニング: トレーニング計画、トレーニング内容、トレーニング方法、
# ドキュメント: ドキュメント一覧、ドキュメントの作成、ドキュメントの管理、
# 移行計画: 移行計画、移行手順、移行リスク、移行スケジュール、
# 引継ぎ計画: 引継ぎ計画、引継ぎ手順、引継ぎリスク、引継ぎスケジュール、

check_titles = {
    'check01': 'プロジェクト概要',
    'check02': '機能要件',
    'check03': 'データ要件',
    'check04': '非機能要件',
    'check05': '制約条件',
    'check06': 'リスク管理',
    'check07': 'テスト計画',
    'check08': '承認と変更管理',
    'check09': 'プロジェクト計画',
    'check10': '運用と保守',
    'check11': 'トレーニング',
    'check12': 'ドキュメント',
    'check13': '移行計画',
    'check14': '引継ぎ計画',
}

check_items = {
    'check0101': '目的',
    'check0102': '背景',
    'check0103': '範囲',
    'check0104': 'スコープ',
    'check0105': '成果物',
    'check0106': 'リスク',
    'check0107': '課題',
    'check0108': 'システム構成図',
    'check0109': '用語集',
    'check0201': 'システム機能の一覧',
    'check0202': 'ユースケース',
    'check0203': '画面・ユーザーインターフェース',
    'check0204': '帳票',
    'check0205': '情報・データ',
    'check0206': '外部インターフェース',
    'check0207': '制約事項',
    'check0301': 'データベース要件一覧',
    'check0302': 'データモデル',
    'check0303': 'データフロー',
    'check0304': 'データの保存',
    'check0305': 'データの保護',
    'check0306': 'データの品質',
    'check0307': 'データセキュリティ',
    'check0401': '性能',
    'check0402': '信頼性',
    'check0403': 'セキュリティ',
    'check0404': '保守性',
    'check0405': '運用性',
    'check0406': '拡張性',
    'check0407': '移行性',
    'check0408': '可用性',
    'check0409': 'システムの冗長性・耐障害性',
    'check0501': '予算',
    'check0502': 'スケジュール',
    'check0503': 'リソース',
    'check0504': '技術',
    'check0505': '法規制',
    'check0601': 'リスク一覧',
    'check0602': 'リスクの定義',
    'check0603': 'リスクの評価',
    'check0604': 'リスクの対応',
    'check0605': 'リスクの監視',
    'check0606': 'リスクの報告',
    'check0701': 'テストの範囲',
    'check0702': 'テストの種類',
    'check0703': 'テストの項目',
    'check0704': 'テストの方法',
    'check0705': 'テストのスケジュール',
    'check0706': 'テストの報告',
    'check0801': '承認プロセス',
    'check0802': '変更管理プロセス',
    'check0803': '変更履歴',
    'check0901': 'WBS',
    'check1001': '運用計画',
    'check1002': '保守計画',
    'check1003': 'サポート体制',
    'check1101': 'トレーニング計画',
    'check1102': 'トレーニング内容',
    'check1103': 'トレーニング方法',
    'check1201': 'ドキュメント一覧',
    'check1202': 'ドキュメントの作成',
    'check1203': 'ドキュメントの管理',
    'check1301': '移行計画',
    'check1302': '移行手順',
    'check1303': '移行リスク',
    'check1304': '移行スケジュール',
    'check1401': '引継ぎ計画',
    'check1402': '引継ぎ手順',
    'check1403': '引継ぎリスク',
    'check1404': '引継ぎスケジュール',
}


def get_title_from_check_titles(title):
    """
    指定されたtitleをkeyとして、check_titlesからtitleを取得する
    例) title: check01 -> title: プロジェクト概要
    :param title:
    :return:
    """
    return check_titles.get(title)

def get_kind_from_check_items(check_name):
    """
    指定されたcheck_nameをkeyとして、check_itemsからkindを取得する
    例) check_name: check0101 -> kind: 目的
    :param check_name:
    :return:
    """
    return check_items.get(check_name)

def set_selected_checks(check_title, check_item, selected_checks: dict):
    """
    指定されたcheck_titleとcheck_itemをselected_checksに追加する
    :param check_title:
    :param check_item:
    :param selected_checks:
    :return:
    """
    title = get_title_from_check_titles(check_title)
    if selected_checks.get(title) is None:
        selected_checks[title] = []
    selected_checks[title].append(get_kind_from_check_items(check_item))




class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        # with st.chat_message(sender.name):
        #     st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        st.session_state.messages.append({"role": sender.name, "content": message})
        return super()._process_received_message(message, sender, silent)

with st.container():
    st.markdown('### 要件定義作成')
    start_text = st.text_area('要件定義の大まかな内容を入力してください')

    st.markdown('##### 要件定義として作成する項目を選択してください')
    st.write('**プロジェクト概要**')
    col101, col102, col103 = st.columns(3)
    col104, col105, col106 = st.columns(3)
    col107, col108, col109 = st.columns(3)
    with col101:
        check0101 = st.checkbox(get_kind_from_check_items('check0101'))
    with col102:
        check0102 = st.checkbox(get_kind_from_check_items('check0102'))
    with col103:
        check0103 = st.checkbox(get_kind_from_check_items('check0103'))
    with col104:
        check0104 = st.checkbox(get_kind_from_check_items('check0104'))
    with col105:
        check0105 = st.checkbox(get_kind_from_check_items('check0105'))
    with col106:
        check0106 = st.checkbox(get_kind_from_check_items('check0106'))
    with col107:
        check0107 = st.checkbox(get_kind_from_check_items('check0107'))
    with col108:
        check0108 = st.checkbox(get_kind_from_check_items('check0108'))
    with col109:
        check0109 = st.checkbox(get_kind_from_check_items('check0109'))
    add_100 = st.text_area('プロジェクト概要補足')

    st.markdown('---')
    st.markdown('**機能要件**')
    col201, col202, col203 = st.columns(3)
    col204, col205, col206 = st.columns(3)
    col207, col208, col209 = st.columns(3)
    with col201:
        check0201 = st.checkbox(get_kind_from_check_items('check0201'))
    with col202:
        check0202 = st.checkbox(get_kind_from_check_items('check0202'))
    with col203:
        check0203 = st.checkbox(get_kind_from_check_items('check0203'))
    with col204:
        check0204 = st.checkbox(get_kind_from_check_items('check0204'))
    with col205:
        check0205 = st.checkbox(get_kind_from_check_items('check0205'))
    with col206:
        check0206 = st.checkbox(get_kind_from_check_items('check0206'))
    with col207:
        check0207 = st.checkbox(get_kind_from_check_items('check0207'))
    add_200 = st.text_area('機能要件補足')

    st.markdown('---')
    st.markdown('**データ要件**')
    col301, col302, col303 = st.columns(3)
    col304, col305, col306 = st.columns(3)
    col307, col308, col309 = st.columns(3)
    with col301:
        check0301 = st.checkbox(get_kind_from_check_items('check0301'))
    with col302:
        check0302 = st.checkbox(get_kind_from_check_items('check0302'))
    with col303:
        check0303 = st.checkbox(get_kind_from_check_items('check0303'))
    with col304:
        check0304 = st.checkbox(get_kind_from_check_items('check0304'))
    with col305:
        check0305 = st.checkbox(get_kind_from_check_items('check0305'))
    with col306:
        check0306 = st.checkbox(get_kind_from_check_items('check0306'))
    with col307:
        check0307 = st.checkbox(get_kind_from_check_items('check0307'))
    add_300 = st.text_area('データ要件補足')

    st.markdown('---')
    st.markdown('**非機能要件**')
    col401, col402, col403 = st.columns(3)
    col404, col405, col406 = st.columns(3)
    col407, col408, col409 = st.columns(3)
    with col401:
        check0401 = st.checkbox(get_kind_from_check_items('check0401'))
    with col402:
        check0402 = st.checkbox(get_kind_from_check_items('check0402'))
    with col403:
        check0403 = st.checkbox(get_kind_from_check_items('check0403'))
    with col404:
        check0404 = st.checkbox(get_kind_from_check_items('check0404'))
    with col405:
        check0405 = st.checkbox(get_kind_from_check_items('check0405'))
    with col406:
        check0406 = st.checkbox(get_kind_from_check_items('check0406'))
    with col407:
        check0407 = st.checkbox(get_kind_from_check_items('check0407'))
    with col408:
        check0408 = st.checkbox(get_kind_from_check_items('check0408'))
    with col409:
        check0409 = st.checkbox(get_kind_from_check_items('check0409'))
    add_400 = st.text_area('非機能要件補足')

    st.markdown('---')
    st.markdown('**制約条件**')
    col501, col502, col503 = st.columns(3)
    col504, col505, col506 = st.columns(3)
    col507, col508, col509 = st.columns(3)
    with col501:
        check0501 = st.checkbox(get_kind_from_check_items('check0501'))
    with col502:
        check0502 = st.checkbox(get_kind_from_check_items('check0502'))
    with col503:
        check0503 = st.checkbox(get_kind_from_check_items('check0503'))
    with col504:
        check0504 = st.checkbox(get_kind_from_check_items('check0504'))
    with col505:
        check0505 = st.checkbox(get_kind_from_check_items('check0505'))
    add_500 = st.text_area('制約条件補足')

    st.markdown('---')
    st.markdown('**リスク管理**')
    col601, col602, col603 = st.columns(3)
    col604, col605, col606 = st.columns(3)
    col607, col608, col609 = st.columns(3)
    with col601:
        check0601 = st.checkbox(get_kind_from_check_items('check0601'))
    with col602:
        check0602 = st.checkbox(get_kind_from_check_items('check0602'))
    with col603:
        check0603 = st.checkbox(get_kind_from_check_items('check0603'))
    with col604:
        check0604 = st.checkbox(get_kind_from_check_items('check0604'))
    with col605:
        check0605 = st.checkbox(get_kind_from_check_items('check0605'))
    with col606:
        check0606 = st.checkbox(get_kind_from_check_items('check0606'))
    add_600 = st.text_area('リスク管理補足')

    st.markdown('---')
    st.markdown('**テスト計画**')
    col701, col702, col703 = st.columns(3)
    col704, col705, col706 = st.columns(3)
    col707, col708, col709 = st.columns(3)
    with col701:
        check0701 = st.checkbox(get_kind_from_check_items('check0701'))
    with col702:
        check0702 = st.checkbox(get_kind_from_check_items('check0702'))
    with col703:
        check0703 = st.checkbox(get_kind_from_check_items('check0703'))
    with col704:
        check0704 = st.checkbox(get_kind_from_check_items('check0704'))
    with col705:
        check0705 = st.checkbox(get_kind_from_check_items('check0705'))
    with col706:
        check0706 = st.checkbox(get_kind_from_check_items('check0706'))
    add_700 = st.text_area('テスト計画補足')

    st.markdown('---')
    st.markdown('**承認と変更管理**')
    col801, col802, col803 = st.columns(3)
    col804, col805, col806 = st.columns(3)
    col807, col808, col809 = st.columns(3)
    with col801:
        check0801 = st.checkbox(get_kind_from_check_items('check0801'))
    with col802:
        check0802 = st.checkbox(get_kind_from_check_items('check0802'))
    with col803:
        check0803 = st.checkbox(get_kind_from_check_items('check0803'))
    add_800 = st.text_area('承認と変更管理補足')

    st.markdown('---')
    st.markdown('**プロジェクト計画**')
    col901, col902, col903 = st.columns(3)
    col904, col905, col906 = st.columns(3)
    col907, col908, col909 = st.columns(3)
    with col901:
        check0901 = st.checkbox(get_kind_from_check_items('check0901'))
    add_900 = st.text_area('プロジェクト計画補足')

    st.markdown('---')
    st.markdown('**運用と保守**')
    col1001, col1002, col1003 = st.columns(3)
    col1004, col1005, col1006 = st.columns(3)
    col1007, col1008, col1009 = st.columns(3)
    with col1001:
        check1001 = st.checkbox(get_kind_from_check_items('check1001'))
    with col1002:
        check1002 = st.checkbox(get_kind_from_check_items('check1002'))
    with col1003:
        check1003 = st.checkbox(get_kind_from_check_items('check1003'))
    add_1000 = st.text_area('運用と保守補足')

    st.markdown('---')
    st.markdown('**トレーニング**')
    col1101, col1102, col1103 = st.columns(3)
    col1104, col1105, col1106 = st.columns(3)
    col1107, col1108, col1109 = st.columns(3)
    with col1101:
        check1101 = st.checkbox(get_kind_from_check_items('check1101'))
    with col1102:
        check1102 = st.checkbox(get_kind_from_check_items('check1102'))
    with col1103:
        check1103 = st.checkbox(get_kind_from_check_items('check1103'))
    add_1100 = st.text_area('トレーニング補足')

    st.markdown('---')
    st.markdown('**ドキュメント**')
    col1201, col1202, col1203 = st.columns(3)
    col1204, col1205, col1206 = st.columns(3)
    col1207, col1208, col1209 = st.columns(3)
    with col1201:
        check1201 = st.checkbox(get_kind_from_check_items('check1201'))
    with col1202:
        check1202 = st.checkbox(get_kind_from_check_items('check1202'))
    with col1203:
        check1203 = st.checkbox(get_kind_from_check_items('check1203'))
    add_1200 = st.text_area('ドキュメント補足')

    st.markdown('---')
    st.markdown('**移行計画**')
    col1301, col1302, col1303 = st.columns(3)
    col1304, col1305, col1306 = st.columns(3)
    col1307, col1308, col1309 = st.columns(3)
    with col1301:
        check1301 = st.checkbox(get_kind_from_check_items('check1301'))
    with col1302:
        check1302 = st.checkbox(get_kind_from_check_items('check1302'))
    with col1303:
        check1303 = st.checkbox(get_kind_from_check_items('check1303'))
    with col1304:
        check1304 = st.checkbox(get_kind_from_check_items('check1304'))
    add_1300 = st.text_area('移行計画補足')

    st.markdown('---')
    st.markdown('**引継ぎ計画**')
    col1401, col1402, col1403 = st.columns(3)
    col1404, col1405, col1406 = st.columns(3)
    col1407, col1408, col1409 = st.columns(3)
    with col1401:
        check1401 = st.checkbox(get_kind_from_check_items('check1401'))
    with col1402:
        check1402 = st.checkbox(get_kind_from_check_items('check1402'))
    with col1403:
        check1403 = st.checkbox(get_kind_from_check_items('check1403'))
    with col1404:
        check1404 = st.checkbox(get_kind_from_check_items('check1404'))
    add_1400 = st.text_area('引継ぎ計画補足')

    st.markdown('---')
    st.markdown('**その他**')
    st.text_area('その他')


if start_text:
    create_documents = st.button(f'要件定義を作成する')
    if create_documents:
        st.session_state["messages"] = []
        writer = TrackableAssistantAgent(
            name="Writer",
            llm_config=llm_config,
            max_consecutive_auto_reply=2,
            system_message=f"""
                あなたは、アプリケーション開発における設計の専門家です。
                {start_text}の内容に即しつつ、指定された[タイトル]と[項目]に関する要件定義書を作成してください。
                [タイトル]は1つだけですが、[項目]は複数指定されている場合があります。
                [補足事項]が指示されていない場合はその部分は作成しないでください。
                [補足事項]が指示されている場合はそれも含めて作成してください。
                内容は日本語で記述してください。
                指定された[タイトル]と[項目]、[補足事項]以外は絶対に作成しないでください。
                作成する成果物としては最大で5000文字までとします。
                ドキュメントはMarkdown形式で記述してください。
                フロー図やクラス図、モデル、その他の図を記載する場合は必ずMarkdownもしくはMermaid形式で記述し、他のWebサイト等やリンクを利用しないでください。
                テーブル形式の場合はMarkdownのテーブル形式で記述してください。
                レビュアーから修正や指摘、フィードバックが与えられた場合は修正して再提出してください。
                """,
        )

        reviewer = TrackableAssistantAgent(
            name="Reviewer",
            llm_config=llm_config,
            max_consecutive_auto_reply=2,
            system_message=f"""
                        あなたは、設計の品質を向上させるためのフィードバックを提供するレビュアーです。
                        {start_text}の内容に即しつつ、要件定義書として指定された[タイトル]と[項目]、[補足事項]のみが作成されているか確認してください。
                        ただし、[補足事項]が無い場合は、その部分は作成されていなくても構いません。
                        指定された[タイトル]と[項目]、[補足事項]に関係しない内容が作成されている場合は削除するように指示してください。
                        {start_text}に要件定義書が適合しているか、設計の妥当性、完全性、および潜在的な問題点を特定し、改善提案を行い、設計者(Writer)にフィードバックを提供してください。
                        指定された[タイトル]と[項目]、[補足事項]以外の内容を追加するような指示は絶対にしないでください。
                        内容は日本語で記述してください。
                        """,
        )

        user_proxy = TrackableUserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
            code_execution_config=False,
        )

        selected_checks = {}
        if check0101:
            set_selected_checks('check01', 'check0101', selected_checks)
        if check0102:
            set_selected_checks('check01', 'check0102', selected_checks)
        if check0103:
            set_selected_checks('check01', 'check0103', selected_checks)
        if check0104:
            set_selected_checks('check01', 'check0104', selected_checks)
        if check0105:
            set_selected_checks('check01', 'check0105', selected_checks)
        if check0106:
            set_selected_checks('check01', 'check0106', selected_checks)
        if check0107:
            set_selected_checks('check01', 'check0107', selected_checks)
        if check0108:
            set_selected_checks('check01', 'check0108', selected_checks)
        if check0109:
            set_selected_checks('check01', 'check0109', selected_checks)
        if check0201:
            set_selected_checks('check02', 'check0201', selected_checks)
        if check0202:
            set_selected_checks('check02', 'check0202', selected_checks)
        if check0203:
            set_selected_checks('check02', 'check0203', selected_checks)
        if check0204:
            set_selected_checks('check02', 'check0204', selected_checks)
        if check0205:
            set_selected_checks('check02', 'check0205', selected_checks)
        if check0206:
            set_selected_checks('check02', 'check0206', selected_checks)
        if check0207:
            set_selected_checks('check02', 'check0207', selected_checks)
        if check0301:
            set_selected_checks('check03', 'check0301', selected_checks)
        if check0302:
            set_selected_checks('check03', 'check0302', selected_checks)
        if check0303:
            set_selected_checks('check03', 'check0303', selected_checks)
        if check0304:
            set_selected_checks('check03', 'check0304', selected_checks)
        if check0305:
            set_selected_checks('check03', 'check0305', selected_checks)
        if check0306:
            set_selected_checks('check03', 'check0306', selected_checks)
        if check0307:
            set_selected_checks('check03', 'check0307', selected_checks)
        if check0401:
            set_selected_checks('check04', 'check0401', selected_checks)
        if check0402:
            set_selected_checks('check04', 'check0402', selected_checks)
        if check0403:
            set_selected_checks('check04', 'check0403', selected_checks)
        if check0404:
            set_selected_checks('check04', 'check0404', selected_checks)
        if check0405:
            set_selected_checks('check04', 'check0405', selected_checks)
        if check0406:
            set_selected_checks('check04', 'check0406', selected_checks)
        if check0407:
            set_selected_checks('check04', 'check0407', selected_checks)
        if check0408:
            set_selected_checks('check04', 'check0408', selected_checks)
        if check0409:
            set_selected_checks('check04', 'check0409', selected_checks)
        if check0501:
            set_selected_checks('check05', 'check0501', selected_checks)
        if check0502:
            set_selected_checks('check05', 'check0502', selected_checks)
        if check0503:
            set_selected_checks('check05', 'check0503', selected_checks)
        if check0504:
            set_selected_checks('check05', 'check0504', selected_checks)
        if check0505:
            set_selected_checks('check05', 'check0505', selected_checks)
        if check0601:
            set_selected_checks('check06', 'check0601', selected_checks)
        if check0602:
            set_selected_checks('check06', 'check0602', selected_checks)
        if check0603:
            set_selected_checks('check06', 'check0603', selected_checks)
        if check0604:
            set_selected_checks('check06', 'check0604', selected_checks)
        if check0605:
            set_selected_checks('check06', 'check0605', selected_checks)
        if check0606:
            set_selected_checks('check06', 'check0606', selected_checks)
        if check0701:
            set_selected_checks('check07', 'check0701', selected_checks)
        if check0702:
            set_selected_checks('check07', 'check0702', selected_checks)
        if check0703:
            set_selected_checks('check07', 'check0703', selected_checks)
        if check0704:
            set_selected_checks('check07', 'check0704', selected_checks)
        if check0705:
            set_selected_checks('check07', 'check0705', selected_checks)
        if check0706:
            set_selected_checks('check07', 'check0706', selected_checks)
        if check0801:
            set_selected_checks('check08', 'check0801', selected_checks)
        if check0802:
            set_selected_checks('check08', 'check0802', selected_checks)
        if check0803:
            set_selected_checks('check08', 'check0803', selected_checks)
        if check0901:
            set_selected_checks('check09', 'check0901', selected_checks)
        if check1001:
            set_selected_checks('check10', 'check1001', selected_checks)
        if check1002:
            set_selected_checks('check10', 'check1002', selected_checks)
        if check1003:
            set_selected_checks('check10', 'check1003', selected_checks)
        if check1101:
            set_selected_checks('check11', 'check1101', selected_checks)
        if check1102:
            set_selected_checks('check11', 'check1102', selected_checks)
        if check1103:
            set_selected_checks('check11', 'check1103', selected_checks)
        if check1201:
            set_selected_checks('check12', 'check1201', selected_checks)
        if check1202:
            set_selected_checks('check12', 'check1202', selected_checks)
        if check1203:
            set_selected_checks('check12', 'check1203', selected_checks)
        if check1301:
            set_selected_checks('check13', 'check1301', selected_checks)
        if check1302:
            set_selected_checks('check13', 'check1302', selected_checks)
        if check1303:
            set_selected_checks('check13', 'check1303', selected_checks)
        if check1304:
            set_selected_checks('check13', 'check1304', selected_checks)
        if check1401:
            set_selected_checks('check14', 'check1401', selected_checks)
        if check1402:
            set_selected_checks('check14', 'check1402', selected_checks)
        if check1403:
            set_selected_checks('check14', 'check1403', selected_checks)
        if check1404:
            set_selected_checks('check14', 'check1404', selected_checks)



        for title in selected_checks.keys():
            check_items = selected_checks[title]
            print(f'タイトル: [{title}], 項目: {check_items}',)

            user_proxy.initiate_chats(
                [
                    {
                        "chat_id": 0,
                        "recipient": writer,
                        "message": f'タイトル: [{title}], 項目: {check_items}',
                        "clear_history": True,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    },
                    {
                        "chat_id": 1,
                        "recipient": reviewer,
                        "message": f'タイトル: [{title}], 項目: {check_items}',
                        "clear_history": False,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    },
                    {
                        "chat_id": 2,
                        "recipient": writer,
                        "message": f'タイトル: [{title}], 項目: {check_items}. 最終版として完成させてください。',
                        "clear_history": False,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    },
                    # {
                    #     "chat_id": 3,
                    #     "recipient": reviewer,
                    #     "message": f'タイトル: [{title}], 項目: {check_items}',
                    #     "clear_history": False,
                    #     "silent": False,
                    #     "max_turns": 1,
                    #     "summary_method": "last_msg"
                    # },
                    # {
                    #     "chat_id": 4,
                    #     "recipient": writer,
                    #     "message": f'タイトル: [{title}], 項目: {check_items}',
                    #     "clear_history": False,
                    #     "silent": False,
                    #     "max_turns": 1,
                    #     "summary_method": "last_msg"
                    # },
                ]
            )

if st.button('Show messages'):
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])



        # user_input = st.chat_input("check0101: false")
