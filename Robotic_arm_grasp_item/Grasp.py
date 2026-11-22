import mujoco
import mujoco.viewer
import numpy as np
import time
import threading


# Integration timestep in seconds.
integration_dt: float = 1.0
damping: float = 1e-4
gravity_compensation: bool = True
dt: float = 0.002
max_angvel = 0.0
# Set the start point and end point
start_position = np.array([0.5, 0.0, 0.5])
end_position = np.array([0.5, 0.5, 0.2])


def control_gripper(open_gripper):
    """Control gripper opening/closing"""
    global data, gripper_actuator_id  # Ensure correct variable scope
    if gripper_actuator_id is not None:
        position = 0 if open_gripper else 255   # 0 = open, 255 = closed
        data.ctrl[gripper_actuator_id] = position
        print(f"Gripper {'Opened' if open_gripper else 'Closed'}")
    else:
        print("Warning: Cannot control gripper, gripper_actuator_id is None.")



def main() -> None:
    assert mujoco.__version__ >= "3.1.0", "Please upgrade to mujoco 3.1.0 or later."

    # Load the model
    model = mujoco.MjModel.from_xml_path("universal_robots_ur5e/scene2.xml")
    data = mujoco.MjData(model)


    # Define the simulation time step
    model.opt.timestep = dt

    site_id = model.site("attachment_site").id

    # Get the ID of the mocap site
    try:
        mocap_id = model.body("target").mocapid[0]
        print(f"Detected mocap target ID: {mocap_id}")
    except KeyError:
        print("Error: Mocap target 'target' not found in model!")
        return

    body_names = [
        "shoulder_link", "upper_arm_link", "forearm_link", "wrist_1_link",
        "wrist_2_link", "wrist_3_link", "base_gripper", "left_driver",
        "left_coupler", "left_spring_link", "left_follower", "left_pad",
        "gelsight_left", "tongue_left", "right_driver", "right_coupler",
        "right_spring_link", "right_follower", "right_pad", "tongue_right", "gelsight_right",
        "cup"
    ]
    body_ids = [model.body(name).id for name in body_names]
    if gravity_compensation:
        model.body_gravcomp[body_ids] = 1.0

    # Get the ID of the actuator for the Robotic arm
    joint_names = ["shoulder_pan", "shoulder_lift", "elbow", "wrist_1", "wrist_2", "wrist_3"]
    dof_ids = np.array([model.joint(name).id for name in joint_names])
    actuator_ids = np.array([model.actuator(name).id for name in joint_names])

    # Get the ID of the actuator for the Gripper
    actuator_names = [
        model.names[model.name_actuatoradr[i]:].split(b"\x00", 1)[0].decode("utf-8")
        for i in range(model.nu)
    ]
    gripper_actuator_id = None
    for i, actuator in enumerate(actuator_names):
        if actuator == "fingers_actuator":
            gripper_actuator_id = i
            print(f"Detected gripper actuator: {actuator} (ID: {gripper_actuator_id})")
            break

    # Define the gripper control function
    def control_gripper(position):
        if gripper_actuator_id is not None:
            position = max(0, min(255, position))  # Range of 0-255
            data.ctrl[gripper_actuator_id] = position
            print(f"Gripper position set to {position}")
        else:
            print("Warning: Cannot control gripper, gripper_actuator_id is None.")

    #Define the circle function
    def circle(t: float, r: float, h: float, k: float, f: float) -> np.ndarray:
         x = r * np.cos(2 * np.pi * f * t) + h
         y = r * np.sin(2 * np.pi * f * t) + k
         return np.array([x, y])

    

    waypoints = [
        np.array([0.5, 0.0, 0.2]),
        np.array([0.5, 0.0, 0.2]),  # Start Moving
        np.array([0.5, 0.0, 0.3]),  
        np.array([0.5, 0.0, 0.4]),  
        np.array([0.5, 0.0, 0.5]),
        np.array([0.5, 0.2, 0.5]),
        np.array([0.2, 0.4, 0.4]),
        np.array([0.2, 0.4, 0.2]),  # Final 
    ]

    move_duration = 3.0  # Each move duration
    gripper_hold_time = 0.5  # Gripper close time
    current_waypoint = 0  # Movement index
    start_time = time.time()
    movement_stage = 0  # 0: Moving, 1: Gripper Close, 2: Continue moving    # Define motion waypoints

    with mujoco.viewer.launch_passive(model=model, data=data, show_left_ui=False, show_right_ui=False) as viewer:
        
        mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)
        mujoco.mjv_defaultFreeCamera(model, viewer.cam)
        viewer.opt.frame = mujoco.mjtFrame.mjFRAME_SITE

        # Gripper opening/closing
        gripper_open = True

        while viewer.is_running():
            step_start = time.time()

            # Set the mocap target position
            #data.mocap_pos[mocap_id, 0:2] = circle(data.time, 0.1, 0.5, 0.0, 0.5)
            #data.mocap_pos[mocap_id] = np.array([0.5, 0.0, 0.5])
    # Calculate the time elapsed since the start of the movement
            elapsed_time = time.time() - start_time
            t = min(1.0, elapsed_time / move_duration)  # Limit t from 0 to 1

    # Calculate the target position based on the current waypoint
            # target_position = (1 - t) * start_position + t * end_position
            # data.mocap_pos[mocap_id] = target_position
            # calculate the error position
            # error_pos = data.mocap_pos[mocap_id] - data.site(site_id).xpos
            # site_quat = np.zeros(4)
            # mujoco.mju_mat2Quat(site_quat, data.site(site_id).xmat)
            # site_quat_conj = np.zeros(4)
            # mujoco.mju_negQuat(site_quat_conj, site_quat)
            # error_quat = np.zeros(4)
            # mujoco.mju_mulQuat(error_quat, data.mocap_quat[mocap_id], site_quat_conj)
            # error_ori = np.zeros(3)
            # mujoco.mju_quat2Vel(error_ori, error_quat, 1.0)
            # start_pos = waypoints[current_waypoint]

            if current_waypoint < len(waypoints):
                start_pos = waypoints[current_waypoint]
            else:
                start_pos = waypoints[-1] 

            if current_waypoint + 1 < len(waypoints):
                end_pos = waypoints[current_waypoint + 1]
            else:
                end_pos = waypoints[-1]  #Saty at the last position
            target_position = (1 - t) * start_pos + t * end_pos

                # **Update mocap target position**
            data.mocap_pos[mocap_id] = target_position

                # **Compute control input using Jacobian**
            error_pos = data.mocap_pos[mocap_id] - data.site(site_id).xpos

                # **Compute orientation error**
            site_quat = np.zeros(4)
            mujoco.mju_mat2Quat(site_quat, data.site(site_id).xmat)

            site_quat_conj = np.zeros(4)
            mujoco.mju_negQuat(site_quat_conj, site_quat)

            error_quat = np.zeros(4)
            mujoco.mju_mulQuat(error_quat, data.mocap_quat[mocap_id], site_quat_conj)

            error_ori = np.zeros(3)
            mujoco.mju_quat2Vel(error_ori, error_quat, 1.0)
            #Calculate the Jacobian matrix
            jac = np.zeros((6, model.nv))
            mujoco.mj_jacSite(model, data, jac[:3], jac[3:], site_id)

            # Solve the governing equation： J @ dq = error**
            dq = jac.T @ np.linalg.solve(jac @ jac.T + damping * np.eye(6), np.hstack([error_pos, error_ori]))

            # Limit the maximum joint velocity
            if max_angvel > 0:
                dq_abs_max = np.abs(dq).max()
                if dq_abs_max > max_angvel:
                    dq *= max_angvel / dq_abs_max

            # Integral computes the joint positions
            q = data.qpos.copy()
            mujoco.mj_integratePos(model, q, dq, integration_dt)
            np.clip(q, *model.jnt_range.T, out=q)
            data.ctrl[actuator_ids] = q[dof_ids]
        
            if t == 1.0:
                print(f"Reached {end_pos}")

                if current_waypoint == 0:  # **Reached gripping position**
                    print("Closing gripper")
                    control_gripper(255)
                    movement_stage = 1  # Switch to gripper closing stage
                    start_time = time.time()
                else:
                    current_waypoint += 1  # Move to next waypoint
                    start_time = time.time()

            elif movement_stage == 1:  # **Gripper close wait time**
                if time.time() - start_time > gripper_hold_time:
                    print("Gripper closed, continuing movement")
                    movement_stage = 0  # Resume movement
                    current_waypoint += 1  # Move to next waypoint
                    start_time = time.time()
 
        # Close the gripper after the motion is complete
            # if not movement_complete and t == 1.0:
            #   control_gripper(255)  # Gripper closed
            #   movement_complete = True    
              
              
        # simulation step
            mujoco.mj_step(model, data)
            viewer.sync()

        
            time_until_next_step = dt - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

if __name__ == "__main__":
    main()



