#!/usr/bin/env python3

""" nv applicaiton """

import argparse
import notesviewer.vardata
import notesviewer.interactive
import notesviewer.commands
from notesviewer.config import loadconfig, set_data_location


def main():
    """ main application function """
    loadconfig()
    set_data_location()
    parse_arguments()


def parse_arguments():
    """ parse all the program arguments """

    # create the root parser
    parser = argparse.ArgumentParser()

    # create subparser
    subparser = parser.add_subparsers(dest='cmd')

    # version command
    version_parser = subparser.add_parser('version')

    # init notes directory
    init_parser = subparser.add_parser('init')

    # add
    add_parser = subparser.add_parser('add')
    add_parser.add_argument('name', action='store')

    # insert
    add_parser = subparser.add_parser('insert')
    add_parser.add_argument('name', action='store')
    add_parser.add_argument('title', action='store')

    # edit
    edit_parser = subparser.add_parser('edit')
    edit_parser.add_argument('entry', action='store', type=int)
    edit_parser.add_argument('note', action='store')

    # delete
    delete_parser = subparser.add_parser('delete')
    delete_parser.add_argument('name', action='store')

    # remove
    remove_parser = subparser.add_parser('remove')
    remove_parser.add_argument('entry', action='store', type=int)
    remove_parser.add_argument('name', action='store')

    # move
    move_parser = subparser.add_parser('move')
    move_parser.add_argument('entry', action='store', type=int)
    move_parser.add_argument('fromnote', action='store')
    move_parser.add_argument('tonote', action='store')

    # add tags
    addtags_parser = subparser.add_parser('addtags')
    addtags_parser.add_argument('note', action='store')
    addtags_parser.add_argument('tag', action='store')

    # show tags
    tags_parser = subparser.add_parser('tags')
    tags_parser.add_argument('note', action='store')

    # remove tags
    remove_parser = subparser.add_parser('removetags')
    remove_parser.add_argument('note', action='store')
    remove_parser.add_argument('tags', action='store')

    # list
    list_parser = subparser.add_parser('list')
    list_parser.add_argument('--verbose', '-v', action='store_true')

    # display
    display_parser = subparser.add_parser('display')
    display_parser.add_argument('note', action='store')
    display_parser.add_argument('--short', '-s', action='store_true')

    # showconfig
    showconfig_parser = subparser.add_parser('showconfig')

    # setdefaultconfig
    setdefaultconfig_parser = subparser.add_parser('setdefaultconfig')

    # search
    search_parser = subparser.add_parser('search')
    search_parser.add_argument('regex', action='store')
    search_parser.add_argument(dest="note", action='store')

    # status
    status_parser = subparser.add_parser('check')

    # interactive
    interactive_parser = subparser.add_parser('interactive')

    # info lists python version and modues vesion for debugging
    info_parser = subparser.add_parser('info')

    # parse user arguments
    args = vars(parser.parse_args())
    if args['cmd'] is None:
        notesviewer.file.print_err_msg("Missing command")
        parser.print_usage()
    process_args(args)


def process_args(argument):
    """ call the cm function for an arument """

    if argument['cmd'] == 'version':
        notesviewer.commands.cm_version()
    elif argument['cmd'] == 'info':
        notesviewer.commands.cm_info()
    elif argument['cmd'] == 'setdefaultconfig':
        notesviewer.commands.cm_setdefaultconfig()
    elif argument['cmd'] == 'showconfig':
        notesviewer.commands.cm_showconfig()
    elif argument['cmd'] == 'init':
        notesviewer.commands.cm_init()
    elif argument['cmd'] == 'list':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_list(argument['verbose'])
    elif argument['cmd'] == 'add':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_add(argument['name'])
    elif argument['cmd'] == 'insert':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_insert(argument['name'], argument['title'])
    elif argument['cmd'] == 'edit':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_edit(argument['entry'], argument['note'])
    elif argument['cmd'] == 'delete':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_delete(argument['name'])
    elif argument['cmd'] == 'remove':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_remove(argument['entry'], argument['name'])
    elif argument['cmd'] == 'move':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_move(argument['entry'],
                                     argument['fromnote'],
                                     argument['tonote'])
    elif argument['cmd'] == 'addtags':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_addtags(argument['note'], argument['tag'])
    elif argument['cmd'] == 'tags':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_tags(argument['note'])
    elif argument['cmd'] == 'removetags':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_removetags(argument['note'],
                                           argument['tags'])
    elif argument['cmd'] == 'display':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_display(argument['note'],
                                        argument['short'])
    elif argument['cmd'] == 'search':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_search(argument['regex'], argument['note'])
    elif argument['cmd'] == 'check':
        notesviewer.file.verify_notes_root_path()
        notesviewer.commands.cm_check()
    elif argument['cmd'] == 'interactive':
        notesviewer.file.verify_notes_root_path()
        notesviewer.interactive.interactive()


if __name__ == '__main__':
    main()
