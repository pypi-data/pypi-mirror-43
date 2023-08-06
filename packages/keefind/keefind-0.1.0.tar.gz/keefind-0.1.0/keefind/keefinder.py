import pprint
import sys

from pykeepass import entry
from pykeepass import group
from pykeepass import PyKeePass


class KeeFinder(object):
    def __init__(self, db_path, db_pass, verbosity):
        self.db = PyKeePass(db_path, db_pass)
        self.verbosity = verbosity
        self.found_entries = list()

    def find(self, strings):
        if not isinstance(strings, list):
            raise TypeError("Passed value has to be list type")
        self.found_entries = self._find_entries(strings[-1])
        if not self.found_entries:
            return
        if len(strings) > 1:
            self.found_entries = self._find_in_entries(
                self.found_entries, strings[:-1])

    def print_found(self):
        if not self.found_entries:
            print('Nothing found')
            return
        for entr in self.found_entries:
            self._print_entry(entr, self.verbosity)

    def _find_entries(self, substring, glob=True):
        search_string = substring.lower()
        res = list()
        if glob:
            search_string = '.*%s.*' % search_string
        method_names = ['title', 'username', 'url', 'password', 'path']
        for method_name in method_names:
            method = getattr(self.db, 'find_entries_by_%s' % method_name)
            results = method(search_string, regex=True, flags='i')
            for result in results:
                if result not in res:
                    res.append(result)

        root_group = self.db.find_groups_by_path('/')
        res_groups = list()
        # Now any group in res_groups will have a substring in path
        self._find_groups(substring, root_group, res_groups)
        for grp in res_groups:
            # As group has substring in path, it means any entry in this group
            # will have this substring in path too. There is no other way to do
            # this, sorry
            group_entries = self.db.find_entries_by_title(
                '.*', regex=True, group=grp)
            for entr in group_entries:
                if entr not in res:
                    res.append(entr)
        return res

    def _find_in_entries(self, entries, entry_names):
        survivors = entries.copy()
        while entry_names:
            entry_name = entry_names.pop()
            for index, entr in enumerate(entries):
                if not self._find_in_entry(entry_name, entr):
                    survivors.remove(entr)
            survivors = self._find_in_entries(survivors, entry_names)
        return survivors

    def _find_in_entry(self, substring, entr):
        substring = substring.lower()
        if isinstance(entr, entry.Entry):
            subentries = [entr.group.path, entr.title, entr.username,
                          entr.password, entr.url]
        elif isinstance(entr, group.Group):
            subentries = [entr.path]
        for subentry in subentries:
            if subentry and (substring in subentry.lower()):
                return True
        return False

    def _find_groups(self, name, root_groups, result=[]):
        for grp in root_groups:
            if name.lower() in grp.path.lower():
                result.append(grp)
            subgroups = grp.subgroups
            self._find_groups(name, subgroups, result)

    def _print_entry(self, entr, verbosity):
        info = dict()

        def _get_fields(count):
            _info = dict()
            fields = ('group', 'username', 'password', 'title', 'url')
            if count == 2:
                fields = fields[:3]
            for field in fields:
                if field == 'group':
                    _info[field] = entr.group.path
                else:
                    _info[field] = getattr(entr, field)
            return _info

        if not verbosity:
            print(entr.password)
        elif verbosity == 1:
            print("%s - %s" % (entr.group.path, entr.username),
                  file=sys.stderr)
            print(entr.password, end="")
            sys.stdout.flush()
            print("", file=sys.stderr)
        else:
            info = _get_fields(verbosity)

        if info:
            pprint.pprint(info)
            print()
