# Franka FR3 + Franka Hand 的 MuJoCo 仿真

七轴 Franka Research 3 机械臂与双指 Franka Hand 的仿真项目。
支持关节目标位置调节和夹爪开合，目前没有 IK、抓取物体或实机通信。

## 安装和启动

需要 Git、Conda 和可用的桌面 OpenGL。克隆本项目后，在项目目录执行：

```bash
conda create -n mujoco python=3.11 -y
conda activate mujoco
python -m pip install -r requirements.txt
python setup_models.py
bash start_fr3.sh
```

启动脚本使用激活环境的 Python，也可用 `PYTHON=/path/to/python bash start_fr3.sh` 指定。

## 操作

- 空格键：暂停或继续。
- 右侧 Control 面板：调节七个关节目标位置。
- `hand_open_close`：0 关闭，255 打开，中间值为中间开度（不是毫米）；模型最大开口约 80 mm。

启动时使用 home 姿态。仿真参数尚未按用户实物标定。

## 文件

- `scene_fr3_hand.xml`：带地面的入口场景。
- `fr3_hand.xml`：FR3 和 Franka Hand 组合模型。
- `view_fr3.py` / `start_fr3.sh`：启动可视化。
- `setup_models.py`：下载固定版本的上游模型资源。
- `build_fr3_hand.py`：重新生成组合模型和场景。

`mujoco_menagerie/` 是下载的模型依赖，不重复上传网格文件。

## 来源与许可

模型来自 [Google DeepMind MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)，
固定提交为 `0059d4335f8156206f63a35662313385f7ad6d74`。
机械臂使用 `franka_fr3`，夹爪取自 `franka_emika_panda`。
本地组合保留来源模型的惯量、碰撞和双指耦合参数；原模型不修改。
模型及衍生 XML 按 Apache-2.0 许可使用，见 `LICENSE` 和下载模型目录中的许可文件。

## 验证

本机 MuJoCo 3.15.0 下加载成功：9 个位置坐标、8 个执行器。
打开、关闭、重新打开夹爪共运行 4500 步（9 秒），左右手指同步，状态数值有限。
