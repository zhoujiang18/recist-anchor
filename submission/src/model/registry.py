from functools import partial

from src.model.build_medai_model import build_medai_model
from src.model.modeling.position_encoder3D import LieRE, PositionEmbeddingRandom3D, RoPEMixed

model_registry = {
    "medai_model_sinusoidal": partial(build_medai_model, PositionEmbeddingRandom3D),
    "medai_model_rope_mixed": partial(build_medai_model, RoPEMixed),
    "medai_model_rope_mixed_large": partial(build_medai_model, RoPEMixed, large=True),
    "medai_model_liere": partial(build_medai_model, LieRE),
    "medai_model_liere_large": partial(build_medai_model, LieRE, large=True),
}
