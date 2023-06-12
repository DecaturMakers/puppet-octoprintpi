# Class octoprintpi::mjpgstreamer
#
# Manage MJPGstreamer
class octoprintpi::mjpgstreamer () {

  $packages = [
    'libjpeg62-turbo-dev',
    'imagemagick',
    'ffmpeg',
    'libv4l-dev',
  ]

  if ($facts['os']['name'] == 'Debian' and $facts['os']['release']['major'] == '11' and $facts['os']['hardware'] == 'aarch64') {
    $source_dir = 'Debian11-aarch64'
  } else {
    fail("ERROR: mjpgstreamer unsupported on ${facts['os']['name']} ${facts['os']['release']['major']} on arch ${facts['os']['hardware']}")
  }

  package { $packages:
    ensure => present,
  }
  -> file {'/opt/mjpg-streamer':
    ensure  => directory,
    path    => '/opt/mjpg-streamer',
    source  => "puppet:///modules/octoprintpi/mjpgstreamer/${source_dir}",
    recurse => true,
    owner   => 'root',
    group   => 'root',
    mode    => '0755',
  }
  -> service{'webcamd.service':
    ensure => running,
    enable => true,
  }
  # we're omitting the /home/pi/mjpg_streamer legacy compatibility symlink

}
