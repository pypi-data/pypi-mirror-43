# kube-provision

### Design Principles

* **Stateless** - Do not require the pre-population of inventory files with IP/Hostsname.
* **Self Contained** - Do not require any external depdenencies likes load balancers
* **Multi-Target** - Support multiple target environments including vSphere and VMWare Fusion
* **UNIX Philosophy** - Use small components that do 1 thing and do it well.

## Getting Started

**install kube-provision**

```bash
pip install kube-provision
```

**configure the provisioner**

*config.yml*

```yaml
os: ubuntu
consul_bind_interface: ens33
target: vmware-fusion
template: /Users/home/Virtual Machines.localized/ubuntu_base.vmwarevm/ubuntu_base.vmx
vm_dir: /Users/home/Virtual Machines.localized/
```

See [ansible-provision](www.moshloop.com/ansible-provision) to see how to configure provisioners for different targets.

**create a base image with kubeadm**

Install kubeadm and a container runtime as per [install kubeadm](https://kubernetes.io/docs/setup/independent/install-kubeadm/)

[bake.yml](https://github.com/moshloop/kube-provision/blob/master/bake.yml) is an ansible playbook that automates this process.

**provision a new cluster** (automatically creates a new consul server)

```bash
kube-provision --config config.yml --masters 3 --workers 3 --name cluster-name
```

**provision a new cluster** (with an existing consul cluster)

```bash
kube-provision --config config.yml --masters 3 --workers 3 --name cluster-name --consul-ip=10.200.200.1
```

## Architecture

![](architecture.png)

***consul***

An externally hosted consul server/cluster is used for service discovery of kubernetes masters. Each master runs a consul agent that registers as a service endpoint for the cluster. If not specified at runtime a new consul server will be provisioned before proceeding with kubernetes.

***etcd***

Etcd nodes are run stacked with the master nodes, that is each api-server talks only with it’s local etcd node and the etcd nodes are joined to the “primary master” and then discover each other. Should the primary master fail, then new masters can be joined by specifying any other master.

***worker node***

All worker nodes run an instance of nginx that listens on <https://localhost:8443> that watches for changes in consul to the registered masters and updates the *nginx.conf* to reload the config as needed.

**ansible-deploy**

`ansible-deploy` is used to create the boot script based upon templated commands and files with the *cloud-init* deployment target.

**ansible-provision**

`ansible-provision` is used to provision consul and the kubernetes nodes to any supported target.