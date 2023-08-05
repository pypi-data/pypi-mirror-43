"""syphon.archive.archive.py

   Copyright Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/tektronix/syphon/blob/master/LICENSE)

"""
from syphon import Context


def archive(context: Context):
    """Store the files specified in the current context.

    Args:
        context (Context): Runtime settings object.

    Raises:
        FileExistsError: An archive file already exists with
            the same filepath.
        IndexError: Schema value is not a column header of a
            given DataFrame.
        OSError: File operation error. Error type raised may be
            a subclass of OSError.
        ParserError: Error raised by pandas.read_csv.
        ValueError: More than one unique metadata value exists
            under a column header.
    """
    from glob import glob
    from os import makedirs
    from os.path import exists, join, split

    from pandas import concat, DataFrame, read_csv, Series
    from pandas.errors import EmptyDataError, ParserError
    from sortedcontainers import SortedList
    from syphon.schema import check_columns, resolve_path

    from . import datafilter
    from . import file_map
    from ._lockmanager import LockManager

    lock_manager = LockManager()
    lock_list = list()

    # add '#lock' file to all data directories
    data_list = SortedList(glob(context.data))
    lock_list.append(lock_manager.lock(split(data_list[0])[0]))

    # add '#lock' file to all metadata directories
    meta_list = SortedList()
    if context.meta is not None:
        meta_list = SortedList(glob(context.meta))
        lock_list.append(lock_manager.lock(split(meta_list[0])[0]))

    fmap = file_map(data_list, meta_list)

    for datafile in fmap:
        _, datafilename = split(datafile)

        data_frame = None
        try:
            data_frame = DataFrame(read_csv(datafile, dtype=str))
        except EmptyDataError:
            # trigger the empty check below
            data_frame = DataFrame()
        except ParserError:
            lock_manager.release_all()
            raise

        if data_frame.empty:
            print('Skipping empty data file @ {}'.format(datafile))
            continue

        # remove empty columns
        data_frame.dropna(axis=1, how='all', inplace=True)

        total_rows, _ = data_frame.shape

        # merge all metadata files into a single DataFrame
        meta_frame = None
        for metafile in fmap[datafile]:
            try:
                new_frame = DataFrame(read_csv(metafile, dtype=str))
            except ParserError:
                lock_manager.release_all()
                raise

            new_frame.dropna(axis=1, how='all', inplace=True)
            for header in list(new_frame.columns.values):
                # complain if there's more than one value in a column
                if len(new_frame[header].drop_duplicates().values) > 1:
                    lock_manager.release_all()
                    raise ValueError(
                        'More than one value exists under the {} column.'
                        .format(header))

                if len(new_frame[header]) is total_rows:
                    if meta_frame is None:
                        meta_frame = new_frame[header]
                    else:
                        meta_frame = concat(
                            [meta_frame, new_frame[header]], axis=1)
                else:
                    meta_value = new_frame[header].iloc[0]
                    series = Series([meta_value] * total_rows, name=header)
                    if meta_frame is None:
                        meta_frame = DataFrame(series)
                    else:
                        meta_frame = concat([meta_frame, series], axis=1)

        if meta_frame is not None:
            data_frame = concat([data_frame, meta_frame], axis=1)

        try:
            check_columns(context.schema, data_frame)
        except IndexError:
            lock_manager.release_all()
            raise

        filtered_data = None
        filtered_data = datafilter(context.schema, data_frame)

        if len(filtered_data) is 0:
            filtered_data = [data_frame]

        for data in filtered_data:
            path = None
            try:
                path = resolve_path(context.archive, context.schema, data)
            except IndexError:
                lock_manager.release_all()
                raise
            except ValueError:
                lock_manager.release_all()
                raise

            target_filename = join(path, datafilename)

            if exists(target_filename) and not context.overwrite:
                lock_manager.release_all()
                raise FileExistsError('Archive error: file already exists @ '
                                      '{}'.format(target_filename))

            try:
                makedirs(path, exist_ok=True)
                data.to_csv(target_filename, index=False)
            except OSError:
                lock_manager.release_all()
                raise

            if context.verbose:
                print('Archive: wrote {0}'.format(target_filename))

    while lock_list:
        lock = lock_list.pop()
        lock_manager.release(lock)
