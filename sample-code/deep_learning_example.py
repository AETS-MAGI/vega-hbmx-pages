#!/usr/bin/env python3
import torch
import torch.nn as nn


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("GPU is not available to torch")

    device = torch.device("cuda")
    print(f"torch={torch.__version__}")
    print(f"torch.version.hip={torch.version.hip}")
    print(f"device={torch.cuda.get_device_name(0)}")

    model = nn.Sequential(
        nn.Conv2d(1, 1, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(16, 2),
    ).to(device)

    x = torch.randn(1, 1, 4, 4, device=device)
    y = model(x)

    print("input shape:", tuple(x.shape))
    print("output shape:", tuple(y.shape))
    print(model)


if __name__ == "__main__":
    main()
