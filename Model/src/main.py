"""SimGNN runner."""

from utils import tab_printer
from simgnn import SimGNNTrainer
from param_parser import parameter_parser
import time
def main():
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a SimGNN model.
    """
    args = parameter_parser()
    tab_printer(args)
    trainer = SimGNNTrainer(args)
    if args.load_path and args.restart:
        trainer.load()
        trainer.fit()

    elif args.load_path and not(args.restart):
        start = time.time()
        trainer.load()
        end = time.time()
        print("Time:", end-start, "s")

    else:
        trainer.fit()
    trainer.score()
    if args.save_path:
        trainer.save()

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Time2:", end-start, "s")
