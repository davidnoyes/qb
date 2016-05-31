#!/usr/bin/env python3

import logging
import sys

from pylxd import Client  # https://pylxd.readthedocs.io/


class Container(object):
    """ Class to wrap Container functionality. """

    def __init__(self, url, cert, key):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("Using LXD API config:\n"
                     "     URL: %s\n"
                     "     Cert: %s\n"
                     "     Key: %s" % (url, cert, key))

        # Create an LXD client instance.
        self.lxd = Client(
            endpoint=url,
            cert=(cert, key),
            verify=False
        )

    def list(self):
        """ Function to list a qb containers. """

        self.p.debug("Listing containers...")

    def create(self, name, image):
        """ Create a qb container. """

        # TODO: Pull config from elsewhere using 'name'.
        # Create the LXD API JSON payload.
        config = {
            'name': '%s' % name,
            'architecture': 'x86_64',
            'profiles': [
                'default'
            ],
            'ephemeral': False,
            'config': {
                'limits.cpu': '2'
            },
            'source': {
                'type': 'image',
                'mode': 'pull',
                'protocol': 'simplestreams',
                'server': 'https://cloud-images.ubuntu.com/releases',
                'alias': '14.04'
            }
        }

        # Create the container.
        self.p.info("Creating \"%s\" from the \"%s\" image..." % (name, image))

        try:
            container = self.lxd.containers.create(config, wait=True)

        except:
            self.p.error("Failed to create container.")
            sys.exit(1)

        return container

    def start(self, name):
        """ Start a qb container. """

        self.p.info("Starting \"%s\"..." % name)

    def stop(self, name):
        """ Stop a qb container. """

        self.p.debug("Stopping \"%s\"..." % name)

    def remove(self, name):
        """ Remove a qb container. """

        self.p.debug("Removing \"%s\"..." % name)
