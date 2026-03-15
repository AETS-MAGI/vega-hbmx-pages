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

    model = nn.Linear(3, 1).to(device)
    x = torch.tensor([[1.0, 2.0, 3.0]], device=device)
    target = torch.tensor([[7.0]], device=device)

    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    w_before = model.weight.detach().clone()
    pred = model(x)
    loss = loss_fn(pred, target)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    w_after = model.weight.detach().clone()

    print("loss:", float(loss.item()))
    print("weight changed:", not torch.allclose(w_before, w_after))
    print("weight before:", w_before.cpu())
    print("weight after:", w_after.cpu())


if __name__ == "__main__":
    main()
