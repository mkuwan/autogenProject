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


# チャットメッセージを表示
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


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
        with st.chat_message(sender.name):
            st.markdown(message)
        st.session_state.messages.append({"role": sender.name, "content": message})
        return super()._process_received_message(message, sender, silent)


# 要件定義書の作成項目をJSONファイルから読み込んで表示させます
# JSONファイルを読み込んで使用しているので、各項目の表示名等を変更する場合はJSONファイルを変更してください
# 各項目のチェックボックスに表示されるものは、最大で9つまで表示されます
# 抽象化しているため、項目数が変わっても自動的に対応しますが、直接コードに設定するのもありかもです
# とりあえず、件数としては最大14, 各項目の最大件数は9としています
with st.container():
    st.markdown('### 要件定義作成')
    # requirement_document_itemsからtitleとitemsを取得
    summary = st.text_area("要件定義概要")
    for item in requirement_document_items:
        title = item.get('title')
        st.markdown(f"**{title}**")

        title_index = item.get('title_index')
        if title_index == "01":
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




    if check0101 and subject0101:
        st.write(f"col0101: {subject0101}")
    if check0102 and subject0102:
        st.write(f"col0102: {subject0102}")
    if check0103 and subject0103:
        st.write(f"col0103: {subject0103}")
    if check0104 and subject0104:
        st.write(f"col0104: {subject0104}")
    if check0105 and subject0105:
        st.write(f"col0105: {subject0105}")
    if check0106 and subject0106:
        st.write(f"col0106: {subject0106}")
    if check0107 and subject0107:
        st.write(f"col0107: {subject0107}")
    if check0108 and subject0108:
        st.write(f"col0108: {subject0108}")
    if check0109 and subject0109:
        st.write(f"col0109: {subject0109}")
    if appendix01:
        st.write(f"appendix01: {appendix01}")

    if check0201 and subject0201:
        st.write(f"col0201: {subject0201}")
    if check0202 and subject0202:
        st.write(f"col0202: {subject0202}")
    if check0203 and subject0203:
        st.write(f"col0203: {subject0203}")
    if check0204 and subject0204:
        st.write(f"col0204: {subject0204}")
    if check0205 and subject0205:
        st.write(f"col0205: {subject0205}")
    if check0206 and subject0206:
        st.write(f"col0206: {subject0206}")
    if check0207 and subject0207:
        st.write(f"col0207: {subject0207}")
    if check0208 and subject0208:
        st.write(f"col0208: {subject0208}")
    if check0209 and subject0209:
        st.write(f"col0209: {subject0209}")
    if appendix02:
        st.write(f"appendix02: {appendix02}")

    if check0301 and subject0301:
        st.write(f"col0301: {subject0301}")
    if check0302 and subject0302:
        st.write(f"col0302: {subject0302}")
    if check0303 and subject0303:
        st.write(f"col0303: {subject0303}")
    if check0304 and subject0304:
        st.write(f"col0304: {subject0304}")
    if check0305 and subject0305:
        st.write(f"col0305: {subject0305}")
    if check0306 and subject0306:
        st.write(f"col0306: {subject0306}")
    if check0307 and subject0307:
        st.write(f"col0307: {subject0307}")
    if check0308 and subject0308:
        st.write(f"col0308: {subject0308}")
    if check0309 and subject0309:
        st.write(f"col0309: {subject0309}")
    if appendix03:
        st.write(f"appendix03: {appendix03}")

    if check0401 and subject0401:
        st.write(f"col0401: {subject0401}")
    if check0402 and subject0402:
        st.write(f"col0402: {subject0402}")
    if check0403 and subject0403:
        st.write(f"col0403: {subject0403}")
    if check0404 and subject0404:
        st.write(f"col0404: {subject0404}")
    if check0405 and subject0405:
        st.write(f"col0405: {subject0405}")
    if check0406 and subject0406:
        st.write(f"col0406: {subject0406}")
    if check0407 and subject0407:
        st.write(f"col0407: {subject0407}")
    if check0408 and subject0408:
        st.write(f"col0408: {subject0408}")
    if check0409 and subject0409:
        st.write(f"col0409: {subject0409}")
    if appendix04:
        st.write(f"appendix04: {appendix04}")

    if check0501 and subject0501:
        st.write(f"col0501: {subject0501}")
    if check0502 and subject0502:
        st.write(f"col0502: {subject0502}")
    if check0503 and subject0503:
        st.write(f"col0503: {subject0503}")
    if check0504 and subject0504:
        st.write(f"col0504: {subject0504}")
    if check0505 and subject0505:
        st.write(f"col0505: {subject0505}")
    if check0506 and subject0506:
        st.write(f"col0506: {subject0506}")
    if check0507 and subject0507:
        st.write(f"col0507: {subject0507}")
    if check0508 and subject0508:
        st.write(f"col0508: {subject0508}")
    if check0509 and subject0509:
        st.write(f"col0509: {subject0509}")
    if appendix05:
        st.write(f"appendix05: {appendix05}")

    if check0601 and subject0601:
        st.write(f"col0601: {subject0601}")
    if check0602 and subject0602:
        st.write(f"col0602: {subject0602}")
    if check0603 and subject0603:
        st.write(f"col0603: {subject0603}")
    if check0604 and subject0604:
        st.write(f"col0604: {subject0604}")
    if check0605 and subject0605:
        st.write(f"col0605: {subject0605}")
    if check0606 and subject0606:
        st.write(f"col0606: {subject0606}")
    if check0607 and subject0607:
        st.write(f"col0607: {subject0607}")
    if check0608 and subject0608:
        st.write(f"col0608: {subject0608}")
    if check0609 and subject0609:
        st.write(f"col0609: {subject0609}")
    if appendix06:
        st.write(f"appendix06: {appendix06}")

    if check0701 and subject0701:
        st.write(f"col0701: {subject0701}")
    if check0702 and subject0702:
        st.write(f"col0702: {subject0702}")
    if check0703 and subject0703:
        st.write(f"col0703: {subject0703}")
    if check0704 and subject0704:
        st.write(f"col0704: {subject0704}")
    if check0705 and subject0705:
        st.write(f"col0705: {subject0705}")
    if check0706 and subject0706:
        st.write(f"col0706: {subject0706}")
    if check0707 and subject0707:
        st.write(f"col0707: {subject0707}")
    if check0708 and subject0708:
        st.write(f"col0708: {subject0708}")
    if check0709 and subject0709:
        st.write(f"col0709: {subject0709}")
    if appendix07:
        st.write(f"appendix07: {appendix07}")

    if check0801 and subject0801:
        st.write(f"col0801: {subject0801}")
    if check0802 and subject0802:
        st.write(f"col0802: {subject0802}")
    if check0803 and subject0803:
        st.write(f"col0803: {subject0803}")
    if check0804 and subject0804:
        st.write(f"col0804: {subject0804}")
    if check0805 and subject0805:
        st.write(f"col0805: {subject0805}")
    if check0806 and subject0806:
        st.write(f"col0806: {subject0806}")
    if check0807 and subject0807:
        st.write(f"col0807: {subject0807}")
    if check0808 and subject0808:
        st.write(f"col0808: {subject0808}")
    if check0809 and subject0809:
        st.write(f"col0809: {subject0809}")
    if appendix08:
        st.write(f"appendix08: {appendix08}")

    if check0901 and subject0901:
        st.write(f"col0901: {subject0901}")
    if check0902 and subject0902:
        st.write(f"col0902: {subject0902}")
    if check0903 and subject0903:
        st.write(f"col0903: {subject0903}")
    if check0904 and subject0904:
        st.write(f"col0904: {subject0904}")
    if check0905 and subject0905:
        st.write(f"col0905: {subject0905}")
    if check0906 and subject0906:
        st.write(f"col0906: {subject0906}")
    if check0907 and subject0907:
        st.write(f"col0907: {subject0907}")
    if check0908 and subject0908:
        st.write(f"col0908: {subject0908}")
    if check0909 and subject0909:
        st.write(f"col0909: {subject0909}")
    if appendix09:
        st.write(f"appendix09: {appendix09}")

    if check1001 and subject1001:
        st.write(f"col1001: {subject1001}")
    if check1002 and subject1002:
        st.write(f"col1002: {subject1002}")
    if check1003 and subject1003:
        st.write(f"col1003: {subject1003}")
    if check1004 and subject1004:
        st.write(f"col1004: {subject1004}")
    if check1005 and subject1005:
        st.write(f"col1005: {subject1005}")
    if check1006 and subject1006:
        st.write(f"col1006: {subject1006}")
    if check1007 and subject1007:
        st.write(f"col1007: {subject1007}")
    if check1008 and subject1008:
        st.write(f"col1008: {subject1008}")
    if check1009 and subject1009:
        st.write(f"col1009: {subject1009}")
    if appendix10:
        st.write(f"appendix10: {appendix10}")

    if check1101 and subject1101:
        st.write(f"col1101: {subject1101}")
    if check1102 and subject1102:
        st.write(f"col1102: {subject1102}")
    if check1103 and subject1103:
        st.write(f"col1103: {subject1103}")
    if check1104 and subject1104:
        st.write(f"col1104: {subject1104}")
    if check1105 and subject1105:
        st.write(f"col1105: {subject1105}")
    if check1106 and subject1106:
        st.write(f"col1106: {subject1106}")
    if check1107 and subject1107:
        st.write(f"col1107: {subject1107}")
    if check1108 and subject1108:
        st.write(f"col1108: {subject1108}")
    if check1109 and subject1109:
        st.write(f"col1109: {subject1109}")
    if appendix11:
        st.write(f"appendix11: {appendix11}")

    if check1201 and subject1201:
        st.write(f"col1201: {subject1201}")
    if check1202 and subject1202:
        st.write(f"col1202: {subject1202}")
    if check1203 and subject1203:
        st.write(f"col1203: {subject1203}")
    if check1204 and subject1204:
        st.write(f"col1204: {subject1204}")
    if check1205 and subject1205:
        st.write(f"col1205: {subject1205}")
    if check1206 and subject1206:
        st.write(f"col1206: {subject1206}")
    if check1207 and subject1207:
        st.write(f"col1207: {subject1207}")
    if check1208 and subject1208:
        st.write(f"col1208: {subject1208}")
    if check1209 and subject1209:
        st.write(f"col1209: {subject1209}")
    if appendix12:
        st.write(f"appendix12: {appendix12}")

    if check1301 and subject1301:
        st.write(f"col1301: {subject1301}")
    if check1302 and subject1302:
        st.write(f"col1302: {subject1302}")
    if check1303 and subject1303:
        st.write(f"col1303: {subject1303}")
    if check1304 and subject1304:
        st.write(f"col1304: {subject1304}")
    if check1305 and subject1305:
        st.write(f"col1305: {subject1305}")
    if check1306 and subject1306:
        st.write(f"col1306: {subject1306}")
    if check1307 and subject1307:
        st.write(f"col1307: {subject1307}")
    if check1308 and subject1308:
        st.write(f"col1308: {subject1308}")
    if check1309 and subject1309:
        st.write(f"col1309: {subject1309}")
    if appendix13:
        st.write(f"appendix13: {appendix13}")

    if check1401 and subject1401:
        st.write(f"col1401: {subject1401}")
    if check1402 and subject1402:
        st.write(f"col1402: {subject1402}")
    if check1403 and subject1403:
        st.write(f"col1403: {subject1403}")
    if check1404 and subject1404:
        st.write(f"col1404: {subject1404}")
    if check1405 and subject1405:
        st.write(f"col1405: {subject1405}")
    if check1406 and subject1406:
        st.write(f"col1406: {subject1406}")
    if check1407 and subject1407:
        st.write(f"col1407: {subject1407}")
    if check1408 and subject1408:
        st.write(f"col1408: {subject1408}")
    if check1409 and subject1409:
        st.write(f"col1409: {subject1409}")
    if appendix14:
        st.write(f"appendix14: {appendix14}")

    if appendix_other:
        st.write(f"appendix_other: {appendix_other}")




