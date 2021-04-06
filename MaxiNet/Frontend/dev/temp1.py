import json
import time
from MaxiNet.Frontend import maxinet
from MaxiNet.Frontend.container import Docker
from mininet.topo import Topo
from mininet.node import OVSSwitch

with open("/usr/local/share/MaxiNet/dev/tempVioletfiles/infra-config-new2.json") as f:
    dataConfig = json.load(f)

dataConfig["infra_config"].pop("sensor_types", None)

def get_distribution(dataConfig):
    fog = {}
    for key, value in dataConfig["infra_config"]["devices"].items():
        if key == "Fog":
            fog_temp = list(dataConfig["infra_config"]["devices"]["Fog"].keys())
            for fog_i in fog_temp:
                fog[fog_i] = []
        if key == "Edge":
            edge_temp = list(dataConfig["infra_config"]["devices"]["Edge"].keys())
            for edge_i in edge_temp:
                ed_dom = edge_i.split("-")[1][0]
                fog_str = "Fog-" + ed_dom
                fog[fog_str].append(edge_i)
    return (len(dataConfig["infra_config"]["devices"]["Fog"]), len(dataConfig["infra_config"]["devices"]["Edge"]), fog)

(fog_len, edge_len, config) = get_distribution(dataConfig)

print(config)

# Topology Creation

topo = Topo()

metaFog = {}
metaEdge = {}
metaSwitch = {}

# add a global switch to connect all the fog's public network
print("Creating a Public Newtork")
metaSwitch["global"] = {}
metaSwitch["global"]["id"] = "s0"
metaSwitch["global"]["topo"] = topo.addSwitch(metaSwitch["global"]["id"])
metaSwitch["global"]["bw"] = dataConfig["infra_config"]["public_networks"]["global"]["bw"]
metaSwitch["global"]["latency"] = dataConfig["infra_config"]["public_networks"]["global"]["latency"]+"ms"
print("Public Network Config -> " +  str(metaSwitch["global"]))

for i in range(0, len(list(config.keys()))):
    # AddHost for Fogs
    fog = list(config.keys())[i]
    metaFog[fog] = {}
    metaFog[fog]["ip"] = "10.0.0."+str(i+1)
    metaFog[fog]["topo"] = topo.addHost(fog, cls=Docker, ip=metaFog[fog]["ip"], dimage="ubuntu:trusty")
    print(fog + " created")

    # add a switch for each fog's private network
    print("Creating "+fog+"'s Private Network")
    metaSwitch[fog] = {}
    metaSwitch[fog]["id"] = "s"+str(i+1)
    metaSwitch[fog]["topo"] = topo.addSwitch(metaSwitch[fog]["id"])
    metaSwitch[fog]["bw"] = dataConfig["infra_config"]["private_networks"][fog+"-private"]["bw"]
    metaSwitch[fog]["latency"] = dataConfig["infra_config"]["private_networks"][fog+"-private"]["latency"]+"ms"
    print(fog+"'s Network -> " + str(metaSwitch[fog]))
    
    # add Link to public network
    print("Adding "+fog+" to public network")
    topo.addLink(metaFog[fog]["topo"], metaSwitch["global"]["topo"], bw = metaSwitch["global"]["bw"], delay = metaSwitch["global"]["latency"])
    # add Link to private network
    topo.addLink(metaFog[fog]["topo"], metaSwitch[fog]["topo"], intfName1=fog+"-eth1", params1={'ip':'10.0.2/8'})

    # AddHost for Edges
    print("Creating Edges for "+fog)
    for j in range(0, len(config[fog])):
        edge = config[fog][j]
        metaEdge[edge] = {}
        metaEdge[edge]["ip"] = "10.0.1."+str(j)
        metaEdge[edge]["topo"] = topo.addHost(edge, cls=Docker, ip=metaEdge[edge]["ip"], dimage="ubuntu:trusty")
        print(edge+" created")
        # add Links to private network
        print("Adding "+edge+" to "+fog+"'s private network")
        topo.addLink(metaEdge[edge]["topo"], metaSwitch[fog]["topo"], bw = metaSwitch[fog]["bw"], delay = metaSwitch[fog]["latency"])



cluster = maxinet.Cluster()
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

try:
    print("Waiting 3 secs to converge")
    time.sleep(3)
    
    # Re-initailize fog's public connections
    print(metaFog)
    print(metaEdge)
    for fog in metaFog:
        strg = "ifconfig"+" "+fog+"-eth0"+" "+metaFog[fog]["ip"]+" "+"netmask 255.255.255.0"
        exp.get_node(fog).cmd(strg)

    # see configs
   # print(exp.get_node("Fog-1").cmd("ifconfig"))
   # print(exp.get_node("Fog-2").cmd("ifconfig"))
    
    # pings
   # print("Fog-1 -> Fog-2")
   # print(exp.get_node("Fog-1").cmd("ping -c 3 10.0.0.2"))
    
   # print("Edge-1.1 -> Fog-1")
   # print(exp.get_node("Edge-1.1").cmd("ping -c 3 10.0.2.0"))

   # print("Edge-1.2 -> Edge-1.1")
   # print(exp.get_node("Edge-1.2").cmd("ping -c 3 10.0.1.0"))

   # print("Edge-2.1 -> Fog-1")
   # print(exp.get_node("Edge-2.1").cmd("ping -c 3 10.0.0.1"))

   # print("Edge-2.2 -> Edge-2.1")
   # print(exp.get_node("Edge-2.2").cmd("ping -c 3 10.0.1.0"))


    exp.CLI(locals(), globals())
finally:
    exp.stop()




