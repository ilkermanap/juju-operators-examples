#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/olm/defining-and-using-persistent-storage

# storage-filesystem-attach
# storage-filesystem-detaching


import logging
import os
import shutil

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus
import sys

logger = logging.getLogger(__name__)

EMOJI_CORE_HOOK_EVENT = "\U0001F4CC"
EMOJI_CHECK_MARK_BUTTON = "\U00002705"
EMOJI_CROSS_MARK_BUTTON = "\U0000274E"
EMOJI_COMPUTER_DISK = "\U0001F4BD"


class StorageFilesystemCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.logdata_storage_attached, self._logdata_storage_attached)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.logdata_storage_detaching, self._logdata_storage_detaching)

    def _logdata_storage_attached(self, event):
        """
        Executes before install for new units.
        When type is filesystem, a default ext4 filesystem is mounted at the location
        defined in metadata.yaml

        Install and enable the systemd mount file for the attached storage-filesystem.
        """
        logger.debug(EMOJI_COMPUTER_DISK + sys._getframe().f_code.co_name)

        shutil.copyfile('templates/etc/systemd/system/var-log-mylogs.mount',
                        '/etc/systemd/system/var-log-mylogs.mount')
        os.system('systemctl daemon-reload')

        # Start the storage unit here, or in some other hook.
        os.system('systemctl enable var-log-mylogs.mount --now')
        self.unit.status = ActiveStatus(f"{EMOJI_CHECK_MARK_BUTTON} Started /var/log/mylogs bind mount.")

    def _on_install(self, event):
        """
        TODO: Render dynamically a unit-file based on the location name?
        1. Query the unit for enabled storage-filesystem.
        """
        logger.debug(EMOJI_CORE_HOOK_EVENT + sys._getframe().f_code.co_name)
        self.unit.status = ActiveStatus(f"Ready (installed)")


    def _logdata_storage_detaching(self, event):
        """
        Disable the storage-filesystem and remove the unit file.
        """
        logger.debug(EMOJI_COMPUTER_DISK + sys._getframe().f_code.co_name)
        os.system('systemctl disable var-log-mylogs.mount --now')
        os.remove('/etc/systemd/system/var-log-mylogs.mount')
        self.unit.status = ActiveStatus(f"{EMOJI_CROSS_MARK_BUTTON} Disabled /var/log/mylogs bind mount.")


if __name__ == "__main__":
    main(StorageFilesystemCharm)
