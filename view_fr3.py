from pathlib import Path

import mujoco
import mujoco.viewer


scene = Path(__file__).parent / "scene_fr3_hand.xml"
model = mujoco.MjModel.from_xml_path(str(scene))
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, 0)
mujoco.mj_forward(model, data)
mujoco.viewer.launch(model=model, data=data)
