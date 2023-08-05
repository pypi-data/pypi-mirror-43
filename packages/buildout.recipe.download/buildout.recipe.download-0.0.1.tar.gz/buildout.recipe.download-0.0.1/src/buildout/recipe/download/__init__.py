from zc.buildout.download import Download
import zc.buildout.easy_install
import ConfigParser
import multiprocessing as mp
import pkg_resources


__author__ = 'Jagadeesh N Malakannavar <mnjagadeesh@gmail.com>'

ws = ''
dc = ''


def parallel_downloads(urls, idc, iindex, processes):
    global ws
    global dc
    dc = idc
    ws = zc.buildout.easy_install.Installer(dest=idc, index=iindex)
    pool = mp.Pool(int(processes))
    pool.map(func=mp_download, iterable=urls)
    pool.close()


def mp_download(url):
    global ws
    req = pkg_resources.Requirement.parse([url])
    pkg = ws._obtain(req)
    if pkg.location:
        download = Download(cache=dc)
        download(pkg.location)


class Download_eggs():
    def __init__(self, buildout, name, options={}):
        self.url = options.get('pkgurl')
        if not self.url.endswith('/'):
            self.url += '/'
        self.dc = options.get('cache-folder')
        self.files = options.get('files-list')
        self.versions = options.get('versions-files')
        self.ed = options.get('eggs-directory')
        self.index = options.get('index', self.url)
        self.processes = options.get('threads', 50)

    def read_versions(self):
        urls = []
        config = ConfigParser.ConfigParser()
        config.readfp(open(self.versions))
        urls = [[i[0] + '==' + i[1]] for i in config.items('versions')]
        return urls

    def install(self):
        urls = self.read_versions()
        parallel_downloads(urls, self.dc, self.index, self.processes)
        return self.dc

    update = install


if __name__ == '__main__':
    Download_eggs()
