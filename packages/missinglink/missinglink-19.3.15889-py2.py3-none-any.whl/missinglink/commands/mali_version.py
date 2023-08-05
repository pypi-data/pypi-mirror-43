# -*- coding: utf8 -*-
import os
from self_update.sdk_version import get_version


class MissinglinkVersion:

    package = 'missinglink'

    @classmethod
    def get_missinglink_cli_version(cls):
        return os.environ.get('_ML_FORCE_VERSION', get_version(cls.package))

    @classmethod
    def get_missinglink_package(cls):
        return cls.package
