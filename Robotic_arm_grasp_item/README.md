# UR5e Grasping with MuJoCo

Single-file implementation of a UR5e robot performing a grasping task using
**Jacobian-based differential IK** and a **Robotiq 2F-85 gripper** in MuJoCo.

This project demonstrates:
- End-effector pose tracking with operational space control  
- Gripper actuation using a tendon-driven model  
- Object grasping and lifting  
- UR5e + Gripper + Gelsight fingertip simulation in MuJoCo  

---

# Before running this project, you need to place the folder of this project in the path of Ubuntu:
# ~/Robotic_arm_grasp_item

# Installation（base on WSL Ubantu 24.04.1）
cd ~/Robotic_arm_grasp_item
sudo apt update

# Load Environment
sudo apt install python3-venv python3-pip -y
python3 -m venv mj_env
source mj_env/bin/activate

# Install of mujoco
pip install mujoco==3.1.0
pip install mujoco-python-viewer
pip install numpy

# To Run The Code(In the terminal)
python3 Grasp.py

# The MuJoCo viewer will automaticly open in few seconds after you run the code