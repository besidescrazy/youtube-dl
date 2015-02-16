# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_urlparse
from ..utils import month_by_abbreviation
import re


class YamIE(InfoExtractor):
    _VALID_URL = r'http://mymedia.yam.com/m/(?P<id>\d+)'

    _TESTS = [{
        # An audio hosted on Yam
        'url': 'http://mymedia.yam.com/m/2283921',
        'md5': 'c011b8e262a52d5473d9c2e3c9963b9c',
        'info_dict': {
            'id': '2283921',
            'ext': 'mp3',
            'title': '發現 - 趙薇 京華煙雲主題曲',
            'uploader_id': 'princekt',
            'upload_date': '20080807',
            'duration': 313.0,
        }
    }, {
        # An external video hosted on YouTube
        'url': 'http://mymedia.yam.com/m/3598173',
        'md5': '0238ceec479c654e8c2f1223755bf3e9',
        'info_dict': {
            'id': 'pJ2Deys283c',
            'ext': 'mp4',
            'upload_date': '20150202',
            'uploader': '新莊社大瑜伽社',
            'description': 'md5:f5cc72f0baf259a70fb731654b0d2eff',
            'uploader_id': '2323agoy',
            'title': '外婆的澎湖灣KTV-潘安邦',
        }
    }]

    def _real_extract(self, url):
        media_id = self._match_id(url)
        page = self._download_webpage(url, media_id)

        # Is it hosted externally on YouTube?
        youtube_url = self._html_search_regex(
            r'<embed src="(http://www.youtube.com/[^"]+)"',
            page, 'YouTube url', default=None)
        if youtube_url:
            return self.url_result(youtube_url, 'Youtube')

        api_page = self._download_webpage(
            'http://mymedia.yam.com/api/a/?pID=' + media_id, media_id)
        api_result_obj = compat_urlparse.parse_qs(api_page)

        author = self._html_search_regex(
            r'<!-- 發表作者 -->：[\n ]+<a href="/([a-z]+)"', page, 'author')
        mobj = re.search(r'<!-- 發表於 -->(?P<mon>[A-Z][a-z]{2})  ' +
                         r'(?P<day>\d{1,2}), (?P<year>\d{4})', page)
        upload_date = '%s%02d%02d' % (mobj.group('year'),
                                      month_by_abbreviation(mobj.group('mon')),
                                      int(mobj.group('day')))

        return {
            'id': media_id,
            'url': api_result_obj['mp3file'][0],
            'title': self._html_search_meta('description', page),
            'duration': float(api_result_obj['totaltime'][0]) / 1000.0,
            'uploader_id': author,
            'upload_date': upload_date,
        }
