"""Status misc segment for showing NordVPN connection status."""

import enum

from .base import StatusMiscSegment

class TransmissionNotificationSegment(StatusMiscSegment):
    """Status line segment showing numbers of transmission statuses."""

    name = 'transmission'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._transmission = None
        # pylint: disable=access-member-before-definition
        if not self.sections:
            self.sections = [self.TransmissionSectionStatus.COMPLETE,
                             self.TransmissionSectionStatus.INCOMPLETE]
        else:
            self.sections = [self.TransmissionSectionStatus[x.upper()] for x in self.sections]

    class TransmissionSectionStatus(enum.IntEnum):
        """Possible count that can be shown on this status segment."""

        DOWNLOADING = enum.auto()
        DOWNLOADING_HIGH_PRIORITY = enum.auto()
        SEEDING = enum.auto()
        PAUSED = enum.auto()
        COMPLETE = enum.auto()
        INCOMPLETE = enum.auto()
        CHECKING = enum.auto()

    @classmethod
    def parser_args(cls, parser):
        t_parser = parser.add_argument_group('transmission')
        t_parser.add_argument(f'--{cls.name}-icon', default='T', metavar='ICON',
                              help='Icon to prefix download status numbers')
        t_parser.add_argument(f'--{cls.name}-icon-style',
                              default='', metavar='STYLE',
                              help='Styling for transmission icon')
        t_parser.add_argument(f'--{cls.name}-sections', nargs='+',
                              choices=[x.name.lower() for x in cls.TransmissionSectionStatus],
                              help='Possible sections and the order in which they appear')
        t_parser.add_argument(f'--{cls.name}-section-styles', nargs='+',
                              metavar='STYLE',
                              help=f'Styles for {cls.name.upper()}_SECTIONS in the same order')
        t_parser.add_argument(f'--{cls.name}-format',
                              default='{:02d}',
                              help='Format string for transmission torrent counts')
        t_parser.add_argument(f'--{cls.name}-hide-zero',
                              action='store_true',
                              help="When true don't show empty torrent sections")

    def render(self):
        # pylint: disable=no-member,import-outside-toplevel
        from mohkale import transmission as t
        if not self._transmission:
            self._transmission = t.Transmission.from_conf_file()
        if not self._transmission.check():
            return None
        try:
            # KLUDGE: Including fields based on sections is hacky :/.
            resp = self._transmission.command(
                'torrent-get',
                fields=['status', 'percentDone']
                + (['bandwidthPriority'] if self.TransmissionSectionStatus.DOWNLOADING_HIGH_PRIORITY in self.sections else []))
            torrents = resp['arguments']['torrents']
        except KeyError:
            return None

        COUNT_PREDICATES = {
            self.TransmissionSectionStatus.DOWNLOADING: lambda torrent: torrent['status'] == t.TransmissionTorrentStatus.download,
            self.TransmissionSectionStatus.DOWNLOADING_HIGH_PRIORITY: lambda torrent:
            torrent['status'] == t.TransmissionTorrentStatus.download
            and torrent['bandwidthPriority'] > 0,
            self.TransmissionSectionStatus.SEEDING: lambda torrent: torrent['status'] == t.TransmissionTorrentStatus.seed,
            self.TransmissionSectionStatus.PAUSED: lambda torrent:
            torrent['status'] == t.TransmissionTorrentStatus.download_wait
            or torrent['status'] == t.TransmissionTorrentStatus.seed_wait
            or torrent['status'] == t.TransmissionTorrentStatus.check_wait,
            self.TransmissionSectionStatus.COMPLETE: lambda torrent: torrent['percentDone'] == 1,
            self.TransmissionSectionStatus.INCOMPLETE: lambda torrent: torrent['percentDone'] != 1,
            self.TransmissionSectionStatus.CHECKING: lambda torrent:
            torrent['status'] == t.TransmissionTorrentStatus.check
            or torrent['status'] == t.TransmissionTorrentStatus.check_wait,
        }
        counts = {x: 0 for x in COUNT_PREDICATES}
        for torrent in torrents:
            for key, pred in COUNT_PREDICATES.items():
                if pred(torrent):
                    counts[key] += 1

        res = []
        for i, section in enumerate(self.sections):
            style = ''
            if self.section_styles and len(self.section_styles) > i:
                style = self.section_styles[i]
            if counts[section] == 0 and self.hide_zero:
                continue
            res.append(self._style(self.format.format(counts[section]), style))
        if not res:
            return None
        return ((self._style(self.icon, self.icon_style) + ' ') if self.icon else '') + ' '.join(res)
