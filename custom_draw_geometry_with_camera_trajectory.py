import os
from open3d import *
import numpy as np
import matplotlib.pyplot as plt

def custom_draw_geometry_with_camera_trajectory(pcd):
    custom_draw_geometry_with_camera_trajectory.index = -1
    custom_draw_geometry_with_camera_trajectory.trajectory =\
            read_pinhole_camera_trajectory(
                    "camera_trajectory.json")
    custom_draw_geometry_with_camera_trajectory.vis = Visualizer()
    if not os.path.exists("image/"):
        os.makedirs("image")
    if not os.path.exists("depth/"):
        os.makedirs("depth")
    def move_forward(vis):
        # This function is called within the Visualizer::run() loop
        # The run loop calls the function, then re-render
        # So the sequence in this function is to:
        # 1. Capture frame
        # 2. index++, check ending criteria
        # 3. Set camera
        # 4. (Re-render)
        ctr = vis.get_view_control()
        glb = custom_draw_geometry_with_camera_trajectory
        if glb.index >= 0:
            print("Capture image {:05d}".format(glb.index))
            depth = vis.capture_depth_float_buffer(False)
            image = vis.capture_screen_float_buffer(False)
            plt.imsave("depth/{:05d}.png".format(glb.index),\
                    np.asarray(depth), dpi = 1)
            plt.imsave("image/{:05d}.png".format(glb.index),\
                    np.asarray(image), dpi = 1)
            #vis.capture_depth_image("depth/{:05d}.png".format(glb.index), False)
            #vis.capture_screen_image("image/{:05d}.png".format(glb.index), False)
        glb.index = glb.index + 1
        if glb.index < len(glb.trajectory.extrinsic):
            ctr.convert_from_pinhole_camera_parameters(glb.trajectory.intrinsic,\
                    glb.trajectory.extrinsic[glb.index])
        else:
            custom_draw_geometry_with_camera_trajectory.vis.\
                    register_animation_callback(None)
        return False
    vis = custom_draw_geometry_with_camera_trajectory.vis
    vis.create_window(width = 852, height = 480)
    vis.add_geometry(pcd)
    vis.get_render_option().load_from_json("renderoption.json")
    vis.register_animation_callback(move_forward)
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    pcd = read_point_cloud("pt1.pcd")
    print("6. Customized visualization playing a camera trajectory")
    custom_draw_geometry_with_camera_trajectory(pcd)
