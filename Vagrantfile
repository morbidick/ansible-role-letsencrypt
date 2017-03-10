VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "letsencrypt", primary: true do |host|
    host.vm.box = "ubuntu/trusty64"

    host.vm.provision :ansible do |ansible|
      ansible.sudo = true
      ansible.playbook = "tests/role.yml"
    end
  end

end
