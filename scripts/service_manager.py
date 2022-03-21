#!/usr/bin/env python3

import rospy
import rosnode
from std_srvs.srv import Trigger, TriggerResponse

import os
import subprocess


class ServiceManager():
    def __init__(self):
        node_names = []

        self.start_recording_service = rospy.Service('/data_recording/start_recording', Trigger, self.start_recording)
        self.stop_recording_service = rospy.Service('/data_recording/stop_recording', Trigger, self.stop_recording)
        self.stop_recording_service = rospy.Service('/data_recording/toggle_recording', Trigger, self.toggle_recording)

        self.launch_recording_service = rospy.Service('/service_management/launch_recording', Trigger, self.launch_recording)
        self.launch_xsens_service = rospy.Service('/service_management/launch_xsens', Trigger, self.launch_xsens)
        self.launch_cameras_service = rospy.Service('/service_management/launch_cameras', Trigger, self.launch_cameras)
        self.launch_mars_service = rospy.Service('/service_management/launch_mars', Trigger, self.launch_mars)
        self.launch_rviz_service = rospy.Service('/service_management/launch_rviz', Trigger, self.launch_rviz)
        self.launch_all_service = rospy.Service('/service_management/launch_all', Trigger, self.launch_all)

        self.launch_tf_listener_service = rospy.Service('/service_management/launch_tf_listener', Trigger, self.launch_tf_listener)


        self.end_recording_service = rospy.Service('/service_management/end_recording', Trigger, self.end_recording)
        self.launch_shutdown_all_nodes_service = rospy.Service('/service_management/shutdown_all', Trigger, self.shutdown_all)
        self.launch_kill_master_service = rospy.Service('/service_management/kill_rosmaster', Trigger, self.kill_rosmaster)


        self.process = None
        self.recording = False

#        self.output_directory = rospy.get_param('/data_recording/output_directory', '~/rosbag/')
        self.output_directory = rospy.get_param('/data_recording/output_directory', '')


        self.topics = rospy.get_param('/data_recording/topics', [])
        if not self.topics:
            rospy.logerr('No Topics Specified.')

#        self.command = ['rosrun', 'rosbag', 'record', '-e'] + self.topics + ['__name:=data_recording_myrecorder']
        self.command = []

        rospy.loginfo('Data Recorder Started')



    def launch_recording(self, req):
        self.command = ["roslaunch", "mars", "launch_recording.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started Recording, PID %s' % self.process.pid)


    def launch_xsens(self, req):
        self.command = ["roslaunch", "mars", "launch_xsens.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started Xsens, PID %s' % self.process.pid)


    def launch_cameras(self, req):
        self.command = ["roslaunch", "mars", "launch_cameras.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started Cameras, PID %s' % self.process.pid)


    def launch_mars(self, req):
        self.command = ["roslaunch", "mars", "launch_mars.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started Mars, PID %s' % self.process.pid)


    def launch_rviz(self, req):
        self.command = ["roslaunch", "mars", "launch_rviz.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started Rviz, PID %s' % self.process.pid)


    def launch_tf_listener(self, req):
        self.command = ["roslaunch", "mars", "launch_tf_listener.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started TF Listener, PID %s' % self.process.pid)


    def launch_all(self, req):
        self.command = ["roslaunch", "mars", "launch_all.launch"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started All, PID %s' % self.process.pid)


    def end_recording(self, req):
        rosnode.kill_nodes(['/record_node'])
        return TriggerResponse(True, 'Recording Ends')


    def shutdown_all(self, req):
        self.command = ["rosnode", "kill", "--all"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Started All, PID %s' % self.process.pid)


    def kill_rosmaster(self, req):
        self.command = ["killall", "-9", "rosmaster"]
        self.process = subprocess.Popen(self.command)
        return TriggerResponse(True, 'Killed roscore, PID %s' % self.process.pid)



    def toggle_recording(self, req):
        if self.recording:
            return self.stop_recording(req)
        else:
            return self.start_recording(req)

    def start_recording(self, req):
        if self.recording:
            rospy.logerr('Already Recording')
            return TriggerResponse(False, 'Already Recording')

        self.process = subprocess.Popen(self.command, cwd=self.output_directory)        
        self.recording = True
        rospy.loginfo('Started recorder, PID %s' % self.process.pid)
        return TriggerResponse(True, 'Started recorder, PID %s' % self.process.pid)

    def stop_recording(self, req):
        if not self.recording:
            rospy.logerr('Not Recording')
            return TriggerResponse(False, 'Not Recording')

        rosnode.kill_nodes(['/data_recording_myrecorder'])

        self.process = None
        self.recording = False

        rospy.loginfo('Stopped Recording')
        return TriggerResponse(True, 'Stopped Recording')

if __name__ == "__main__":
    rospy.init_node('service_management_node')
    ServiceManager()
    rospy.spin()


