#ifndef HUMANDISTANCECALCULATION_H
#define HUMANDISTANCECALCULATION_H

#include <iostream>
#include <stdlib.h>
#include <iomanip>
#include <vector>
#include <float.h>
#include <limits.h>
#include <algorithm>
#include <string>
#include <mutex> 

#include <Eigen/Eigen>
#include <Eigen/Core>


#include <fcl/narrowphase/collision_object.h>
#include <fcl/narrowphase/distance.h>
#include <fcl/narrowphase/distance_request.h>
#include <fcl/narrowphase/distance_result.h>
#include <fcl/math/constants.h>
#include <fcl/narrowphase/collision.h>

#include <RobotRepresentation.h>
#include <Human.h>

//for nuitrack
#include <nuitrack/Nuitrack.h>

#include <visualization_msgs/Marker.h>
#include "ros/ros.h"
#include "ros/console.h"


using namespace std;

namespace RVServiceTool_OHT{

class HumanDistanceCalculation { 
	private:

		RobotRepresentation* robotRepresentation;
		vector<Human> humans;
		std::string camera_depth_frame_;
		tf::StampedTransform camera_transform;
		
		
		double inc;
		double reso;
		
		
		int arr[4]= {2,4,6,8};
		std::vector<double> minDistances_all;
		
		ros::Publisher marker_pub_;
		ros::NodeHandle nh_;
		
		tdv::nuitrack::SkeletonTracker::Ptr _skeletonTracker;
		tdv::nuitrack::UserTracker::Ptr _userTracker;
		tdv::nuitrack::IssuesData::Ptr _issuesData;
		
		uint64_t _onIssuesUpdateHandler;
		bool _isInitialized;

		/**
		 * Nuitrack callbacks
		 */
		
		void onSkeletonUpdate(tdv::nuitrack::SkeletonData::Ptr userSkeletons);
		void onIssuesUpdate(tdv::nuitrack::IssuesData::Ptr issuesData);
		void onNewUser(int id);
		void onLostUser (int id);
		
		//calculation distances for six robot cylinder
		void calculateMinDistances(Human *it);
		double getDistance(const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2);	
		Eigen::Quaterniond calculate_q (const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2);
		std::vector<double> getMiddlePoint(const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2);
	
		void PublishCylinderMarker(int id, float x, float y, float z, float color_r, float color_g, float color_b, float d , Eigen::Quaterniond q, int i);
		
		//void visualizeDistances(Human* it);
	  
		void writeSkeletonJoints(Human *it);
		
		
 
  	public:
	
		HumanDistanceCalculation(RobotRepresentation* robotRepresentation, std::string camera_depth_frame_, tf::StampedTransform camera_transform_);
		~HumanDistanceCalculation();
	
		// Initialize sample: initialize Nuitrack, create all required modules,
		// register callbacks and start Nuitrack
		void init(const std::string& config = "");
	
		// Update the depth map, tracking and gesture recognition data,
		// then redraw the view
		bool update();
	
		// Release all resources
		void release();
		
		vector<Human> getHumans();
		void setHumans(std::vector<Human> h);
		
		//for marker clear 
		visualization_msgs::Marker markerD;
		
		
		std::vector<double> getMinDistances_all();
		fcl::Vector3<double> minDistP1_all[4];
		fcl::Vector3<double> minDistP2_all[4];
		
		ros::Publisher cylinder_pub;
		
		


};

}

#endif
