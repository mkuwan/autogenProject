import autogen

def main():
    config_list = autogen.config_list_from_json(
        env_or_file="../LLM_CONFIG_LIST.json",
    )

    filter_codellama = {"model": ["codellama"]}
    filter_codegemma = {"model": ["codegemma"]}
    filter_llama31 = {"model": ["llama3.1"]}
    filter_mistral = {"model": ["mistral"]}
    filter_mistral_nemo = {"model": ["mistral-nemo-instruct-2407"]}

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={
            "config_list": autogen.filter_config(config_list, filter_mistral_nemo),
            "temperature": 0,
            "price": [0, 0],
        },
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        },
        max_consecutive_auto_reply=10,
    )

    user_proxy.initiate_chat(
        assistant,
        message="Plot a chart of META and TESLA stock price change.",
    )

if __name__ == "__main__":
    main()