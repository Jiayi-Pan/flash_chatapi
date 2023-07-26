# Flash Chat API 
This package provides a simple but high-throughput interface for ChatGPT API.

## Key Features
- **Parallel, async execution**: Maximize utilization with parallel async API calls, while maintaining compliance with API rate limits.
- **Automatic retries**: Resilient handling of rate limit or network-related failures through automatic retries.
- **API key pool support**: Increase throughput by iterating multiple API keys.

## Installation
```bash
pip install flash-chatgpt-api
pip install git+https://github.com/Jiayi-Pan/flash_chatapi.git
```

## Example
```python
from flash_chatapi import generate_from_openai_chat_completion

chats = [
    [{"role": "user", "content": "Say hi"},],
    [{"role": "user", "content": "说你好"},]
]

# if api_keys is None, we will use the OPENAI_API_KEY environment variable
api_keys = ['key1', 'key2', 'key3']

responses = asyncio.run(generate_from_openai_chat_completion(
    chats=chats,
    model="gpt-3.5-turbo",
    api_keys=api_keys,
))
```

## Acknowledgements
This implementation is built on top of the awesome implementation from [Zeno](https://github.com/zeno-ml/zeno-build/blob/main/zeno_build/models/providers/openai_utils.py).


## License
MIT License.
