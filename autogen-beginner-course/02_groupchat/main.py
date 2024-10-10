import autogen
import pprint

def main():
    config_list = autogen.config_list_from_json(
        env_or_file="../LLM_CONFIG_LIST.json",
    )

    filter_codellama = {"model": ["codellama"]}
    filter_codegemma = {"model": ["codegemma"]}
    filter_llama31 = {"model": ["llama3.1"]}
    filter_mistral = {"model": ["mistral"]}

    llm_config = {
        "cache_seed": 43,  # change the cache_seed for different trials. if set None, it will be random?
        "temperature": 0,
        "config_list": autogen.filter_config(config_list, filter_codegemma),
        "timeout": 240,  # in seconds
        "price": [0, 0],
    }

    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        human_input_mode="TERMINATE",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        },
        # max_consecutive_auto_reply=10,
        system_message="A human admin. Interact with the planner to discuss the plan. "
                        "Plan execution needs to be approved by this admin.",
    )

    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=llm_config,
        system_message="""Engineer. You follow an approved plan. Make sure you save code to disk.  You write python/shell 
        code to solve tasks. Wrap the code in a code block that specifies the script type and the name of the file to 
        save to disk.""",
    )
    scientist = autogen.AssistantAgent(
        name="Scientist",
        llm_config=llm_config,
        system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their 
        abstracts printed. You don't write code.""",
    )
    planner = autogen.AssistantAgent(
        name="Planner",
        system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """,
        llm_config=llm_config,
    )

    critic = autogen.AssistantAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the "
                       "plan includes adding verifiable info such as source URL.",
        llm_config=llm_config,
    )


    group_chat = autogen.GroupChat(
        agents=[user_proxy, engineer, scientist, planner, critic],
        messages=[],
        max_round=12
    )

    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )

    chat_result = user_proxy.initiate_chat(
        manager,
        message="""
    Find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.
    """,
        summary_method="reflection_with_llm",
        max_turns=4
    )

    print("Summary:")
    print(chat_result.summary)
    print()

    print("Chat history:")
    for item in chat_result.chat_history:
        # item['content']に文字がある場合は出力する
        if item['content']:
            print(f"Name: {item['name']}, Content: {item['content']}")

    print("Cost:")
    pprint.pprint(chat_result.cost)

if __name__ == "__main__":
    main()
