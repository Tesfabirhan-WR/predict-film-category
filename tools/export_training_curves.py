"""Export the TensorBoard curves of the final model to a static image served by the API.

Usage:
    python tools/export_training_curves.py notebook/my_log_dir/<session-folder>
    python tools/export_training_curves.py notebook/my_log_dir/<session-folder>/final_model   # also accepted
    python tools/export_training_curves.py notebook/my_log_dir/<session-folder> --list       # only print what the logs contain
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from tensorboard.util import tensor_util

OUT = "src/static/training_curves.png"


def load(run_dir):
    """Return the accumulator of a run folder, or None if it holds no event file."""
    if not run_dir.is_dir() or not any(run_dir.glob("events.out.tfevents.*")):
        return None
    # 0 = keep every point. Keras 3 / TF2 write scalars as "tensors", old code as "scalars": read both.
    acc = EventAccumulator(str(run_dir), size_guidance={"scalars": 0, "tensors": 0})
    acc.Reload()
    return acc


def all_tags(acc):
    tags = acc.Tags()
    return sorted(set(tags["scalars"]) | set(tags["tensors"]))


def points(acc, tag):
    """List of (epoch, value) for one tag, from scalar events or tensor events."""
    if tag in acc.Tags()["scalars"]:
        return [(e.step, e.value) for e in acc.Scalars(tag)]
    return [(e.step, float(tensor_util.make_ndarray(e.tensor_proto))) for e in acc.Tensors(tag)]


def pick_tag(tags, name):
    """Find the tag for 'loss' or 'accuracy' whatever the Keras version calls it."""
    for candidate in (f"epoch_{name}", name):
        if candidate in tags:
            return candidate
    matches = sorted((t for t in tags if name in t and "learning_rate" not in t), key=len)
    return matches[0] if matches else None


def main(log_dir, list_only=False):
    base = Path(log_dir)
    # Accept the session folder (.../20261028-110802) or the run folder itself (.../final_model)
    run = base if (base / "train").is_dir() else base / "final_model"
    accs = {split: load(run / split) for split in ("train", "validation")}

    print(f"Run folder: {run}  (exists: {run.is_dir()})")
    for split, acc in accs.items():
        print(f"  {split}: " + ("no event file found" if acc is None else f"tags = {all_tags(acc)}"))
    if list_only:
        return

    available = {s: a for s, a in accs.items() if a is not None}
    if not available:
        sys.exit("No TensorBoard events found. Check the session folder: it must contain final_model/train/.")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    drawn = 0
    for ax, name, title in zip(axes, ("loss", "accuracy"), ("Loss", "Accuracy")):
        for split, acc in available.items():
            tag = pick_tag(all_tags(acc), name)
            if tag is None:
                continue
            pts = points(acc, tag)
            ax.plot([s for s, _ in pts], [v for _, v in pts], label=split)
            drawn += 1
        ax.set_title(title)
        ax.set_xlabel("epoch")
        if ax.get_legend_handles_labels()[0]:
            ax.legend()
    if drawn == 0:
        sys.exit("No loss or accuracy tag found: run the script again with --list and check the tag names.")

    fig.tight_layout()
    fig.savefig(OUT, dpi=110)
    print("saved", OUT)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], list_only="--list" in sys.argv)
