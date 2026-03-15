#!/usr/bin/env python3
import torch
import torch.nn as nn


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("GPU is not available to torch")

    print(f"torch={torch.__version__}")
    print(f"torch.version.hip={torch.version.hip}")
    assert torch.version.hip is not None, "This example expects PyTorch built for ROCm"

    # PyTorch on ROCm still uses the "cuda" device string for compatibility.
    device = torch.device("cuda")
    print(f"device={device} ({torch.cuda.get_device_name(0)})")

    model = nn.Linear(3, 1).to(device)
    with torch.no_grad():
        model.weight[:] = torch.tensor([[0.1, 0.2, 0.3]], device=device)
        model.bias[:] = torch.tensor([0.5], device=device)

    model.eval()
    print("model.training:", model.training)
    x = torch.tensor([[1.0, 2.0, 3.0]], device=device)

    w_before = model.weight.detach().clone()
    with torch.no_grad():
        pred = model(x)
    w_after = model.weight.detach().clone()

    print("input:", x.cpu())
    print("prediction:", pred.cpu())
    print("prediction requires_grad:", pred.requires_grad)
    print("weight changed:", not torch.allclose(w_before, w_after))


if __name__ == "__main__":
    main()
