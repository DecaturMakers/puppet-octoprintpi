# Class octoprintpi
#
# Manage a Raspberry Pi for OctoPrint and related things
class octoprintpi (
  String $octoprint_version = '1.9.0',
  String $octoprint_user = 'pi',
) {

  $packages = [
    # base packages present in OctoPi
    'libraspberrypi-bin', # Raspberry Pi VideoCore IV utilities
    'rpi.gpio-common', # Python RPi.GPIO
    # pacakges from OctoPi start_chroot_script
    'avahi-daemon',
    'cmake-data',
    'cmake',
    'git',
    'iputils-ping',
    'libatlas3-base',
    'libavahi-compat-libdnssd1',
    'libffi-dev',
    'libssl-dev',
    'python3-dev',
    'python3',
    'screen',
    'subversion',
    'unzip',
    'avrdude',
  ]

  package { $packages:
    ensure => present,
  }
  -> class {'octoprintpi::octoprint':
    user    => $octoprint_user,
    version => $octoprint_version,
  }
  -> class {'octoprintpi::mjpgstreamer': }
  -> class {'octoprintpi::haproxy': }
  -> class {'octoprintpi::yq': }
  -> file {'/etc/rc.local':
    ensure => present,
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
    source => 'puppet:///modules/octoprintpi/rc.local',
  }
  -> service {'networkcheck.timer':
    enable => true,
  }

}
