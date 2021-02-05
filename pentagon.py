#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
PI = 3.141592653589793238462643383279 

x=0
y=0
theta=0


def posecallback(pose_message):
	global x
	global y
	global theta
	x = pose_message.x
	y = pose_message.y
	theta = pose_message.theta
	
	
def move(speed, distance):
	velocity_message = Twist()
	global x, y
	x0 = x
	y0 = y
	
	velocity_message.linear.x = abs(int(speed))
	distance_moved = 0.0
	loop_rate = rospy.Rate(10)
	cmd_vel_topic = '/turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	
	while True:
		rospy.loginfo("Turlesim moves forwards")
		velocity_publisher.publish(velocity_message)
		
		loop_rate.sleep()
		
		distance_moved = distance_moved + abs( math.sqrt(((x-x0)**2) + ((y-y0)**2)))
		if not (distance_moved < distance):
			rospy.loginfo("reached")
			break
	velocity_message.linear.x =0
	velocity_publisher.publish(velocity_message)

def rotate(speed,angle):
	#Starts a new node
	velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()
	#Converting from angles to radians
	angular_speed = speed*PI/180
	relative_angle =angle*PI/180

	#We wont use linear components
	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0

	# Checking if our movement is CW or CCW
	vel_msg.angular.z = abs(angular_speed)
	# Setting the current time for distance calculus
	t0 = rospy.Time.now().to_sec()
	current_angle = 0
	loop_rate = rospy.Rate(10)
	    
	while True:
		rospy.loginfo("Turtlesim rotates")
		velocity_publisher.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)
		loop_rate.sleep()
	
		if (current_angle > relative_angle):
			rospy.loginfo("reached")
			break	


	#Forcing our robot to stop
	vel_msg.angular.z = 0
	velocity_publisher.publish(vel_msg)
	
def pentagonPath():
	move(2,8)
	rotate(40,68)
	move(2,8)
	rotate(30,68)
	move(2,8)
	rotate(30,68)
	move(2,8)
	rotate(30,68)
	move(2,8)
	rotate(30,68)
	
	
	
	
if __name__ == '__main__':
	try:
		rospy.init_node('turtlesim_motion_pose', anonymous = True)
		
		cmd_vel_topic ='turtle1/cmd_vel'
		velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)
		
		position_topic = 'turtle1/pose'
		pose_subscriber = rospy.Subscriber(position_topic, Pose, posecallback)
		time.sleep(2)
		
		pentagonPath()
		
	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated")
