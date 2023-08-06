# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE
"""
Record objects for the Simple Data Package format.
"""

from rowgenerators import get_cache
from .exc import *
from .doc import MetapackDoc, Resolver
from .package import open_package, Downloader
from .appurl import MetapackUrl, MetapackDocumentUrl, MetapackResourceUrl, MetapackPackageUrl
from .terms import Resource
from  . import jupyter

#from metapack.jupyter.magic import load_ipython_extension, unload_ipython_extension

from rowgenerators import set_default_cache_name

set_default_cache_name('metapack')

import rowgenerators.appurl.url

rowgenerators.appurl.url.default_downloader = Downloader.get_instance()
