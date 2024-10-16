import autogen
from autogen import AssistantAgent, UserProxyAgent
import streamlit as st
import json
import pprint as pp

# LLMの設定
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


# RequirementDocumentItems.jsonのデータを読み込む
with open('pages/RequirementDocumentItems.json', 'r', encoding='utf-8') as f:
    requirement_document_items = json.load(f).get('requirements')


# チャットメッセージを格納するリスト
if "messages" not in st.session_state:
    print('initialize st.session_state.messages')
    st.session_state["messages"] = []



class TrackableAssistantAgent(AssistantAgent):
    """
    AssistantAgentを継承して、メッセージをトラッキングする機能を追加します。
    AssistantAgentに対する指示も表示されるため、通常は使用しないことをお勧めします。
    """
    def _process_received_message(self, message, sender, silent):
        # with st.chat_message(sender.name):
        #     st.markdown(message)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    """
    UserProxyAgentを継承して、メッセージをトラッキングする機能を追加します。
    AssistantAgentからの回答を表示できるため、こちらを使用することをお勧めします。
    """
    def _process_received_message(self, message, sender, silent):
        # st.chat_message(sender.name).write(message)
        # with st.chat_message(sender.name):
        #     st.markdown(message)
        st.session_state.messages.append({"role": sender.name, "content": message})
        return super()._process_received_message(message, sender, silent)



def print_messages(recipient, messages, sender, config):
    print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")

    msg = messages[-1]['content']

    with st.chat_message(sender.name):
        st.markdown(msg)

    return False, None #conversation continued


def create_message(title, subjects: [], appendix, check_messages: dict):
    """
    チェックメッセージを作成します
    :param title:
    :param subjects:
    :param appendix:
    :param check_messages:
    :return:
    """
    if title not in check_messages:
        check_messages[title] = {
            "subjects": subjects,
            "appendix": appendix
        }
    # もしタイトルがすでに辞書に存在していたら、そのタイトルのsubjectリスト、補足に変更する
    else:
        check_messages[title]["subjects"] = subjects
        check_messages[title]["appendix"] = appendix


# 要件定義書の作成項目をJSONファイルから読み込んで表示させます
# JSONファイルを読み込んで使用しているので、各項目の表示名等を変更する場合はJSONファイルを変更してください
# 各項目のチェックボックスに表示されるものは、最大で9つまで表示されます
# 抽象化しているため、項目数が変わっても自動的に対応しますが、直接コードに設定するのもありかもです
# とりあえず、件数としては最大14, 各項目の最大件数は9としています
with st.container():
    st.markdown('### 要件定義作成')
    # requirement_document_itemsからtitleとitemsを取得
    overview = st.text_area("要件定義概要")
    for item in requirement_document_items:
        title = item.get('title')
        st.markdown(f"**{title}**")

        title_index = item.get('title_index')
        if title_index == "01":
            title01 = title
            col0101, col0102, col0103 = st.columns(3)
            col0104, col0105, col0106 = st.columns(3)
            col0107, col0108, col0109 = st.columns(3)
            check0101, check0102, check0103 = False, False, False
            check0104, check0105, check0106 = False, False, False
            check0107, check0108, check0109 = False, False, False
            subject0101, subject0102, subject0103 = "", "", ""
            subject0104, subject0105, subject0106 = "", "", ""
            subject0107, subject0108, subject0109 = "", "", ""
            appendix01 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0101:
                        check0101 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0101 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0102:
                        check0102 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0102 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0103:
                        check0103 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0103 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0104:
                        check0104 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0104 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0105:
                        check0105 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0105 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0106:
                        check0106 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0106 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0107:
                        check0107 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0107 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0108:
                        check0108 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0108 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0109:
                        check0109 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0109 = subject.get('subject')
            appendix01 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "02":
            title02 = title
            col0201, col0202, col0203 = st.columns(3)
            col0204, col0205, col0206 = st.columns(3)
            col0207, col0208, col0209 = st.columns(3)
            check0201, check0202, check0203 = False, False, False
            check0204, check0205, check0206 = False, False, False
            check0207, check0208, check0209 = False, False, False
            subject0201, subject0202, subject0203 = "", "", ""
            subject0204, subject0205, subject0206 = "", "", ""
            subject0207, subject0208, subject0209 = "", "", ""
            appendix02 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0201:
                        check0201 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0201 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0202:
                        check0202 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0202 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0203:
                        check0203 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0203 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0204:
                        check0204 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0204 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0205:
                        check0205 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0205 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0206:
                        check0206 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0206 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0207:
                        check0207 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0207 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0208:
                        check0208 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0208 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0209:
                        check0209 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0209 = subject.get('subject')
            appendix02 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "03":
            title03 = title
            col0301, col0302, col0303 = st.columns(3)
            col0304, col0305, col0306 = st.columns(3)
            col0307, col0308, col0309 = st.columns(3)
            check0301, check0302, check0303 = False, False, False
            check0304, check0305, check0306 = False, False, False
            check0307, check0308, check0309 = False, False, False
            subject0301, subject0302, subject0303 = "", "", ""
            subject0304, subject0305, subject0306 = "", "", ""
            subject0307, subject0308, subject0309 = "", "", ""
            appendix03 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0301:
                        check0301 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0301 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0302:
                        check0302 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0302 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0303:
                        check0303 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0303 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0304:
                        check0304 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0304 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0305:
                        check0305 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0305 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0306:
                        check0306 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0306 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0307:
                        check0307 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0307 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0308:
                        check0308 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0308 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0309:
                        check0309 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0309 = subject.get('subject')
            appendix03 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "04":
            title04 = title
            col0401, col0402, col0403 = st.columns(3)
            col0404, col0405, col0406 = st.columns(3)
            col0407, col0408, col0409 = st.columns(3)
            check0401, check0402, check0403 = False, False, False
            check0404, check0405, check0406 = False, False, False
            check0407, check0408, check0409 = False, False, False
            subject0401, subject0402, subject0403 = "", "", ""
            subject0404, subject0405, subject0406 = "", "", ""
            subject0407, subject0408, subject0409 = "", "", ""
            appendix04 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0401:
                        check0401 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0401 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0402:
                        check0402 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0402 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0403:
                        check0403 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0403 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0404:
                        check0404 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0404 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0405:
                        check0405 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0405 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0406:
                        check0406 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0406 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0407:
                        check0407 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0407 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0408:
                        check0408 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0408 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0409:
                        check0409 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0409 = subject.get('subject')
            appendix04 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "05":
            title05 = title
            col0501, col0502, col0503 = st.columns(3)
            col0504, col0505, col0506 = st.columns(3)
            col0507, col0508, col0509 = st.columns(3)
            check0501, check0502, check0503 = False, False, False
            check0504, check0505, check0506 = False, False, False
            check0507, check0508, check0509 = False, False, False
            subject0501, subject0502, subject0503 = "", "", ""
            subject0504, subject0505, subject0506 = "", "", ""
            subject0507, subject0508, subject0509 = "", "", ""
            appendix05 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0501:
                        check0501 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0501 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0502:
                        check0502 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0502 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0503:
                        check0503 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0503 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0504:
                        check0504 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0504 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0505:
                        check0505 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0505 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0506:
                        check0506 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0506 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0507:
                        check0507 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0507 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0508:
                        check0508 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0508 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0509:
                        check0509 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0509 = subject.get('subject')
            appendix05 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "06":
            title06 = title
            col0601, col0602, col0603 = st.columns(3)
            col0604, col0605, col0606 = st.columns(3)
            col0607, col0608, col0609 = st.columns(3)
            check0601, check0602, check0603 = False, False, False
            check0604, check0605, check0606 = False, False, False
            check0607, check0608, check0609 = False, False, False
            subject0601, subject0602, subject0603 = "", "", ""
            subject0604, subject0605, subject0606 = "", "", ""
            subject0607, subject0608, subject0609 = "", "", ""
            appendix06 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0601:
                        check0601 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0601 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0602:
                        check0602 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0602 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0603:
                        check0603 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0603 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0604:
                        check0604 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0604 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0605:
                        check0605 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0605 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0606:
                        check0606 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0606 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0607:
                        check0607 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0607 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0608:
                        check0608 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0608 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0609:
                        check0609 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0609 = subject.get('subject')
            appendix06 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "07":
            title07 = title
            col0701, col0702, col0703 = st.columns(3)
            col0704, col0705, col0706 = st.columns(3)
            col0707, col0708, col0709 = st.columns(3)
            check0701, check0702, check0703 = False, False, False
            check0704, check0705, check0706 = False, False, False
            check0707, check0708, check0709 = False, False, False
            subject0701, subject0702, subject0703 = "", "", ""
            subject0704, subject0705, subject0706 = "", "", ""
            subject0707, subject0708, subject0709 = "", "", ""
            appendix07 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0701:
                        check0701 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0701 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0702:
                        check0702 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0702 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0703:
                        check0703 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0703 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0704:
                        check0704 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0704 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0705:
                        check0705 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0705 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0706:
                        check0706 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0706 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0707:
                        check0707 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0707 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0708:
                        check0708 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0708 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0709:
                        check0709 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0709 = subject.get('subject')
            appendix07 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "08":
            title08 = title
            col0801, col0802, col0803 = st.columns(3)
            col0804, col0805, col0806 = st.columns(3)
            col0807, col0808, col0809 = st.columns(3)
            check0801, check0802, check0803 = False, False, False
            check0804, check0805, check0806 = False, False, False
            check0807, check0808, check0809 = False, False, False
            subject0801, subject0802, subject0803 = "", "", ""
            subject0804, subject0805, subject0806 = "", "", ""
            subject0807, subject0808, subject0809 = "", "", ""
            appendix08 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0801:
                        check0801 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0801 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0802:
                        check0802 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0802 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0803:
                        check0803 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0803 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0804:
                        check0804 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0804 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0805:
                        check0805 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0805 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0806:
                        check0806 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0806 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0807:
                        check0807 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0807 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0808:
                        check0808 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0808 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0809:
                        check0809 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0809 = subject.get('subject')
            appendix08 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "09":
            title09 = title
            col0901, col0902, col0903 = st.columns(3)
            col0904, col0905, col0906 = st.columns(3)
            col0907, col0908, col0909 = st.columns(3)
            check0901, check0902, check0903 = False, False, False
            check0904, check0905, check0906 = False, False, False
            check0907, check0908, check0909 = False, False, False
            subject0901, subject0902, subject0903 = "", "", ""
            subject0904, subject0905, subject0906 = "", "", ""
            subject0907, subject0908, subject0909 = "", "", ""
            appendix09 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col0901:
                        check0901 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0901 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col0902:
                        check0902 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0902 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col0903:
                        check0903 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0903 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col0904:
                        check0904 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0904 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col0905:
                        check0905 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0905 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col0906:
                        check0906 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0906 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col0907:
                        check0907 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0907 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col0908:
                        check0908 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0908 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col0909:
                        check0909 = st.checkbox(f"{subject.get('subject')}", False)
                        subject0909 = subject.get('subject')
            appendix09 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "10":
            title10 = title
            col1001, col1002, col1003 = st.columns(3)
            col1004, col1005, col1006 = st.columns(3)
            col1007, col1008, col1009 = st.columns(3)
            check1001, check1002, check1003 = False, False, False
            check1004, check1005, check1006 = False, False, False
            check1007, check1008, check1009 = False, False, False
            subject1001, subject1002, subject1003 = "", "", ""
            subject1004, subject1005, subject1006 = "", "", ""
            subject1007, subject1008, subject1009 = "", "", ""
            appendix10 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col1001:
                        check1001 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1001 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col1002:
                        check1002 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1002 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col1003:
                        check1003 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1003 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col1004:
                        check1004 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1004 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col1005:
                        check1005 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1005 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col1006:
                        check1006 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1006 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col1007:
                        check1007 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1007 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col1008:
                        check1008 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1008 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col1009:
                        check1009 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1009 = subject.get('subject')
            appendix10 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "11":
            title11 = title
            col1101, col1102, col1103 = st.columns(3)
            col1104, col1105, col1106 = st.columns(3)
            col1107, col1108, col1109 = st.columns(3)
            check1101, check1102, check1103 = False, False, False
            check1104, check1105, check1106 = False, False, False
            check1107, check1108, check1109 = False, False, False
            subject1101, subject1102, subject1103 = "", "", ""
            subject1104, subject1105, subject1106 = "", "", ""
            subject1107, subject1108, subject1109 = "", "", ""
            appendix11 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col1101:
                        check1101 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1101 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col1102:
                        check1102 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1102 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col1103:
                        check1103 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1103 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col1104:
                        check1104 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1104 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col1105:
                        check1105 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1105 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col1106:
                        check1106 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1106 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col1107:
                        check1107 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1107 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col1108:
                        check1108 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1108 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col1109:
                        check1109 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1109 = subject.get('subject')
            appendix11 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "12":
            title12 = title
            col1201, col1202, col1203 = st.columns(3)
            col1204, col1205, col1206 = st.columns(3)
            col1207, col1208, col1209 = st.columns(3)
            check1201, check1202, check1203 = False, False, False
            check1204, check1205, check1206 = False, False, False
            check1207, check1208, check1209 = False, False, False
            subject1201, subject1202, subject1203 = "", "", ""
            subject1204, subject1205, subject1206 = "", "", ""
            subject1207, subject1208, subject1209 = "", "", ""
            appendix12 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col1201:
                        check1201 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1201 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col1202:
                        check1202 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1202 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col1203:
                        check1203 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1203 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col1204:
                        check1204 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1204 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col1205:
                        check1205 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1205 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col1206:
                        check1206 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1206 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col1207:
                        check1207 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1207 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col1208:
                        check1208 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1208 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col1209:
                        check1209 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1209 = subject.get('subject')
            appendix12 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "13":
            title13 = title
            col1301, col1302, col1303 = st.columns(3)
            col1304, col1305, col1306 = st.columns(3)
            col1307, col1308, col1309 = st.columns(3)
            check1301, check1302, check1303 = False, False, False
            check1304, check1305, check1306 = False, False, False
            check1307, check1308, check1309 = False, False, False
            subject1301, subject1302, subject1303 = "", "", ""
            subject1304, subject1305, subject1306 = "", "", ""
            subject1307, subject1308, subject1309 = "", "", ""
            appendix13 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col1301:
                        check1301 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1301 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col1302:
                        check1302 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1302 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col1303:
                        check1303 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1303 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col1304:
                        check1304 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1304 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col1305:
                        check1305 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1305 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col1306:
                        check1306 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1306 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col1307:
                        check1307 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1307 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col1308:
                        check1308 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1308 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col1309:
                        check1309 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1309 = subject.get('subject')
            appendix13 = st.text_area(f"{item.get('title')}補足")

        elif title_index == "14":
            title14 = title
            col1401, col1402, col1403 = st.columns(3)
            col1404, col1405, col1406 = st.columns(3)
            col1407, col1408, col1409 = st.columns(3)
            check1401, check1402, check1403 = False, False, False
            check1404, check1405, check1406 = False, False, False
            check1407, check1408, check1409 = False, False, False
            subject1401, subject1402, subject1403 = "", "", ""
            subject1404, subject1405, subject1406 = "", "", ""
            subject1407, subject1408, subject1409 = "", "", ""
            appendix14 = ""
            items = item.get('items')
            for i, subject in enumerate(items):
                if subject.get('subject_index') == "01":
                    with col1401:
                        check1401 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1401 = subject.get('subject')
                elif subject.get('subject_index') == "02":
                    with col1402:
                        check1402 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1402 = subject.get('subject')
                elif subject.get('subject_index') == "03":
                    with col1403:
                        check1403 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1403 = subject.get('subject')
                elif subject.get('subject_index') == "04":
                    with col1404:
                        check1404 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1404 = subject.get('subject')
                elif subject.get('subject_index') == "05":
                    with col1405:
                        check1405 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1405 = subject.get('subject')
                elif subject.get('subject_index') == "06":
                    with col1406:
                        check1406 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1406 = subject.get('subject')
                elif subject.get('subject_index') == "07":
                    with col1407:
                        check1407 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1407 = subject.get('subject')
                elif subject.get('subject_index') == "08":
                    with col1408:
                        check1408 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1408 = subject.get('subject')
                elif subject.get('subject_index') == "09":
                    with col1409:
                        check1409 = st.checkbox(f"{subject.get('subject')}", False)
                        subject1409 = subject.get('subject')
            appendix14 = st.text_area(f"{item.get('title')}補足")

    appendix_other = st.text_area("**その他**")


# """項目入力"""
check_messages = {}
if overview:
    check_messages = {}
    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0101:
        temp_title = title01
        temp_subjects.append(subject0101)
    if check0102:
        temp_title = title01
        temp_subjects.append(subject0102)
    if check0103:
        temp_title = title01
        temp_subjects.append(subject0103)
    if check0104:
        temp_title = title01
        temp_subjects.append(subject0104)
    if check0105:
        temp_title = title01
        temp_subjects.append(subject0105)
    if check0106:
        temp_title = title01
        temp_subjects.append(subject0106)
    if check0107:
        temp_title = title01
        temp_subjects.append(subject0107)
    if check0108:
        temp_title = title01
        temp_subjects.append(subject0108)
    if check0109:
        temp_title = title01
        temp_subjects.append(subject0109)
    if appendix01:
        temp_title = title01
        temp_appendix = appendix01
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0201:
        temp_title = title02
        temp_subjects.append(subject0201)
    if check0202:
        temp_title = title02
        temp_subjects.append(subject0202)
    if check0203:
        temp_title = title02
        temp_subjects.append(subject0203)
    if check0204:
        temp_title = title02
        temp_subjects.append(subject0204)
    if check0205:
        temp_title = title02
        temp_subjects.append(subject0205)
    if check0206:
        temp_title = title02
        temp_subjects.append(subject0206)
    if check0207:
        temp_title = title02
        temp_subjects.append(subject0207)
    if check0208:
        temp_title = title02
        temp_subjects.append(subject0208)
    if check0209:
        temp_title = title02
        temp_subjects.append(subject0209)
    if appendix02:
        temp_title = title02
        temp_appendix = appendix02
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0301:
        temp_title = title03
        temp_subjects.append(subject0301)
    if check0302:
        temp_title = title03
        temp_subjects.append(subject0302)
    if check0303:
        temp_title = title03
        temp_subjects.append(subject0303)
    if check0304:
        temp_title = title03
        temp_subjects.append(subject0304)
    if check0305:
        temp_title = title03
        temp_subjects.append(subject0305)
    if check0306:
        temp_title = title03
        temp_subjects.append(subject0306)
    if check0307:
        temp_title = title03
        temp_subjects.append(subject0307)
    if check0308:
        temp_title = title03
        temp_subjects.append(subject0308)
    if check0309:
        temp_title = title03
        temp_subjects.append(subject0309)
    if appendix03:
        temp_title = title03
        temp_appendix = appendix03
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0401:
        temp_title = title04
        temp_subjects.append(subject0401)
    if check0402:
        temp_title = title04
        temp_subjects.append(subject0402)
    if check0403:
        temp_title = title04
        temp_subjects.append(subject0403)
    if check0404:
        temp_title = title04
        temp_subjects.append(subject0404)
    if check0405:
        temp_title = title04
        temp_subjects.append(subject0405)
    if check0406:
        temp_title = title04
        temp_subjects.append(subject0406)
    if check0407:
        temp_title = title04
        temp_subjects.append(subject0407)
    if check0408:
        temp_title = title04
        temp_subjects.append(subject0408)
    if check0409:
        temp_title = title04
        temp_subjects.append(subject0409)
    if appendix04:
        temp_title = title04
        temp_appendix = appendix04
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0501:
        temp_title = title05
        temp_subjects.append(subject0501)
    if check0502:
        temp_title = title05
        temp_subjects.append(subject0502)
    if check0503:
        temp_title = title05
        temp_subjects.append(subject0503)
    if check0504:
        temp_title = title05
        temp_subjects.append(subject0504)
    if check0505:
        temp_title = title05
        temp_subjects.append(subject0505)
    if check0506:
        temp_title = title05
        temp_subjects.append(subject0506)
    if check0507:
        temp_title = title05
        temp_subjects.append(subject0507)
    if check0508:
        temp_title = title05
        temp_subjects.append(subject0508)
    if check0509:
        temp_title = title05
        temp_subjects.append(subject0509)
    if appendix05:
        temp_title = title05
        temp_appendix = appendix05
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0601:
        temp_title = title06
        temp_subjects.append(subject0601)
    if check0602:
        temp_title = title06
        temp_subjects.append(subject0602)
    if check0603:
        temp_title = title06
        temp_subjects.append(subject0603)
    if check0604:
        temp_title = title06
        temp_subjects.append(subject0604)
    if check0605:
        temp_title = title06
        temp_subjects.append(subject0605)
    if check0606:
        temp_title = title06
        temp_subjects.append(subject0606)
    if check0607:
        temp_title = title06
        temp_subjects.append(subject0607)
    if check0608:
        temp_title = title06
        temp_subjects.append(subject0608)
    if check0609:
        temp_title = title06
        temp_subjects.append(subject0609)
    if appendix06:
        temp_title = title06
        temp_appendix = appendix06
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0701:
        temp_title = title07
        temp_subjects.append(subject0701)
    if check0702:
        temp_title = title07
        temp_subjects.append(subject0702)
    if check0703:
        temp_title = title07
        temp_subjects.append(subject0703)
    if check0704:
        temp_title = title07
        temp_subjects.append(subject0704)
    if check0705:
        temp_title = title07
        temp_subjects.append(subject0705)
    if check0706:
        temp_title = title07
        temp_subjects.append(subject0706)
    if check0707:
        temp_title = title07
        temp_subjects.append(subject0707)
    if check0708:
        temp_title = title07
        temp_subjects.append(subject0708)
    if check0709:
        temp_title = title07
        temp_subjects.append(subject0709)
    if appendix07:
        temp_title = title07
        temp_appendix = appendix07
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0801:
        temp_title = title08
        temp_subjects.append(subject0801)
    if check0802:
        temp_title = title08
        temp_subjects.append(subject0802)
    if check0803:
        temp_title = title08
        temp_subjects.append(subject0803)
    if check0804:
        temp_title = title08
        temp_subjects.append(subject0804)
    if check0805:
        temp_title = title08
        temp_subjects.append(subject0805)
    if check0806:
        temp_title = title08
        temp_subjects.append(subject0806)
    if check0807:
        temp_title = title08
        temp_subjects.append(subject0807)
    if check0808:
        temp_title = title08
        temp_subjects.append(subject0808)
    if check0809:
        temp_title = title08
        temp_subjects.append(subject0809)
    if appendix08:
        temp_title = title08
        temp_appendix = appendix08
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check0901:
        temp_title = title09
        temp_subjects.append(subject0901)
    if check0902:
        temp_title = title09
        temp_subjects.append(subject0902)
    if check0903:
        temp_title = title09
        temp_subjects.append(subject0903)
    if check0904:
        temp_title = title09
        temp_subjects.append(subject0904)
    if check0905:
        temp_title = title09
        temp_subjects.append(subject0905)
    if check0906:
        temp_title = title09
        temp_subjects.append(subject0906)
    if check0907:
        temp_title = title09
        temp_subjects.append(subject0907)
    if check0908:
        temp_title = title09
        temp_subjects.append(subject0908)
    if check0909:
        temp_title = title09
        temp_subjects.append(subject0909)
    if appendix09:
        temp_title = title09
        temp_appendix = appendix09
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check1001:
        temp_title = title10
        temp_subjects.append(subject1001)
    if check1002:
        temp_title = title10
        temp_subjects.append(subject1002)
    if check1003:
        temp_title = title10
        temp_subjects.append(subject1003)
    if check1004:
        temp_title = title10
        temp_subjects.append(subject1004)
    if check1005:
        temp_title = title10
        temp_subjects.append(subject1005)
    if check1006:
        temp_title = title10
        temp_subjects.append(subject1006)
    if check1007:
        temp_title = title10
        temp_subjects.append(subject1007)
    if check1008:
        temp_title = title10
        temp_subjects.append(subject1008)
    if check1009:
        temp_title = title10
        temp_subjects.append(subject1009)
    if appendix10:
        temp_title = title10
        temp_appendix = appendix10
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check1101:
        temp_title = title11
        temp_subjects.append(subject1101)
    if check1102:
        temp_title = title11
        temp_subjects.append(subject1102)
    if check1103:
        temp_title = title11
        temp_subjects.append(subject1103)
    if check1104:
        temp_title = title11
        temp_subjects.append(subject1104)
    if check1105:
        temp_title = title11
        temp_subjects.append(subject1105)
    if check1106:
        temp_title = title11
        temp_subjects.append(subject1106)
    if check1107:
        temp_title = title11
        temp_subjects.append(subject1107)
    if check1108:
        temp_title = title11
        temp_subjects.append(subject1108)
    if check1109:
        temp_title = title11
        temp_subjects.append(subject1109)
    if appendix11:
        temp_title = title11
        temp_appendix = appendix11
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check1201:
        temp_title = title12
        temp_subjects.append(subject1201)
    if check1202:
        temp_title = title12
        temp_subjects.append(subject1202)
    if check1203:
        temp_title = title12
        temp_subjects.append(subject1203)
    if check1204:
        temp_title = title12
        temp_subjects.append(subject1204)
    if check1205:
        temp_title = title12
        temp_subjects.append(subject1205)
    if check1206:
        temp_title = title12
        temp_subjects.append(subject1206)
    if check1207:
        temp_title = title12
        temp_subjects.append(subject1207)
    if check1208:
        temp_title = title12
        temp_subjects.append(subject1208)
    if check1209:
        temp_title = title12
        temp_subjects.append(subject1209)
    if appendix12:
        temp_title = title12
        temp_appendix = appendix12
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check1301:
        temp_title = title13
        temp_subjects.append(subject1301)
    if check1302:
        temp_title = title13
        temp_subjects.append(subject1302)
    if check1303:
        temp_title = title13
        temp_subjects.append(subject1303)
    if check1304:
        temp_title = title13
        temp_subjects.append(subject1304)
    if check1305:
        temp_title = title13
        temp_subjects.append(subject1305)
    if check1306:
        temp_title = title13
        temp_subjects.append(subject1306)
    if check1307:
        temp_title = title13
        temp_subjects.append(subject1307)
    if check1308:
        temp_title = title13
        temp_subjects.append(subject1308)
    if check1309:
        temp_title = title13
        temp_subjects.append(subject1309)
    if appendix13:
        temp_title = title13
        temp_appendix = appendix13
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    temp_title = ""
    temp_subjects = []
    temp_appendix = ""
    if check1401:
        temp_title = title14
        temp_subjects.append(subject1401)
    if check1402:
        temp_title = title14
        temp_subjects.append(subject1402)
    if check1403:
        temp_title = title14
        temp_subjects.append(subject1403)
    if check1404:
        temp_title = title14
        temp_subjects.append(subject1404)
    if check1405:
        temp_title = title14
        temp_subjects.append(subject1405)
    if check1406:
        temp_title = title14
        temp_subjects.append(subject1406)
    if check1407:
        temp_title = title14
        temp_subjects.append(subject1407)
    if check1408:
        temp_title = title14
        temp_subjects.append(subject1408)
    if check1409:
        temp_title = title14
        temp_subjects.append(subject1409)
    if appendix14:
        temp_title = title14
        temp_appendix = appendix14
    if temp_title:
        create_message(temp_title, subjects=temp_subjects, appendix=temp_appendix, check_messages=check_messages)

    if appendix_other:
        create_message("その他",subjects=[], appendix=appendix_other, check_messages=check_messages)

    # チャット開始
    if st.button("作成"):
        st.session_state.messages = []

        def create_writer_task(requirement_documents_summary, title, subjects, appendix):
            return f"""
        Role:
        - あなたは、アプリケーション開発における設計の専門家です。
        Task:
        - [要件定義書概要]に関する要件定義書のうち、指定された[タイトル]と[項目]、[追記]に関する部分を作成してください。
        - 要件定義書を作成するにあたって不足している情報がある場合は、ユーザーに対し質問を行ってください。
        - 日本語で回答してください。
        Format:
        - 要件定義書はMarkdown形式で記述してください。
        - 図・フローチャート・テーブル等を記載する場合は、MarkdownもしくはMermaid形式で記述してください。
        - 最大で5000文字までとします。
        制限:
        - 指定された[要件定義書概要]、[タイトル]、[項目]、[追記]に関係ない事項を絶対に作成しないでください。
        - ウェブサイト等のリンクを利用しないでください。
        - 画像を利用しないでください。
        - レビュアーからの文言は含めず、要件定義書のみを作成してください。
        作成項目:
        - [要件定義書概要]: {requirement_documents_summary}
        - [タイトル]: {title}
        - [項目]: {subjects}
        - [追記]: {appendix}
        """


        def create_reviewer_task(requirement_documents_summary, title, subjects, appendix):
            return f"""
        Role:
        - あなたは、アプリケーション開発における設計の専門家です。
        Task:
        - 設計者が作成した要件定義書をレビューしてください。 
        - 要件定義書に不備がある場合は、指摘を行ってください。
        - 要件定義書作成項目に対するレビューを行い、それ以外に関してはレビューを行わないでください。
        - レビュー対象は[要件定義書概要]に関する要件定義書のうち指定された[タイトル]と[項目]、[追記]に関する部分のみです。
        - 日本語で回答してください。
        要件定義書作成項目:
        - [要件定義書概要]: {requirement_documents_summary}
        - [タイトル]: {title}
        - [項目]: {subjects}
        - [追記]: {appendix}
        要件定義書作成ルール:
        - Format
          - 要件定義書はMarkdown形式で記述してください。
          - 図・フローチャート・テーブル等を記載する場合は、MarkdownもしくはMermaid形式で記述してください。
          - 最大で5000文字までとします。
        - 制限
          - 指定された[タイトル]と[項目]、[追記]に関係ない事項を絶対に作成しないでください。
          - ウェブサイト等のリンクを利用しないでください。
          - 画像を利用しないでください。
        レビュー観点:
        - 要件定義書が指示内容に従っているか
        - 要件定義書が正確かつ明確に記述されているか
        - 要件定義書が適切な情報を提供しているか
        - 要件定義書が適切なフォーマットで記述されているか
        - 要件定義書作成ルールに違反していないか
        - 誤字脱字がないか
        - 表現や文体は統一感があるか
        - その他、必要に応じて指摘してください。
        """

        for title in check_messages.keys():
            writer = TrackableAssistantAgent(
                name="Writer",
                llm_config=llm_config,
                max_consecutive_auto_reply=2,
                system_message="あなたは、アプリケーション開発における設計の専門家です。日本語で会話をしてください。"
            )
            # writer.register_reply(
            #     trigger=[autogen.Agent, None],
            #     reply_func=print_messages,
            #     config={"callback": None}
            # )

            reviewer = TrackableAssistantAgent(
                name="Reviewer",
                llm_config=llm_config,
                max_consecutive_auto_reply=2,
                system_message="あなたは、アプリケーション開発における設計の専門家です。日本語で会話をしてください。",
            )
            # reviewer.register_reply(
            #     trigger=[autogen.Agent, None],
            #     reply_func=print_messages,
            #     config={"callback": None}
            # )

            user_proxy = TrackableUserProxyAgent(
                name="User",
                human_input_mode="NEVER",
                is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
                code_execution_config=False,
            )
            # user_proxy.register_reply(
            #     trigger=[autogen.Agent, None],
            #     reply_func=print_messages,
            #     config={"callback": None}
            # )

            user_proxy.initiate_chats(
                [
                    {
                        "chat_id": 0,
                        "recipient": writer,
                        "message": create_writer_task(overview, title, check_messages[title]['subjects'], check_messages[title]['appendix']),
                        "clear_history": True,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    },
                    {
                        "chat_id": 1,
                        "recipient": reviewer,
                        "message": create_reviewer_task(overview, title, check_messages[title]['subjects'], check_messages[title]['appendix']),
                        "clear_history": False,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    },
                    {
                        "chat_id": 2,
                        "recipient": writer,
                        "message": '最終版として要件定義書を作成してください。',
                        "clear_history": False,
                        "silent": False,
                        "max_turns": 1,
                        "summary_method": "last_msg"
                    }
                ]
            )

    # チャットメッセージを表示
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])