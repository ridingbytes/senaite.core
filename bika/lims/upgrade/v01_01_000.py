from Acquisition import aq_inner
from Acquisition import aq_parent

from bika.lims import logger
from bika.lims.catalog import CATALOG_ANALYSIS_LISTING
from bika.lims.config import PROJECTNAME as product
from bika.lims.upgrade import upgradestep
from bika.lims.upgrade.utils import UpgradeUtils

version = '1.1.0'
profile = 'profile-{0}:default'.format(product)


@upgradestep(product, version)
def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    # Since this upgrade is precisely meant to establish a version regardless
    # of the version numbering at bikalims/bika.lims, we don't want this check
    # to be performed.
    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        # The currently installed version is more recent than the target
        # version of this upgradestep
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))
    # Add missing getDateSubmitted Index into analyses catalog
    ut.addIndex(
        CATALOG_ANALYSIS_LISTING, 'getDateSubmitted', 'DateIndex')
    ut.refreshCatalogs()
    # Do nothing, we just only want the profile version to be 1.0.0
    logger.info("{0} upgraded to version {1}".format(product, version))
    return True
