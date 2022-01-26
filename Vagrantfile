# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provision :shell, path: "Vagrant-setup/bootstrap.sh"
  config.vm.provider "virtualbox" do |v|
      v.name = "SudoCool"
  end
  config.vm.network :forwarded_port, host: 18090, guest: 80
  config.vm.network :forwarded_port, host: 8090, guest: 8000
  config.vm.network :forwarded_port, host: 15432, guest: 5432
  config.vm.network :forwarded_port, host: 35729, guest: 35729
end
