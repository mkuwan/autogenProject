## Autogen Project
This project is a simple example of how to use the autogen library to generate code.

## Ollamaを使用した場合の設定方法
https://ollama.com/blog/openai-compatibility
config_list = [
  {
    "model": "codellama",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
  }
]

                      

## 終了トリガー
エージェントのパラメータを設定して会話を終了する方法です。
設定できるパラメータは以下２つ。 
- max_consecutive_auto_reply  
  - 同じ宛先エージェントへの連続応答の数が閾値を超えた場合に終了する。
- is_termination_msg 
  - 受信したメッセージが "TERMINATE" などの特定の条件を満たす場合に、終了する。
  ConversableAgentクラスのコンストラクタの引数is_termination_msgを使用して、この条件をカスタマイズ可能。