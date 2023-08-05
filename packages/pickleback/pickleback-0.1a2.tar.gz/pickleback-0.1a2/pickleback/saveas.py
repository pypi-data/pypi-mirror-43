"""A utility script to help saving matplotlib pickles as other formats"""

import argparse
import pickle
import os

from matplotlib.backend_bases import get_registered_canvas_class


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('in_paths', nargs='+', help='Path(s) to pickles')
    ap.add_argument('-o', '--out', action='append',
                    help='Output path, or format where {} is to be '
                         'substituted with stripped input basename')
    # INSTEAD COULD DO -f for format, plus optional output dir??
    args = ap.parse_args()
    for in_path in args.in_paths:
        in_basename = os.path.splitext(os.path.basename(in_path))[0]
        with open(in_path, 'rb') as f:
            fig = pickle.load(f)
        for out_fmt in args.out:
            # FIXME: fig.canvas comes back None. I've not yet understood why/how
            out_ext = os.path.splitext(out_fmt)[-1]
            FigureCanvas = get_registered_canvas_class(out_ext)
            fig.canvas = FigureCanvas(fig)

            fig.savefig(out_fmt.format(in_basename))

if __name__ == '__main__':
    main()
