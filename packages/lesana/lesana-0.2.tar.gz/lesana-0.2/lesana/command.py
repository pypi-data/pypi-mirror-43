import logging
import os
import subprocess
import sys

import guacamole
import jinja2
from . import Collection, Entry


def edit_file_in_external_editor(filepath):
    # First we try to use $EDITOR
    try:
        editor = os.environ['EDITOR']
        subprocess.call([editor, filepath])
    except FileNotFoundError as e:
        if editor in str(e):
            logging.info(
                'Could not open file {} with $EDITOR (currently {})'.format(
                    filepath,
                    editor
                    )
                )
        else:
            logging.warning("Could not open file {}".format(filepath))
            return False
    else:
        return True
    # then we try to use sensible-editor (which should be available on
    # debian and derivatives)
    try:
        subprocess.call(['sensible-editor', filepath])
    except FileNotFoundError as e:
        if 'sensible-editor' in e.strerror:
            logging.debug(
                "Could not open file {} with editor: sensible-editor".format(
                    filepath
                    )
                )
        else:
            logging.warning("Could not open file {}".format(filepath))
            return False
    else:
        return True
    # and finally we fallback to vi, because ed is the standard editor,
    # but that would be way too cruel, and vi is also in posix
    try:
        subprocess.call(['vi', filepath])
    except FileNotFoundError as e:
        if 'vi' in e.strerror:
            logging.warning(
                "Could not open file {} with any known editor".format(filepath)
                )
            return False
        else:
            logging.warning("Could not open file {}".format(filepath))
            return False
    else:
        return True


class New(guacamole.Command):
    arguments = [
        (['--collection', '-c'], dict(
            help='The collection to work on (default .)'
            )),
        (['--no-git'], dict(
            help="Don't add the new entry to git",
            action="store_false",
            dest='git'
            )),
        ]

    def register_arguments(self, parser):
        for arg in self.arguments:
            parser.add_argument(*arg[0], **arg[1])

    def invoked(self, ctx):
        collection = Collection(ctx.args.collection)
        new_entry = Entry(collection)
        collection.save_entries([new_entry])
        filepath = os.path.join(
            collection.itemdir,
            new_entry.fname
            )
        if edit_file_in_external_editor(filepath):
            collection.update_cache([filepath])
            if ctx.args.git:
                collection.git_add_files([filepath])
        print(new_entry)


class Edit(guacamole.Command):
    arguments = [
        (['--collection', '-c'], dict(
            help='The collection to work on (default .)'
            )),
        (['--no-git'], dict(
            help="Don't add the new entry to git",
            action="store_false",
            dest='git'
            )),
        (['uid'], dict(
            help='uid of an entry to edit',
            )),
        ]

    def register_arguments(self, parser):
        for arg in self.arguments:
            parser.add_argument(*arg[0], **arg[1])

    def invoked(self, ctx):
        collection = Collection(ctx.args.collection)
        entry = collection.entry_from_uid(ctx.args.uid)
        if entry is None:
            return "No such entry: {}".format(ctx.args.uid)
        filepath = os.path.join(
            collection.itemdir,
            entry.fname
            )
        if edit_file_in_external_editor(filepath):
            collection.update_cache([filepath])
            if ctx.args.git:
                collection.git_add_files([filepath])
        print(entry)


class Index(guacamole.Command):
    arguments = [
        ]

    def register_arguments(self, parser):
        parser.add_argument(
            '--collection', '-c',
            help='The collection to work on (default .)',
            )
        parser.add_argument(
            'files',
            help='List of files to index (default: everything)',
            default=None,
            nargs='*'
            )

    def invoked(self, ctx):
        collection = Collection(ctx.args.collection)
        if ctx.args.files:
            files = (os.path.basename(f) for f in ctx.args.files)
        else:
            files = None
        indexed = collection.update_cache(fnames=files)
        print("Found and indexed {} entries".format(indexed))


class Search(guacamole.Command):
    arguments = [
        ]

    def register_arguments(self, parser):
        parser.add_argument(
            '--collection', '-c',
            help='The collection to work on (default .)'
            )
        parser.add_argument(
            '--template', '-t',
            help='Am',
            ),
        parser.add_argument(
            '--offset',
            type=int,
            ),
        parser.add_argument(
            '--pagesize',
            type=int,
            ),
        parser.add_argument(
            '--all',
            action='store_true',
            help='Return all available results'
            )
        parser.add_argument(
            'query',
            help='Xapian query to search in the collection',
            nargs='+'
            ),

    def invoked(self, ctx):
        # TODO: implement "searching" for everything
        if ctx.args.offset:
            logging.warning(
                "offset exposes an internal knob and MAY BE" +
                " REMOVED from a future release of lesana"
                )
        if ctx.args.pagesize:
            logging.warning(
                "pagesize exposes an internal knob and MAY BE" +
                " REMOVED from a future release of lesana"
                )
        offset = ctx.args.offset or 0
        pagesize = ctx.args.pagesize or 12
        collection = Collection(ctx.args.collection)
        if ctx.args.query == ['*']:
            results = collection.get_all_documents()
        else:
            collection.start_search(' '.join(ctx.args.query))
            if ctx.args.all:
                results = collection.get_all_search_results()
            else:
                results = collection.get_search_results(
                    offset,
                    pagesize)
        if ctx.args.template:
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(
                    searchpath='.',
                    followlinks=True,
                    ),
                # TODO: add autoescaping settings
                )
            try:
                template = env.get_template(ctx.args.template)
            except jinja2.exceptions.TemplateNotFound as e:
                logging.error("Could not find template: {}".format(e))
                sys.exit(1)
            else:
                print(template.render(entries=results))
        else:
            for entry in results:
                print(entry)


class Init(guacamole.Command):
    arguments = [
        (['--collection', '-c'], dict(
            help='The directory to work on (default .)',
            default='.'
            )),
        (['--no-git'], dict(
            help='Skip setting up git in this directory',
            action="store_false",
            dest='git'
            )),
        ]

    def register_arguments(self, parser):
        for arg in self.arguments:
            parser.add_argument(*arg[0], **arg[1])

    def invoked(self, ctx):
        Collection.init(
            ctx.args.collection,
            git_enabled=ctx.args.git,
            edit_file=edit_file_in_external_editor
            )


class Remove(guacamole.Command):
    def register_arguments(self, parser):
        parser.add_argument(
            '--collection', '-c',
            help='The collection to work on (default .)',
            )
        parser.add_argument(
            'entries',
            help='List of entries to remove',
            nargs='+',
            )

    def invoked(self, ctx):
        collection = Collection(ctx.args.collection)
        collection.remove_entries(uids=ctx.args.entries)
