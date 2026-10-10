"""Download the pinned upstream model assets (requires Git)."""
from pathlib import Path
import subprocess

COMMIT = "0059d4335f8156206f63a35662313385f7ad6d74"
URL = "https://github.com/google-deepmind/mujoco_menagerie.git"
destination = Path(__file__).resolve().parent / "mujoco_menagerie"

if destination.exists():
    head = subprocess.check_output(
        ["git", "-C", str(destination), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != COMMIT:
        raise SystemExit("Existing model checkout differs from pinned version; keep it and choose another project directory.")
    for asset_dir in ("franka_fr3", "franka_emika_panda"):
        if not (destination / asset_dir / "assets").is_dir():
            raise SystemExit("Existing checkout is missing model assets.")
    print("Pinned model assets already present.")
else:
    subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout", URL, str(destination)], check=True)
    subprocess.run(["git", "-C", str(destination), "sparse-checkout", "set", "franka_fr3", "franka_emika_panda"], check=True)
    subprocess.run(["git", "-C", str(destination), "checkout", "--detach", COMMIT], check=True)
    print("Model assets ready.")
