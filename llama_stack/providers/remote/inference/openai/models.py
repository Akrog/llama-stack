# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import logging

from llama_stack.apis.models import ModelType
from llama_stack.providers.utils.inference.model_registry import (
    ProviderModelEntry,
)

from .config import EmbeddingMetadata

logger = logging.getLogger(__name__)

LLM_MODEL_IDS = [
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-instruct",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-2024-08-06",
    "gpt-4o-mini",
    "gpt-4o-audio-preview",
    "chatgpt-4o-latest",
    "o1",
    "o1-mini",
    "o3-mini",
    "o4-mini",
    "text-embedding-3-small",
    "text-embedding-3-large",
]

EMBEDDING_MODEL_IDS: dict[str, EmbeddingMetadata] = {
    "text-embedding-3-small": EmbeddingMetadata(embedding_dimension=1536, context_length=8192),
    "text-embedding-3-large": EmbeddingMetadata(embedding_dimension=3072, context_length=8192),
}

MODEL_ENTRIES = [ProviderModelEntry(provider_model_id=m) for m in LLM_MODEL_IDS] + [
    ProviderModelEntry(
        provider_model_id=model_id,
        model_type=ModelType.embedding,
        metadata={
            "embedding_dimension": model_info.embedding_dimension,
            "context_length": model_info.context_length,
        },
    )
    for model_id, model_info in EMBEDDING_MODEL_IDS.items()
]


def get_model_entries(
    allowed: list[str] | None, embeddings: dict[str, EmbeddingMetadata] | None
) -> list[ProviderModelEntry]:
    """Get model entries to expose.

    Given a list of allowed model names and a mapping of embedding model names
    to their metadata, returns a list of ProviderModelEntry meant for the
    ModelRegistryHelper.

    All models are returned when allowed is an empty list or None.

    When no embeddings metadata is provided the default values for OpenAI are
    used.
    """
    allowed = allowed or LLM_MODEL_IDS
    if embeddings is None:
        embeddings = EMBEDDING_MODEL_IDS

    res = []
    for model in allowed:
        metadata = embeddings.get(model)
        if metadata:
            res.append(
                ProviderModelEntry(
                    provider_model_id=model,
                    model_type=ModelType.embedding,
                    metadata=dict(metadata),
                )
            )
        else:
            res.append(ProviderModelEntry(provider_model_id=model))

    missing_embeddings = set(embeddings.keys()).difference(allowed)
    if missing_embeddings:
        logger.warning("Embedding metadata provided for unknown models: %s.", ", ".join(missing_embeddings))

    return res
