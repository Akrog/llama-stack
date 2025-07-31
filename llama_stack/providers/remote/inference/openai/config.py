# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any

from pydantic import BaseModel, Field

from llama_stack.schema_utils import json_schema_type

from .models import get_model_entries


class OpenAIProviderDataValidator(BaseModel):
    openai_api_key: str | None = Field(
        default=None,
        description="API key for OpenAI models",
    )


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
        description="List of model names to expose from all the available ones. Defaults to all (empty list).",
    )

    @classmethod
    def sample_run_config(
        cls,
        api_key: str = "${env.OPENAI_API_KEY:=}",
        base_url: str = "${env.OPENAI_BASE_URL:=https://api.openai.com/v1}",
        allowed_models: list[str] = None,
        **kwargs,
    ) -> dict[str, Any]:
        if not allowed_models:
            models = get_model_entries(None)
            allowed_models = [m.provider_model_id for m in models]

        return {
            "api_key": api_key,
            "base_url": base_url,
            "allowed_models": allowed_models,
        }
