#!/usr/bin/env python3
"""! @python program for FANUC robot control"""

# Imports
import sys
import time
from robot_controller import robot  # Assuming robot_controller.py is the file you'll use

# Global Constants
drive_path = '172.29.209.124' # Beaker

def main():
    """! Main program entry"""
    
    poses = [
    [39.951130, 477.915497, -195.488892, -176.860321, -7.206623, -149.600830],
    [626.482544, 547.631714, -110.253525, -176.863785, -7.198499, -149.600449],
    [766.152405, 547.874878, -195.896347, -176.863846, -7.199082, -149.600601],
    [65.602791, 11.239730, -47.675983, -182.053009, 50.037930, -33.581284],
    [65.602669, 11.350146, -47.787033, -182.053497, 50.037941, 53.580002],
    [54.799606, 487.345245, -190.487030, 170.929398, -6.502056, -60.910007],
    [478.069550, 454.651367, 320.369904, 99.916443, -53.792107, 76.019188]
    ]

    ## Initiializing Parameters
    # Create new robot object
    crx10 = robot(drive_path)
    
    # Set robot speed
    crx10.set_speed(200)  # Setting speed to 250 mm/sec as in your .tp program
    
    # Start the main loop (Line 2)
    loops = 1
    while(loops <= 1):

        ### 1 ###
        # Home position (set all positions to 1)
        crx10.set_joints_to_home_position()
        # Sync bit and move robot to home position
        crx10.start_robot()
        # Open gripper
        crx10.gripper("open")
        time.sleep(1)

        ### 2 ###
        # Taken care of by the loop

        ### Line 3-7 ###
        crx10.set_pose(poses[0]) # x,y,z,w,p,r
        
        # Sync bit and move robot to first position
        crx10.start_robot()
        time.sleep(1)

        # Close gripper
        crx10.gripper("close") #4
        time.sleep(1)

        # Move and place die
        # Brings the die to a point just above the prox sensors to avoid potential collisions with the robot gripper
        crx10.set_pose(poses[1]) # 5
        crx10.start_robot()
        time.sleep(1)

        # Sets the dice on the conveyer belt
        crx10.set_pose(poses[2]) # 6
        crx10.start_robot()
        time.sleep(1)

        # Place die on conveyor belt by opening the gripper
        crx10.gripper("close") # 7
        time.sleep(1)

        ### 8-16 ###
        # Turn on conveyer belt (see FANUCRegisterDefinitions for more info)
        # R[21] - DO137 for Beaker = forward conveyer. R[22] is reverse
        # R[30] - Converyor right (furthest) prox. sensor - DI139
        crx10.conveyor('forward') # 8

        # Check if the proximity sensor has been tripped
        # NOTE: right_sensor_register = R[31]
        #       left_sensor_register = R[30]
        #       Assume an off sensor returns 0

        while True: # 9-15
            # Read the right proximity sensor
            right_sensor_value = crx10.conveyor_proximity_sensor("right")
    
            # Check if the sensor returns a '1'
            if right_sensor_value == 1:
                break  # Exit the loop
            time.sleep(0.1)
        
        crx10.conveyor('stop') # 16

        ### 17-... ###

        

# Next lines of code to be executed after the sensor returns a '1'
print("Right proximity sensor detected an object!")



        # Start a new loop


    # ... 

if __name__=="__main__":
    main()




