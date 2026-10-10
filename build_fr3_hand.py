from pathlib import Path
from copy import deepcopy
import xml.etree.ElementTree as ET

base = Path(__file__).resolve().parent
repo = base / 'mujoco_menagerie'
fr3 = ET.parse(repo / 'franka_fr3/fr3.xml').getroot()
panda = ET.parse(repo / 'franka_emika_panda/panda.xml').getroot()
fr3.set('model', 'FR3 with Franka Hand')
fr3.find('compiler').attrib.pop('meshdir', None)
for mesh in fr3.findall('asset/mesh'):
    mesh.set('file', 'mujoco_menagerie/franka_fr3/assets/' + mesh.get('file'))
hand = deepcopy(panda.find(".//body[@name='hand']"))
hand.set('childclass', 'panda')
defaults = deepcopy(panda.find("default/default[@class='panda']"))
materials = {e.get('material') for e in hand.iter() if e.get('material')}
meshes = {e.get('mesh') for e in hand.iter() if e.get('mesh')}
for tree in [hand, defaults]:
    for e in tree.iter():
        for attr in ['class', 'childclass']:
            if e.get(attr):
                e.set(attr, 'hand_' + e.get(attr))
        for attr in ['mesh', 'material']:
            if e.get(attr):
                e.set(attr, 'hand_' + e.get(attr))
fr3.find('default').append(defaults)
for e in panda.find('asset'):
    name = e.get('name') or Path(e.get('file', '')).stem
    if (e.tag == 'mesh' and name in meshes) or (e.tag == 'material' and name in materials):
        asset = deepcopy(e)
        asset.set('name', 'hand_' + name)
        if asset.get('class'):
            asset.set('class', 'hand_' + asset.get('class'))
        if asset.get('file'):
            asset.set('file', 'mujoco_menagerie/franka_emika_panda/assets/' + asset.get('file'))
        fr3.find('asset').append(asset)
fr3.find(".//body[@name='fr3_link7']").append(hand)
for tag in ['tendon', 'equality']:
    fr3.append(deepcopy(panda.find(tag)))
actuator = deepcopy(panda.find("actuator/general[@name='actuator8']"))
actuator.set('class', 'hand_panda')
actuator.set('name', 'hand_open_close')
fr3.find('actuator').append(actuator)
key = fr3.find('keyframe/key')
key.set('qpos', key.get('qpos') + ' 0.04 0.04')
key.set('ctrl', key.get('ctrl') + ' 255')
ET.indent(fr3)
ET.ElementTree(fr3).write(base / 'fr3_hand.xml', encoding='unicode')
scene = ET.parse(repo / 'franka_fr3/scene.xml').getroot()
scene.set('model', 'FR3 with Franka Hand')
scene.find('include').set('file', 'fr3_hand.xml')
ET.indent(scene)
ET.ElementTree(scene).write(base / 'scene_fr3_hand.xml', encoding='unicode')
