# -*- coding: utf-8 -*-

# Standard libraries import.
import re
import datetime as dt

# Third libraries import.


# Projet modules import.
import Read_histo

######################

class Show_datas(Read_histo.Read_histo):
    """
    Show datas as will.

    Public attributes.
        datas = datas read.
    """

    # Private attributes.
        # __date = date, or begin date to see.
        # __end_date = end date to see.


    # Public methods.
    def __init__(self):
        """
        __init__ : initiate class
        @parameters : none.
        @return : none.
        """
        self.__date = None
        self.__end_date = None
        self.datas = None

        super().__init__()

    # ++++++++++ Properties

    @property
    def date_(self):
        """
        Not used.
        """
        pass

    @date_.setter
    def date_(self, date_to_check):
        """
        Set the date/beginning date. Raise an SyntaxError exception if fail.
        @parameters : date = date, or begin date to see.
        @return : none.
        """
        rstr = self.__check_date(date_to_check)
        if not rstr:
            self.__date = date_to_check

        else:
            raise SyntaxError(rstr)

    @property
    def end_date_(self):
        """
        Not used.
        """
        pass

    @date_.setter
    def end_date_(self, date_to_check):
        """
        Set the end date. Raise an SyntaxError exception if fail.
        @parameters : date = date, or begin date to see.
        @return : none.
        """
        rstr = self.__check_date(date_to_check)
        if not rstr:
            self.__end_date = date_to_check

        else:
            raise SyntaxError(rstr)

        startd = dt.datetime.strptime(self.__date, "%Y-%m-%d")
        stopd = dt.datetime.strptime(self.__end_date, "%Y-%m-%d")
        # Keep these variables if, one day, i am nice guy, and decide to reverse both dates,
        # if this case occure : beginning date is after end date.

        if startd > stopd :
            raise SyntaxError("The end is before the beginning !")

    # ++++++++++

    def raw(self):
        """
        Reading (un)compressed history file, and print as-is each line on terminal.
        @parameters : none.
        @return : none.
        """
        for histo_file in self.histo_files:
            print("{} {}".format(4*"-", histo_file))

            for data in self.read_for(histo_file):
                print(data, end='')

            print("")

    def nice_raw(self):
        """
        Reading (un)compressed history file, and print each line on terminal within better way.
        @parameters : none.
        @return : none.
        """
        for histo_file in self.histo_files:
            print("In {} :".format(histo_file))

            for bloc in self.__reform_apt_histofile(histo_file):
                # Separation to be able to manipulate string of date easier, bellow.
                start_date = bloc["Start-Date"].strip().split("  ")
                end_date = bloc["End-Date"].strip().split("  ")
                used_apt_cde = bloc["Commandline"].strip()
                what_done = bloc["SubCommands"]

                self.__print_nice(start_date, end_date, used_apt_cde, what_done, True)

                print("\n")
            print("\n")

    def nice_raw_one_date(self):
        """
        Reading (un)compressed history file, and print each line on terminal within better way for only the date.
        @parameters : none.
        @return : none.
        """
        self.extract_dates()

        print("In {}, found : ".format(self.__date), end='')

        if self.__date not in self.extracted_dates:
            print("Nothing\n")

        else:
            old_histo_file = ""     # Display only one time the filename.

            for histo_file in self.histo_files:
                for bloc in self.__reform_apt_histofile(histo_file):
                    # Separation to be able to manipulate string of date easier, bellow.
                    start_date = bloc["Start-Date"].strip().split("  ")

                    if self.__date and start_date[0] == self.__date:

                        if histo_file != old_histo_file:
                            print("\n\nIn file {} :".format(histo_file))
                            old_histo_file = histo_file

                        # Separation to be able to manipulate string of date easier, bellow.
                        end_date = bloc["End-Date"].strip().split("  ")
                        used_apt_cde = bloc["Commandline"].strip()
                        what_done = bloc["SubCommands"]

                        self.__print_nice(start_date, end_date, used_apt_cde, what_done, False)
                        print("\n")

    def nice_raw_between_dates(self):
        """
        Reading (un)compressed history file, and print each line on terminal within better way
        between 2 dates.
        @parameters : none.
        @return : none.
        """
        self.extract_dates()

        print("From {} to {} found :".format(self.__date, self.__end_date), end='')

        if self.__date not in self.extracted_dates:
            print("\n\nNothing\n")

        else:
            # Parse to manipulate easely.
            b_date = dt.datetime.strptime(self.__date, "%Y-%m-%d")
            e_date = dt.datetime.strptime(self.__end_date, "%Y-%m-%d")

            old_histo_file = ""     # Display only one time the filename.
            old_date_checked = ""   # Display only if date change.

            for histo_file in self.histo_files:
                for bloc in self.__reform_apt_histofile(histo_file):
                    # Separation to be able to manipulate string of date easier, bellow.
                    start_date = bloc["Start-Date"].strip().split("  ")
                    r_date = dt.datetime.strptime(start_date[0], "%Y-%m-%d")
                    if self.__date and r_date >= b_date and r_date < e_date + dt.timedelta(days=1):

                        if histo_file != old_histo_file:
                            print("\n\nIn file {} :".format(histo_file))
                            old_histo_file = histo_file

                        if r_date != old_date_checked:
                            print("In {}, found :\n".format(start_date[0]), end='')
                            old_date_checked = r_date

                        # Separation to be able to manipulate string of date easier, bellow.
                        end_date = bloc["End-Date"].strip().split("  ")
                        used_apt_cde = bloc["Commandline"].strip()
                        what_done = bloc["SubCommands"]

                        self.__print_nice(start_date, end_date, used_apt_cde, what_done, False)
                        print("\n")

    def only_dates(self):
        """
        Display only the found dates.
        @parameters : none.
        @return : none.
        """
        print("Dates found :")

        self.extract_dates()

        for extracted_date in self.extracted_dates:
            print(extracted_date)

        print("\n", end='')


    # Private methods.
    def __print_nice(self, start_date, end_date, used_apt_cde, what_done, display_start_date):
        """
        Display in a "nice" way.
        @parameters : start_date = start date to display.
                      end_date = end date to display.
                      used_apt_cde = used commands to display.
                      what_done = display what it was done.
                      display_start_date = False => display only time, everelse date & time.
        @return : none.
        """
        if display_start_date:
            print(" Start in {}, at {}".format(start_date[0], start_date[1]))
        else:
            print(" Start at {}".format(start_date[1]))

        print(" End in {}, at {}".format(end_date[0], end_date[1]))
        print("   Done with {}".format(used_apt_cde))

        for subcde in self.__prepare_sub_cde(what_done):
            print("     {} :".format(subcde[0]))
            print("       ", end='')

            for pkg in self.__prepare_pkg(subcde[1]):
                print("{} ".format(pkg[0]), end="")

    def __check_date(self, date_to_check):
        """
        Check the given date.setter
        @parameters : date = date to check format.
        @return : string empty (all ok), or the problem occured.
        """
        # don't uses dt.datetime.strptime(date_to_check, "%Y-%m-%d") exception raising
        # to check date, need to detail what's wrong. And also i already write this below.

        days_by_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        date_ok = re.match('^(\d{4})(-)(\d{2})(-)(\d{2})$', date_to_check)       # No miss formated date?
        if not date_ok:
            return "Please, check date format as YYYY-MM-DD"

        # It was checked about digit or not, in regex.
        year = int(date_ok.group(1))
        month = int(date_ok.group(3))
        day = int(date_ok.group(5))

        if month < 1 or month > 12:
            return "Month is not [01-12]"

        if year % 4 == 0:
            days_by_month[1] = 29

        if day < 1 or day > days_by_month[month - 1]:
            return "Day is not [01-{}]".format(days_by_month[month - 1])

        if dt.date.today() < dt.date(year, month, day) :
            return "Can't read the Future !"

        return ""

    def __prepare_pkg(self, packages):
        """
        Prepare the packages to be displayed as we wish.
        @parameters : pkgs = packages to prepare to be displayed.
        @return : list of packages.
        """
        pkgs = []

        for pkg in packages.split("),"):
            # TODO: find something better. Uggly !!!!!! (Try re module).
            np = pkg.split(":")[0].strip()
            arch = pkg.split(":")[1].split(" (")[0]
            vers = pkg.split(":")[1].split(" (")[1].split(", ")[0]
            # TODO: try if something other
    #        other = pkg.split(":")[1].split(" (")[1].split(", ")[1]

            pkgs.append([np, arch, vers, ])

        return pkgs

    def __prepare_sub_cde(self, subcommands):
        """
        Generator to prepare sub commands to be beautifully displayed (huhu).
        @parameters : subcommands = apt sub-commands to dispaly with packages worked on.
        @return : the sub command and their packages.
        """
        subcdes = sorted(subcommands.keys())

        for subcde in subcdes:
            yield [subcde.strip(), subcommands[subcde].strip()]

    def __reform_apt_histofile(self, histofile):
        """
        Reform all apt history file into list of action.
        @parameters : histofile = the whole path of apt history file.
        @return : yield a bloc of apt history as list.
        """
        for line in self.read_for(histofile):
            line = line.strip()

            if line:
                key = line.split(":", 1)[0]
                value = line.split(":", 1)[1]

                if line.find("Start-Date") > -1:
                    bloc = {"SubCommands" : {}}
                    bloc[key] = value

                elif line.find("End-Date") > -1:
                    bloc[key] = value
                    yield bloc

                elif line.find("Commandline") > -1:
                    bloc[key] = value

                else:
                    subcde = line.strip().split(":", 1)[0]
                    pkg = line.strip().split(":", 1)[1]
                    bloc["SubCommands"][subcde] = pkg

            else:
                line = "You should not see me !"

######################

if __name__ == "__main__":
    help(Show_datas)
