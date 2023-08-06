#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Standard library import.
import argparse
import sys

# Third-part library import.

# Project library import.
import Read_histo
import Show_datas

######################

def opt_arg():
    """
    Option and arguments parse.
    @parameters : none.
    @return : parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Formated display the apt history file.",
                                     argument_default="raw")

    parser.add_argument("-r","--raw",
                        action="store_true",
                        default=True,
                        help="Display with raw format as though using 'cat' command (default option)")

    parser.add_argument("-n","--niceraw",
                        action="store_true",
                        default=False,
                        help="Display with raw format,but with a littel formatting")

    parser.add_argument("-d","--date",
                        type=str,
                        default=None,
                        help="Display for a date, or since this date (also use -u option)")

    parser.add_argument("-u","--until",
                        type=str,
                        default=None,
                        help="Display until this date (also use -d option)")

    parser.add_argument("--showdates",
                        action="store_true",
                        default=False,
                        help="Show dates which are be able only")

    return parser.parse_args()

def main():
    """
    Main function.
    @parameters : none.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    print("")
    args = opt_arg()

    show_datas = Show_datas.Show_datas()

    if args.niceraw:
        show_datas.nice_raw()

    elif args.showdates:
        show_datas.only_dates()
        args.raw = False

    elif args.date and not args.until:
        args.raw = False
        try:
            show_datas.date_ = args.date
            show_datas.nice_raw_one_date()
        except SyntaxError as e:
            print(e, "\n")

    elif args.until:
        if not args.date:
            print("Beginning date missing. Use --date or -d\n")
            return 1
        args.raw = False
        try:
            show_datas.date_ = args.date
            show_datas.end_date_ = args.until
            show_datas.nice_raw_between_dates()
        except SyntaxError as e:
            print(e, "\n")

    elif args.raw:
        show_datas.raw()

    return 0

######################

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)

