# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
Functions for converting Jupyter notebooks
"""
import nbformat
from metapack import MetapackDoc
from metapack.cli.core import prt, err
from metapack.jupyter.core import logger, edit_notebook, get_cell_source, set_cell_source
from metapack.jupyter.exporters import NotebookExecutor, DocumentationExporter, HugoExporter, WordpressExporter
from metapack.jupyter.preprocessors import ExtractInlineMetatabDoc
from metapack.util import ensure_dir, copytree
from metatab import DEFAULT_METATAB_FILE
from nbconvert.writers import FilesWriter
from os import getcwd
from os.path import abspath, normpath, exists, dirname
from pathlib import Path
from rowgenerators.util import fs_join as join
from traitlets.config import Config


def convert_documentation(nb_path):
    """Run only the document conversion portion of the notebook conversion

      The final document will not be completel
    """

    with open(nb_path) as f:
        nb = nbformat.reads(f.read(), as_version=4)

    doc = ExtractInlineMetatabDoc(package_url="metapack+file:" + dirname(nb_path)).run(nb)

    package_name = doc.as_version(None)

    output_dir = join(getcwd(), package_name)

    de = DocumentationExporter(config=Config(), log=logger, metadata=doc_metadata(doc))
    prt('Converting documentation')
    output, resources = de.from_filename(nb_path)

    fw = FilesWriter()

    fw.build_directory = join(output_dir, 'docs')
    fw.write(output, resources, notebook_name='notebook')
    prt("Wrote documentation to {}".format(fw.build_directory))


def convert_notebook(nb_path):
    prt('Convert notebook to Metatab source package')

    if not exists(nb_path):
        err("Notebook path does not exist: '{}' ".format(nb_path))

    c = Config()

    pe = NotebookExecutor(config=c, log=logger)

    prt('Running the notebook')
    output, resources = pe.from_filename(nb_path)

    fw = FilesWriter()
    fw.build_directory = pe.output_dir

    fw.write(output, resources, notebook_name=DEFAULT_METATAB_FILE)

    de = DocumentationExporter(config=c, log=logger, metadata=doc_metadata(pe.doc))

    prt('Exporting documentation')
    output, resources = de.from_filename(nb_path)

    fw.build_directory = join(pe.output_dir, 'docs')
    fw.write(output, resources, notebook_name='notebook')

    new_mt_file = join(pe.output_dir, DEFAULT_METATAB_FILE)

    doc = MetapackDoc(new_mt_file)

    de.update_metatab(doc, resources)

    for lib_dir in pe.lib_dirs:
        lib_dir = normpath(lib_dir).lstrip('./')

        doc['Resources'].new_term("Root.PythonLib", lib_dir)

        path = abspath(lib_dir)
        dest = join(pe.output_dir, lib_dir)

        ensure_dir(dest)
        copytree(path, join(pe.output_dir, lib_dir))

    doc.write_csv()

    # Reset the input to use the new data

    prt('Running with new package file: {}'.format(new_mt_file))


def extract_metatab(nb_path):
    if not exists(nb_path):
        err("Notebook path does not exist: '{}' ".format(nb_path))

    c = Config()

    with open(nb_path) as f:
        nb = nbformat.reads(f.read(), as_version=4)

    return ExtractInlineMetatabDoc(package_url="metapack+file:" + dirname(nb_path)).run(nb)


def doc_metadata(doc):
    """Create a metadata dict from a MetatabDoc, for Document conversion"""

    r = doc['Root'].as_dict()
    r.update(doc['Contacts'].as_dict())
    r['author'] = r.get('author', r.get('creator', r.get('wrangler')))

    return r


def convert_hugo(nb_path, hugo_path):
    from os import environ
    from os.path import abspath

    # Total hack. Would like the -H to be allowed to have no arg, and then use the env var,
    # but I don't know how to do that. This is the case where the user types
    # -H nb_path, so just go with it.
    if hugo_path and not nb_path:
        nb_path = hugo_path
        hugo_path = environ.get('METAPACK_HUGO_DIR')

    if not hugo_path:
        err("Must specify value for -H or the METAPACK_HUGO_DIR environment var")

    if not exists(nb_path):
        err("Notebook path does not exist: '{}' ".format(nb_path))

    c = Config()
    c.HugoExporter.hugo_dir = abspath(hugo_path)  # Exports assume rel path is rel to notebook
    he = HugoExporter(config=c, log=logger)

    output, resources = he.from_filename(nb_path)

    prt('Writing Notebook to Hugo Markdown')

    prt('    Writing ', resources['unique_key'] + resources['output_extension'])
    for k, v in resources['outputs'].items():
        prt('    Writing ', k)

    fw = FilesWriter()
    fw.write(output, resources, notebook_name=resources['unique_key'])


def convert_wordpress(nb_path, wp_path):
    if not exists(nb_path):
        err("Notebook path does not exist: '{}' ".format(nb_path))

    c = Config()
    c.WordpressExporter.staging_dir = wp_path
    he = WordpressExporter(config=c, log=logger)

    output, resources = he.from_filename(nb_path)

    prt('Writing Notebook to Wordpress HTML')

    output_file = resources['unique_key'] + resources['output_extension']
    prt('    Writing ', output_file)

    resource_outputs = []

    for k, v in resources['outputs'].items():
        prt('    Writing ', k)
        resource_outputs.append(k)

    fw = FilesWriter()
    fw.write(output, resources, notebook_name=resources['unique_key'])

    return output_file, resource_outputs


def extract_notebook_metatab(nb_path: Path):
    """Extract the metatab lines from a notebook and return a Metapack doc """

    from metatab.rowgenerators import TextRowGenerator
    import nbformat

    with nb_path.open() as f:
        nb = nbformat.read(f, as_version=4)

    lines = '\n'.join(['Declare: metatab-latest'] + [get_cell_source(nb, tag) for tag in ['metadata', 'resources',
                                                                                     'schema']])
    doc = MetapackDoc(TextRowGenerator(lines))

    doc['Root'].get_or_new_term('Root.Title').value = get_cell_source(nb, 'Title').strip('#').strip()
    doc['Root'].get_or_new_term('Root.Description').value = get_cell_source(nb, 'Description')

    doc['Documentation'].get_or_new_term('Root.Readme').value = get_cell_source(nb, 'readme')

    return doc


def write_metatab_notebook(doc, nb_path: Path = None):

    nb_path = nb_path or Path('metadata.ipynb')

    def as_lines(s, excludes):
        return '\n'.join('{}: {}'.format(t, v or '') for t, v in s.lines if t not in excludes)

    with edit_notebook(nb_path) as nb:
        set_cell_source(nb, 'Title', "# " + (doc.get_value('Root.Title') or ''))
        set_cell_source(nb, 'Description', doc.description)
        set_cell_source(nb, 'metadata',
                        '\n\n'.join(as_lines(s, ['Title', 'Description', 'Declare', 'Readme'])
                                    for s in doc if s.name.lower() not in ['references', 'resources',
                                                                           'schema']))
        set_cell_source(nb, 'resources',
                        '\n\n'.join(s.as_lines() for s in doc if s.name.lower() in ['references', 'resources']))

        set_cell_source(nb, 'schema',
                        '\n\n'.join(s.as_lines() for s in doc if s.name.lower() in ['schema']))


        set_cell_source(nb, 'readme', (doc.get_value('Root.Readme') or '').strip())


