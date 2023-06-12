# Class octoprintpi::yq
#
# Manage yq
class octoprintpi::yq () {
  archive { '/usr/local/bin/yq.tar.gz':
    ensure        => present,
    extract       => true,
    extract_path  => '/tmp',
    source        => 'https://github.com/mikefarah/yq/releases/download/v4.34.1/yq_linux_arm64.tar.gz',
    checksum      => 'e43d788ca14c9bd949ed1c828d6073a6b42d8c78c9e454095699b1a1e844abf2',
    checksum_type => 'sha256',
    creates       => '/usr/local/bin/yq',
    cleanup       => true,
    provider      => 'wget',
  }
  -> file {'/usr/local/bin/yq':
    owner => 'root',
    group => 'root',
    mode  => '0755',
  }
}
