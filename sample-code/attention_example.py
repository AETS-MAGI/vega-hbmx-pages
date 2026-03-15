#!/usr/bin/env python3
import math

import torch
import torch.nn as nn
import torch.nn.functional as F


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("GPU is not available to torch")

    device = torch.device("cuda")
    print(f"torch={torch.__version__}")
    print(f"torch.version.hip={torch.version.hip}")
    print(f"device={torch.cuda.get_device_name(0)}")

    x = torch.tensor(
        [
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 0.0],
        ],
        device=device,
    )

    q = k = v = x
    scores = torch.matmul(q, k.T) / math.sqrt(q.size(-1))
    weights = F.softmax(scores, dim=-1)
    out = torch.matmul(weights, v)

    mha = nn.MultiheadAttention(embed_dim=4, num_heads=1, batch_first=True).to(device)
    with torch.no_grad():
        out2, attn = mha(x.unsqueeze(0), x.unsqueeze(0), x.unsqueeze(0))

    print("manual output shape:", tuple(out.shape))
    print("mha output shape:", tuple(out2.shape))
    print("mha attention shape:", tuple(attn.shape))


if __name__ == "__main__":
    main()
