from langchain.llms.base import LLM
from langchain.schema import Generation, LLMResult
from pydantic import PrivateAttr
from typing import Optional, List, Any
from huggingface_hub import InferenceClient
import os

class HFClientLLM(LLM):
    model: str = "HuggingFaceH4/zephyr-7b-beta"
    max_new_tokens: int = 512
    temperature: float = 0.7

    _client: InferenceClient = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = InferenceClient(model=self.model, token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

    @property
    def _llm_type(self) -> str:
        return "hf_inference_client"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.text_generation(
            prompt=prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            stop_sequences=stop or []
        )
        return response
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
    ) -> LLMResult:
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop=stop)
            generations.append([Generation(text=text)])
        return LLMResult(generations=generations)