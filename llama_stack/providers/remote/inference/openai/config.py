# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any

from pydantic import BaseModel, Field

from llama_stack.schema_utils import json_schema_type


class OpenAIProviderDataValidator(BaseModel):
    openai_api_key: str | None = Field(
        default=None,
        description="API key for OpenAI models",
    )


class EmbeddingMetadata(BaseModel):
    embedding_dimension: int = Field(description="The dimensionality of the embeddings.")
    context_length: int = Field(description="The maximum sequence length that the model can handle.")


@json_schema_type
class OpenAIConfig(BaseModel):
    api_key: str | None = Field(
        default=None,
        description="API key for OpenAI models",
    )
    base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for OpenAI API",
    )
    allowed_models: list[str] = Field(
        default_factory=list,
        description="List of model names to expose from all the available ones in the server. Defaults to all (empty list).",
    )
    embeddings_metadata: dict[str, EmbeddingMetadata] | None = Field(
        default=None,
        description="Mapping of embedding models to their metadata. Defaults to OpenAI's values",
    )
    extra_completion_params: dict[str, Any] = Field(
        default_factory=dict,
        description="Extra parameters to pass to litellm's completion. For example drop_params or allowed_openai_params",
    )

    @classmethod
    def sample_run_config(
        cls,
        api_key: str = "${env.OPENAI_API_KEY:=}",
        base_url: str = "${env.OPENAI_BASE_URL:=https://api.openai.com/v1}",
        allowed_models: list[str] = None,
        embeddings_metadata: dict[str, EmbeddingMetadata] | None = None,
        extra_completion_params: dict[str, Any] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        # Import here to avoid circular references
        from .models import EMBEDDING_MODEL_IDS, LLM_MODEL_IDS

        allowed_models = allowed_models or LLM_MODEL_IDS
        embeddings_metadata = embeddings_metadata or EMBEDDING_MODEL_IDS
        extra_completion_params = extra_completion_params or {}

        return {
            "api_key": api_key,
            "base_url": base_url,
            "allowed_models": allowed_models,
            "embeddings_metadata": embeddings_metadata,
            "extra_completion_params": extra_completion_params,
        }
