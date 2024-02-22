completion = {
  "id": "chatcmpl-8vBFFnQ8iB0NOCrHgzYUPz8obc6Of",
  "object": "chat.completion",
  "created": 1708638613,
  "model": "gpt-3.5-turbo-0125",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "SELECT Name FROM table_df WHERE Industry = 'Healthcare'"
      },
      "logprobs": 'null',
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 308,
    "completion_tokens": 12,
    "total_tokens": 320
  },
  "system_fingerprint": "fp_cbdb91ce3f"
}

print(completion['choices'][0]['message']['content'])