from PIL import Image
from pathlib import Path
import click


def render_samples(image, outdir="samples", low=20, high=220, n=10):
    im = Image.open(image)
    stem = Path(image).stem
    step = (high - low) / (n - 1)
    thresholds = [int(low + step * x) for x in range(n)]
    for thresh in thresholds:
        to_binary = lambda x: 255 if x > thresh else 0
        r = im.convert("L").point(to_binary, mode="1")
        p = Path(outdir / "{}_{}.png".format(stem, str(thresh).zfill(3)))
        r.save(p)

@click.group()
def cli():
    pass


@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.argument("outdir", type=click.Path())
@click.option("--low", default=20)
@click.option("--high", default=220)
@click.option("-n", default=6)
def render(image, outdir, low, high, n):
    outdir = Path(outdir)
    Path.mkdir(outdir, exist_ok=True)
    render_samples(image, outdir, low, high, n)
    print("Saved {} files to {}.".format(n, outdir))


@click.command()
@click.argument("keeper", type=click.Path(exists=True))
def keeponly(keeper):
    keeper = Path(keeper)
    parent = keeper.parent
    basename = keeper.stem[0:-4]
    candidates = [f for f in list(parent.glob("*.png")) if basename in str(f)]
    candidates.remove(keeper)
    n = len(candidates)
    for image in candidates:
        Path.unlink(image)
    print("Removed {} files in {}".format(n, parent))


cli.add_command(render)
cli.add_command(keeponly)

if __name__ == "__main__":
    cli()
