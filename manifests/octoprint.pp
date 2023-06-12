# Class octoprintpi::octoprint
#
# Manage OctoPrint itself
class octoprintpi::octoprint (
  String $version,
  String $user = 'pi',
) {

  $version_pattern = regsubst($version, '^\.', '\.')
  $grep_regex = "^OctoPrint==${version_pattern}$"

  exec {'make-virtualenv':
    command => '/usr/bin/python3 -mvenv oprint',
    user    => $user,
    cwd     => "/home/${user}",
    creates => "/home/${user}/oprint/bin/python",
  }
  -> exec {'upgrade-pip':
    command     => "/home/${user}/oprint/bin/pip install --upgrade pip",
    user        => $user,
    cwd         => "/home/${user}/oprint/bin",
    refreshonly => true,
    subscribe   => Exec['make-virtualenv'],
  }
  -> exec {'install-octoprint':
    command => "/home/${user}/oprint/bin/pip install OctoPrint==${version}",
    user    => $user,
    cwd     => "/home/${user}/oprint/bin",
    unless  => "/home/${user}/oprint/bin/pip freeze | /usr/bin/grep -i -e '${grep_regex}'"
  }
  fail('need to enable octoprint.service')

}
