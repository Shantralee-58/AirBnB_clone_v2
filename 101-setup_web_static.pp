# Ensure Apache is installed
package { 'apache2':
  ensure => present,
}

# Create the web_static directory
file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Create the necessary directories
file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

# Create a simple index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html><head></head><body>Holberton School</body></html>',
}

# Ensure ownership and permissions are set
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Ensure Apache is running
service { 'apache2':
  ensure    => running,
  enable    => true,
  require   => Package['apache2'],
  subscribe => File['/data/web_static/releases/test/index.html'],
}
