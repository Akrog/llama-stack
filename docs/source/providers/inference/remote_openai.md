# remote::openai

## Description

OpenAI inference provider for accessing GPT models and other OpenAI services.

## Configuration

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `api_key` | `str \| None` | No |  | API key for OpenAI models |
| `base_url` | `<class 'str'>` | No | https://api.openai.com/v1 | Base URL for OpenAI API |
| `allowed_models` | `list[str` | No | [] | List of model names to expose from all the available ones. Defaults to all (empty list). |
| `embeddings_metadata` | `dict[str, remote.inference.openai.config.EmbeddingMetadata \| None` | No |  | Mapping of embedding models to their metadata. Defaults to OpenAI's values |

## Sample Configuration

```yaml
api_key: ${env.OPENAI_API_KEY:=}
base_url: ${env.OPENAI_BASE_URL:=https://api.openai.com/v1}
allowed_models:
- gpt-3.5-turbo-0125
- gpt-3.5-turbo
- gpt-3.5-turbo-instruct
- gpt-4
- gpt-4-turbo
- gpt-4o
- gpt-4o-2024-08-06
- gpt-4o-mini
- gpt-4o-audio-preview
- chatgpt-4o-latest
- o1
- o1-mini
- o3-mini
- o4-mini
- text-embedding-3-small
- text-embedding-3-large
embeddings_metadata:
  text-embedding-3-small:
    embedding_dimension: 1536
    context_length: 8192
  text-embedding-3-large:
    embedding_dimension: 3072
    context_length: 8192

```

