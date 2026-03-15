#!/usr/bin/env python3
import torch


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("GPU is not available to torch")

    device = torch.device("cuda")
    print(f"torch={torch.__version__}")
    print(f"torch.version.hip={torch.version.hip}")
    print(f"device={torch.cuda.get_device_name(0)}")

    a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], device=device)
    b = torch.tensor([[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]], device=device)
    c = torch.matmul(a, b)

    print("A shape:", tuple(a.shape))
    print("B shape:", tuple(b.shape))
    print("C shape:", tuple(c.shape))
    print("C:")
    print(c.cpu())


if __name__ == "__main__":
    main()
