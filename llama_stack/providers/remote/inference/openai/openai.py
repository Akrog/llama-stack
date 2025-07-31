# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import logging

from llama_stack.providers.utils.inference.litellm_openai_mixin import LiteLLMOpenAIMixin
from llama_stack.providers.utils.inference.openai_mixin import OpenAIMixin

from .config import OpenAIConfig
from .models import get_model_entries

logger = logging.getLogger(__name__)


#
# This OpenAI adapter implements Inference methods using two mixins -
#
# | Inference Method           | Implementation Source    |
# |----------------------------|--------------------------|
# | completion                 | LiteLLMOpenAIMixin       |
# | chat_completion            | LiteLLMOpenAIMixin       |
# | embedding                  | LiteLLMOpenAIMixin       |
# | batch_completion           | LiteLLMOpenAIMixin       |
# | batch_chat_completion      | LiteLLMOpenAIMixin       |
# | openai_completion          | OpenAIMixin              |
# | openai_chat_completion     | OpenAIMixin              |
# | openai_embeddings          | OpenAIMixin              |
#
class OpenAIInferenceAdapter(OpenAIMixin, LiteLLMOpenAIMixin):
    """
    OpenAI Inference Adapter for Llama Stack.

    Note: The inheritance order is important here. OpenAIMixin must come before
    LiteLLMOpenAIMixin to ensure that OpenAIMixin.check_model_availability()
    is used instead of ModelRegistryHelper.check_model_availability().

    - OpenAIMixin.check_model_availability() queries the OpenAI API to check if a model exists
    - ModelRegistryHelper.check_model_availability() (inherited by LiteLLMOpenAIMixin) just returns False and shows a warning
    """

    def __init__(self, config: OpenAIConfig) -> None:
        model_entries = get_model_entries(config.allowed_models, config.embeddings_metadata)
        LiteLLMOpenAIMixin.__init__(
            self,
            model_entries,
            litellm_provider_name="openai",
            api_key_from_config=config.api_key,
            provider_data_api_key_field="openai_api_key",
            openai_compat_api_base=config.base_url,
        )
        self.config = config

    # Delegate the client data handling get_api_key method to LiteLLMOpenAIMixin
    get_api_key = LiteLLMOpenAIMixin.get_api_key

    def get_base_url(self) -> str:
        """
        Get the OpenAI API base URL.

        Returns the OpenAI API base URL from the configuration.
        """
        return self.config.base_url

    async def initialize(self) -> None:
        await super().initialize()

    async def shutdown(self) -> None:
        await super().shutdown()
