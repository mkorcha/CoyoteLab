# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.synced_folder ".", "/home/vagrant/src"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get autoremove -y
    sudo apt-get update
    sudo apt-get install python-virtualenv python-dev libffi-dev libssl-dev -y
    sudo apt-get install lxd -t trusty-backports -y
    sudo apt-get install postgresql libpq-dev redis-server npm nodejs-legacy -y
    sudo -u postgres psql -c "create database db;"
    sudo -u postgres psql -c "create user dbuser with password 'dbuser';"
    sudo -u postgres psql -c "grant all on database db to dbuser;"
    sudo npm install -g gulp
  SHELL
end
