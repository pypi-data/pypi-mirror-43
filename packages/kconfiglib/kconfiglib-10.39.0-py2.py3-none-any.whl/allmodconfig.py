#!/usr/bin/env python

# Copyright (c) 2018-2019, Ulf Magnusson
# SPDX-License-Identifier: ISC

# Works like 'make allmodconfig'. Verified by the test suite to generate output
# identical to 'make allmodconfig', for all ARCHES.
#
# The default output filename is '.config'. A different filename can be passed
# in the KCONFIG_CONFIG environment variable.
#
# Usage for the Linux kernel:
#
#   $ make [ARCH=<arch>] scriptconfig SCRIPT=Kconfiglib/examples/allyesconfig.py

import kconfiglib


def main():
    kconf = kconfiglib.standard_kconfig()

    # See allnoconfig.py
    kconf.disable_warnings()

    # Small optimizations
    BOOL = kconfiglib.BOOL
    TRISTATE = kconfiglib.TRISTATE

    for sym in kconf.unique_defined_syms:
        if sym.orig_type == BOOL:
            # 'bool' choice symbols get their default value, as determined by
            # e.g. 'default's on the choice
            if not sym.choice:
                # All other bool symbols get set to 'y', like for allyesconfig
                sym.set_value(2)
        elif sym.orig_type == TRISTATE:
            sym.set_value(1)

    for choice in kconf.unique_choices:
        choice.set_value(2 if choice.orig_type == BOOL else 1)

    kconf.enable_warnings()

    kconfiglib.load_allconfig(kconf, "allmod.config")

    kconf.write_config()


if __name__ == "__main__":
    main()
