# Class octoprintpi::haproxy
#
# Manage haproxy
class octoprintpi::haproxy () {

  package {['ssl-cert', 'haproxy']:
    ensure => present,
  }
  -> file {['/etc/ssl/private/ssl-cert-snakeoil.key', '/etc/ssl/certs/ssl-cert-snakeoil.pem']:
    ensure => absent,
  }
  -> file {'/etc/haproxy/haproxy.cfg':
    ensure => present,
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
    source => 'puppet:///modules/octoprintpi/haproxy/haproxy.cfg',
  }
  -> service {'gencert.service':
    enable => true,
  }

}
