from typing import List, Optional

from pydantic import BaseModel


class ArchitectureSchema(BaseModel):
    modality: str
    input_modalities: List[str]
    output_modalities: List[str]
    tokenizer: str
    instruct_type: Optional[str]


class PricingSchema(BaseModel):
    prompt: str
    completion: str
    request: str
    image: str
    web_search: str
    internal_reasoning: str


class TopProviderSchema(BaseModel):
    context_length: int
    max_completion_tokens: Optional[int]
    is_moderated: bool


class ModelSchema(BaseModel):
    id: str
    canonical_slug: str
    hugging_face_id: str
    name: str
    created: int
    description: str
    context_length: int
    architecture: ArchitectureSchema
    pricing: PricingSchema
    top_provider: TopProviderSchema
    per_request_limits: Optional[dict]
    supported_parameters: List[str]


class ModelShortSchema(BaseModel):
    id: str
    name: str
    description: str
