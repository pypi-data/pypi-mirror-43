# Copyright 2016-2018 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Vincent Garonne, <vgaronne@gmail.com>, 2016-2018
# - Hannes Hansen, <hannes.jakob.hansen@cern.ch>, 2018

"""
Reaper is a daemon to manage file on disk but not in Rucio(dark data) deletion
"""

import argparse
import signal

from rucio.daemons.reaper.dark_reaper import run, stop


def get_parser():
    """
    Returns the argparse parser.
    """
    parser = argparse.ArgumentParser(description="The Dark-Reaper daemon is responsible for the deletion of quarantined replicas.")
    parser.add_argument("--run-once", action="store_true", default=False, help='One iteration only')
    parser.add_argument("--all-rses", action="store_true", default=False, help='Select RSEs from the quarantined queues')
    parser.add_argument("--total-workers", action="store", default=1, type=int, help='Total number of workers per process')
    parser.add_argument("--chunk-size", action="store", default=10, type=int, help='Chunk size')
    parser.add_argument("--scheme", action="store", default=None, type=str, help='Force the reaper to use a particular protocol, e.g., mock.')
    parser.add_argument('--rses', nargs='+', type=str, help='List of RSEs')
    return parser


def main():
    signal.signal(signal.SIGTERM, stop)
    parser = get_parser()
    args = parser.parse_args()
    try:
        run(total_workers=args.total_workers, chunk_size=args.chunk_size,
            once=args.run_once, scheme=args.scheme, rses=args.rses,
            all_rses=args.all_rses)
    except KeyboardInterrupt:
        stop()
