import os
import unittest

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch

from dem.GitProjectInstaller import GitProjectInstaller
from dem.cache import PackageCache


class MyTestCase(unittest.TestCase):

    @patch('git.Repo.clone_from')
    def test_will_not_install_git_project_if_already_installed(self, mock_git):
        cache = MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = True
        packages = [{'name': 'package', 'version': '1.3.0', 'url': 'http://github.com/nitehawck/dem'},
                    {'name': 'package4', 'version': '0.3.0', 'url': 'http://github.com/nitehawck/dem'}]
        installer = GitProjectInstaller(packages, cache)
        installer.install_packages()

        mock_git.assert_not_called()

    @patch('git.Repo.clone_from')
    def test_will_clone_project_if_not_installed(self, mock_git):
        cache = MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = False

        package1_location = os.path.join('path', 'package')
        package2_location = os.path.join('path2', 'package4')
        repo1 = MagicMock()
        repo2 = MagicMock()

        def clone_from(url, location):
            if location == package1_location:
                return repo1
            return repo2

        mock_git.side_effect = clone_from

        packages = [{'name': 'package', 'version': '1.3.0', 'platform-destination-path': 'path', 'url': 'http://github.com/nitehawck/dem'},
                    {'name': 'package4', 'version': '0.3.0', 'platform-destination-path': 'path2', 'url': 'http://github.com/nitehawck/dem'}]

        installer = GitProjectInstaller(packages, cache)
        installer.install_packages()

        mock_git.assert_any_call('http://github.com/nitehawck/dem', package1_location)
        mock_git.assert_any_call('http://github.com/nitehawck/dem', package2_location)
        repo1.checkout.assert_any_call('1.3.0')
        repo2.checkout.assert_any_call('0.3.0')

    @patch('git.Repo.clone_from')
    def test_will_use_master_when_version_not_known(self, mock_git):
        cache = MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = False

        package1_location = os.path.join('path', 'package')
        repo1 = MagicMock()

        mock_git.return_value = repo1

        packages = [{'name': 'package',  'platform-destination-path': 'path', 'url': 'http://github.com/nitehawck/dem'}]

        installer = GitProjectInstaller(packages, cache)
        installer.install_packages()

        mock_git.assert_any_call('http://github.com/nitehawck/dem', package1_location)
        repo1.checkout.assert_any_call('master')

    @patch('git.Repo.clone_from')
    def test_will_return_when_url_missing(self, mock_git):
        cache = MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = False
        repo1 = MagicMock()
        repo2 = MagicMock()

        def clone_from(url, location):
            if location == os.path.join('path', 'package'):
                return repo1
            return repo2

        mock_git.side_effect = clone_from

        packages = [{'name': 'package', 'platform-destination-path': 'path', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0', 'platform-destination-path': 'path2', 'url': 'http://github.com/nitehawck/dem'}]

        installer = GitProjectInstaller(packages, cache)
        installer.install_packages()

        mock_git.assert_any_call('http://github.com/nitehawck/dem', os.path.join('path2', 'package4'))
        repo2.checkout.assert_any_call('0.3.0')


if __name__ == '__main__':
    unittest.main()
