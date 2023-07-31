#include <iostream>
#include <stdlib.h>
#include <iomanip>
#include <vector>
#include <float.h>
#include <limits.h>
#include <algorithm>

//for nuitrack
#include <cstdlib>
#include <cstring>


#include <Eigen/Eigen>
#include <Eigen/Core>


#include <cmath>
#include <tf/transform_broadcaster.h>
#include <tf/transform_datatypes.h>

#include <fcl/narrowphase/collision_object.h>
#include <fcl/narrowphase/distance.h>
#include <fcl/narrowphase/distance_request.h>
#include <fcl/narrowphase/distance_result.h>
#include <fcl/math/constants.h>
#include <fcl/narrowphase/collision.h>
#include <fcl/geometry/octree/octree.h>

#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>
#include <RobotRepresentation.h>
#include <Human.h>
#include <HumanDistanceCalculation.h>

using namespace std;
using namespace fcl;
using namespace RVServiceTool_OHT;
using namespace tdv::nuitrack;

HumanDistanceCalculation::HumanDistanceCalculation(RobotRepresentation* robotRepresentation_, std::string camera_depth_frame, tf::StampedTransform camera_transform_):
	_isInitialized(false)
{
	robotRepresentation = robotRepresentation_;
	camera_depth_frame_ = camera_depth_frame;
	camera_transform = camera_transform_;
	
	marker_pub_ = nh_.advertise<visualization_msgs::Marker>("body_tracker/marker", 1);	
	cylinder_pub = nh_.advertise<visualization_msgs::Marker>("visualization_marker", 1);
	
	markerD.header.frame_id = camera_depth_frame;  
  	markerD.action = visualization_msgs::Marker::DELETEALL;
	
	for(int i = 0; i<4; i++)
	{
		minDistances_all.push_back(DBL_MAX);
	}
	
}

HumanDistanceCalculation::~HumanDistanceCalculation()
{
	try
	{
		Nuitrack::release();
	}
	catch (const Exception& e)
	{
		// Do nothing
	}
}

void HumanDistanceCalculation::init(const std::string& config)
{
	// Initialize Nuitrack first, then create Nuitrack modules
	try
	{
		tdv::nuitrack::Nuitrack::init("");
	}
	catch (const Exception& e)
	{
		std::cerr << "Can not initialize Nuitrack (ExceptionType: " << e.type() << ")" << std::endl;
		exit(EXIT_FAILURE);
	}
	
	
	// Create required Nuitrack modules

	_skeletonTracker = SkeletonTracker::create();
	// Bind to event update skeleton tracker
	//_skeletonTracker->connectOnNewUser(std::bind(&HumanDistanceCalculation::onNewUser, this, std::placeholders::_2));
	//_skeletonTracker->connectOnLostUser(std::bind(&HumanDistanceCalculation::OnLostUser, this, std::placeholders::_2));
	_skeletonTracker->connectOnUpdate(std::bind(&HumanDistanceCalculation::onSkeletonUpdate, this, std::placeholders::_1));

	_skeletonTracker->setNumActiveUsers(6);

	_userTracker = UserTracker::create(); 
	//_userTracker->connectOnNewUser(std::bind(&HumanDistanceCalculation::onNewUser, this, std::placeholders::_1));
	_userTracker->connectOnLostUser(std::bind(&HumanDistanceCalculation::onLostUser, this, std::placeholders::_1));

	_onIssuesUpdateHandler = Nuitrack::connectOnIssuesUpdate(std::bind(&HumanDistanceCalculation::onIssuesUpdate, this, std::placeholders::_1));
}

bool HumanDistanceCalculation::update()
{
	if (!_isInitialized)
	{

		// When Nuitrack modules are created, we need to call Nuitrack::run() to start processing all modules
		try
		{
			tdv::nuitrack::Nuitrack::run();
		}
		catch (const Exception& e)
		{
			std::cerr << "Can not start Nuitrack (ExceptionType: " << e.type() << ")" << std::endl;
			release();
			exit(EXIT_FAILURE);
		}
		_isInitialized = true;
	}
	try
	{
		// Wait and update Nuitrack data
		Nuitrack::waitUpdate(_skeletonTracker);
		
	}
	catch (const LicenseNotAcquiredException& e)
	{
		// Update failed, negative result
		std::cerr << "LicenseNotAcquired exception (ExceptionType: " << e.type() << ")" << std::endl;
		return false;
	}
	catch (const Exception& e)
	{
		// Update failed, negative result
		std::cerr << "Nuitrack update failed (ExceptionType: " << e.type() << ")" << std::endl;
		return false;
	}
	
	return true;
}

void HumanDistanceCalculation::release()
{
	if (_onIssuesUpdateHandler)
		Nuitrack::disconnectOnIssuesUpdate(_onIssuesUpdateHandler);

	// Release Nuitrack and remove all modules
	try
	{
		Nuitrack::release();
	}
	catch (const Exception& e)
	{
		std::cerr << "Nuitrack release failed (ExceptionType: " << e.type() << ")" << std::endl;
	}

	_isInitialized = false;
	
}

// Callback for onLostSkeleton event
void HumanDistanceCalculation::onLostUser(int id)
{
	
	
	visualization_msgs::Marker markerD;
  	markerD.header.frame_id = "odom";  
  	markerD.action = visualization_msgs::Marker::DELETEALL;
 	marker_pub_.publish(markerD); 
 	cylinder_pub.publish(markerD); 
 	
 	for(int i = 0; i<4; i++)
	{
		minDistances_all.push_back(DBL_MAX);
	}
	
}

// Callback for onNewSkeleton event
void HumanDistanceCalculation::onNewUser(int id)
{
	std::cout << "New User " << id << std::endl;
	
	humans.push_back(Human(id));
	
	
}


// Helper function to skeleton data from Nuitrack data
void HumanDistanceCalculation::writeSkeletonJoints(Human *it)
{
	
	std::vector<Joint> joints = it->getJoints();
	
	for(const tdv::nuitrack::Joint& joint : joints)
	{
		std::cout << "/ joint type: " << joint.type << " x: " << float(joint.real.x) << " y: " << float(joint.real.y) << " z: " << float(joint.real.z) << std::endl;

	}

}

// Prepare visualization of skeletons, received from Nuitrack
void HumanDistanceCalculation::onSkeletonUpdate(SkeletonData::Ptr userSkeletons)
{
	int i = 0;
	vector<Human> humans_;
	
	auto skeletons = userSkeletons->getSkeletons();
	for (auto skeleton: skeletons)
	{

		float tracking_confidence = skeleton.joints[JOINT_LEFT_COLLAR].confidence;
		if (tracking_confidence < 0.15)
		{
		    std::cout << "Nuitrack: ID " << skeleton.id << " Low Confidence (" 
		    << tracking_confidence << "), skipping"  << std::endl;
		    continue;  // assume none of the joints are valid 
		}

		
		humans_.push_back(Human(skeleton.id));
		humans_[i].setJoints(skeleton.joints);
		
		i++;

	}
	
	setHumans(humans_);

	
	for(int i = 0; i<4; i++)
	{
		minDistances_all[i]=DBL_MAX;
	}
	
	
	for (int i = 0; i < humans.size(); i++) 
	{

			//writeSkeletonJoints(*it);
			
			calculateMinDistances(&humans[i]);
				
	}
	
	
	
}

void HumanDistanceCalculation::onIssuesUpdate(IssuesData::Ptr issuesData)
{
	_issuesData = issuesData;
}


double HumanDistanceCalculation::getDistance(const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2)
{


  tf::Vector3 point1(j1.real.z/reso, j1.real.x/reso*-1, j1.real.y/reso);
  tf::Vector3 point2(j2.real.z/reso, j2.real.x/reso*-1, j2.real.y/reso);
  
  tf::Vector3 point_bl1 = camera_transform * point1;
  tf::Vector3 point_bl2 = camera_transform * point2;
	
  double d = sqrt(pow(((point_bl2.getX()) - (point_bl1.getX())), 2) +
						pow(((point_bl2.getY()) - (point_bl1.getY())), 2) +
						pow(((point_bl2.getZ()) - (point_bl1.getZ())), 2));
			
  return d;
	
}

std::vector<double> HumanDistanceCalculation::getMiddlePoint(const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2)
{
	std::vector<double> vec;
	
	tf::Vector3 point1(j1.real.z/reso, j1.real.x/reso*-1, j1.real.y/reso);
  	tf::Vector3 point2(j2.real.z/reso, j2.real.x/reso*-1, j2.real.y/reso);
  	
  	tf::Vector3 point_bl1 = camera_transform * point1;
    	tf::Vector3 point_bl2 = camera_transform * point2;
		
	vec.push_back(((point_bl1.getX()) + (point_bl2.getX()))/2);
	vec.push_back(((point_bl1.getY()) + (point_bl2.getY()))/2);
	vec.push_back(((point_bl1.getZ()) +(point_bl2.getZ()))/2);
						
	return vec;	
}

Eigen::Quaterniond HumanDistanceCalculation::calculate_q (const tdv::nuitrack::Joint& j1, const tdv::nuitrack::Joint& j2)
{


	    tf::Vector3 point1(j1.real.z/reso, j1.real.x/reso*-1, j1.real.y/reso);
 	    tf::Vector3 point2(j2.real.z/reso, j2.real.x/reso*-1, j2.real.y/reso); 
 	    
 	    tf::Vector3 point_bl1 = camera_transform * point1;
	    tf::Vector3 point_bl2 = camera_transform * point2;
	    

	    Eigen::Quaterniond q;
	    	
	    Eigen::Vector3d a (point_bl1.getX(), point_bl1.getY(), point_bl1.getZ());	
		
	    Eigen::Vector3d b (point_bl2.getX(), point_bl2.getY(), point_bl2.getZ());        
			      
		Eigen::Vector3d vd = b - a; //vd
		Eigen::Vector3d rz = vd;
		rz.normalize();  //rz
		  
		Eigen::Vector3d up_vector(0.0, 0.0, 1.0);
		Eigen::Vector3d ry = vd.cross(up_vector); 
		ry.normalized(); //ry 
		
		Eigen::Vector3d rx = ry.cross(rz); //rx
		  
		q = (Eigen::Quaterniond (Eigen::Matrix3d {{ rx[0] ,ry[0], rz[0]},
		  					    { rx[1] ,ry[1], rz[1]},
		  					    { rx[2] ,ry[2], rz[2] }}));
	    	
	   return q;
}




void HumanDistanceCalculation::calculateMinDistances(Human *it)
{
  
  std::vector<Joint> joints = it->getJoints();
  
  //for metric conversion 
  reso = 1000;
  
  
  std::vector<double> joints_distances;
  std::vector<Eigen::Quaterniond> q_;
  std::vector<vector<double>> vect_base;
  std::vector<vector<double>> vect_middle_points;
 
  double radius;
  double height;
  
  double x;
  double y;
  double z;
  
  fcl::Transform3d tf_center;
  CollisionObject<double>* cylinder[4];
  CollisionObject<double>* cylinder_joints[16];

//creation of cylinders to body links
  for(int i = 0; i<4; i++)
  {
    radius = robotRepresentation->representations[i]->getParam("radius");
    height = robotRepresentation->representations[i]->getParam("height");

    //tf::StampedTransform tf_center_tmp = robotRepresentation->representations[i]->transform2world_base;
    tf::StampedTransform tf_center_tmp = robotRepresentation->representations[i]->transform2world_center;

    tf_center.setIdentity();
    tf_center.translation() = Eigen::Vector3d (tf_center_tmp.getOrigin().getX(),
                                               tf_center_tmp.getOrigin().getY(),
                                               tf_center_tmp.getOrigin().getZ());

    tf_center.linear() = (Eigen::Quaterniond (tf_center_tmp.getRotation())).toRotationMatrix();

    std::shared_ptr<fcl::CollisionGeometry<double>> cylinder_geometry(new fcl::Cylinder<double>(radius, height));
    cylinder[i] = new CollisionObject<double>(cylinder_geometry, tf_center);
  }
  
  #if 0
  
	//selecting the base point between the selected points for joint parts.
	vect_base.push_back({joints[JOINT_NECK].real.z/reso, joints[JOINT_NECK].real.x/reso, joints[JOINT_NECK].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_COLLAR].real.z/reso, joints[JOINT_LEFT_COLLAR].real.x/reso, joints[JOINT_LEFT_COLLAR].real.y/reso});
	vect_base.push_back({joints[JOINT_TORSO].real.z/reso, joints[JOINT_TORSO].real.x/reso, joints[JOINT_TORSO].real.y/reso});
	vect_base.push_back({joints[JOINT_WAIST].real.z/reso, joints[JOINT_WAIST].real.x/reso, joints[JOINT_WAIST].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_SHOULDER].real.z/reso, joints[JOINT_LEFT_SHOULDER].real.x/reso, joints[JOINT_LEFT_SHOULDER].real.y/reso});
	vect_base.push_back({joints[JOINT_RIGHT_SHOULDER].real.z/reso, joints[JOINT_RIGHT_SHOULDER].real.x/reso, joints[JOINT_RIGHT_SHOULDER].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_HIP].real.z/reso, joints[JOINT_LEFT_HIP].real.x/reso, joints[JOINT_LEFT_HIP].real.y/reso});
	vect_base.push_back({joints[JOINT_RIGHT_HIP].real.z/reso, joints[JOINT_RIGHT_HIP].real.x/reso, joints[JOINT_RIGHT_HIP].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_ELBOW].real.z/reso, joints[JOINT_LEFT_ELBOW].real.x/reso, joints[JOINT_LEFT_ELBOW].real.y/reso});
	vect_base.push_back({joints[JOINT_RIGHT_ELBOW].real.z/reso, joints[JOINT_RIGHT_ELBOW].real.x/reso, joints[JOINT_RIGHT_ELBOW].real.y/reso});
	vect_base.push_back({joints[JOINT_RIGHT_KNEE].real.z/reso, joints[JOINT_RIGHT_KNEE].real.x/reso, joints[JOINT_RIGHT_KNEE].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_KNEE].real.z/reso, joints[JOINT_LEFT_KNEE].real.x/reso, joints[JOINT_LEFT_KNEE].real.y/reso});
	vect_base.push_back({joints[JOINT_LEFT_ANKLE].real.z/reso, joints[JOINT_LEFT_ANKLE].real.x/reso, joints[JOINT_LEFT_ANKLE].real.y/reso});
	vect_base.push_back({joints[JOINT_RIGHT_ANKLE].real.z/reso, joints[JOINT_RIGHT_ANKLE].real.x/reso, joints[JOINT_RIGHT_ANKLE].real.y/reso});
	
 #endif
	
	//for testing monitoring human and calibration
	tf::Vector3 point1(joints[JOINT_LEFT_COLLAR].real.z/reso, joints[JOINT_LEFT_COLLAR].real.x/reso*-1, joints[JOINT_LEFT_COLLAR].real.y/reso);
  	tf::Vector3 point_bl1 = camera_transform * point1;
	
	it->humanTorso.push_back(point_bl1.getX());
	it->humanTorso.push_back(point_bl1.getY());
	it->humanTorso.push_back(point_bl1.getZ());


	joints_distances.push_back(getDistance(joints[JOINT_NECK], joints[JOINT_HEAD]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_COLLAR], joints[JOINT_NECK]));
	joints_distances.push_back(getDistance(joints[JOINT_TORSO],joints[JOINT_LEFT_COLLAR]));
	joints_distances.push_back(getDistance(joints[JOINT_WAIST], joints[JOINT_TORSO]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_HIP], joints[JOINT_WAIST]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_HIP], joints[JOINT_WAIST]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_ELBOW], joints[JOINT_LEFT_SHOULDER]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_ELBOW], joints[JOINT_RIGHT_SHOULDER]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_KNEE], joints[JOINT_RIGHT_HIP]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_KNEE], joints[JOINT_LEFT_HIP]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_ANKLE], joints[JOINT_LEFT_KNEE]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_ANKLE], joints[JOINT_RIGHT_KNEE]));
	joints_distances.push_back(getDistance(joints[JOINT_RIGHT_WRIST], joints[JOINT_RIGHT_ELBOW]));
	joints_distances.push_back(getDistance(joints[JOINT_LEFT_WRIST], joints[JOINT_LEFT_ELBOW]));

  
	q_.push_back(calculate_q(joints[JOINT_NECK], joints[JOINT_HEAD]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_COLLAR], joints[JOINT_NECK]));
	q_.push_back(calculate_q(joints[JOINT_TORSO],joints[JOINT_LEFT_COLLAR]));
	q_.push_back(calculate_q(joints[JOINT_WAIST], joints[JOINT_TORSO]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_HIP], joints[JOINT_WAIST]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_HIP], joints[JOINT_WAIST]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_ELBOW], joints[JOINT_LEFT_SHOULDER]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_ELBOW], joints[JOINT_RIGHT_SHOULDER]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_KNEE], joints[JOINT_RIGHT_HIP]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_KNEE], joints[JOINT_LEFT_HIP]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_ANKLE], joints[JOINT_LEFT_KNEE]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_ANKLE], joints[JOINT_RIGHT_KNEE]));
	q_.push_back(calculate_q(joints[JOINT_RIGHT_WRIST], joints[JOINT_RIGHT_ELBOW]));
	q_.push_back(calculate_q(joints[JOINT_LEFT_WRIST], joints[JOINT_LEFT_ELBOW]));
	
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_NECK], joints[JOINT_HEAD]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_COLLAR], joints[JOINT_NECK]));
	//2
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_TORSO],joints[JOINT_LEFT_COLLAR]));
	//3
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_WAIST], joints[JOINT_TORSO]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_SHOULDER], joints[JOINT_LEFT_COLLAR]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_HIP], joints[JOINT_WAIST]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_HIP], joints[JOINT_WAIST]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_ELBOW], joints[JOINT_LEFT_SHOULDER]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_ELBOW], joints[JOINT_RIGHT_SHOULDER]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_KNEE], joints[JOINT_RIGHT_HIP]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_KNEE], joints[JOINT_LEFT_HIP]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_ANKLE], joints[JOINT_LEFT_KNEE]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_ANKLE], joints[JOINT_RIGHT_KNEE]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_RIGHT_WRIST], joints[JOINT_RIGHT_ELBOW]));
	vect_middle_points.push_back(getMiddlePoint(joints[JOINT_LEFT_WRIST], joints[JOINT_LEFT_ELBOW]));



  //creation of cylinders to body links
  for(int i = 0; i<16; i++){
	  
    if (i==2 || i==3)
	{
		radius = 0.2;
	}
	else
	{
		radius = 0.1;
	}
	

    height =  joints_distances[i];
	
	fcl::Transform3d tf_tmp;
	
	
    x = vect_middle_points[i][0];
    y = vect_middle_points[i][1];
    z = vect_middle_points[i][2];
	
	
    tf_tmp.setIdentity();
    tf_tmp.translation() = Eigen::Vector3d (x, y, z);
    tf_tmp.linear() = (q_[i]).toRotationMatrix();
	
    std::shared_ptr<fcl::CollisionGeometry<double>> cylinder_geometry(new fcl::Cylinder<double>(radius, height));
    cylinder_joints[i] = new CollisionObject<double>(cylinder_geometry, tf_tmp);
  
  }

  fcl::DistanceRequest<double> request;
  fcl::DistanceResult<double> result;


  vector<double>minDistances;
  
  for(int i = 0; i<4; i++)
  {
	minDistances.push_back(DBL_MAX);

  }


  for(int i = 0; i<4; i++)
	{
		  	it->minDistP1[i].x()= DBL_MAX;
		  	it->minDistP1[i].y()= DBL_MAX;
		  	it->minDistP1[i].z()= DBL_MAX;
			it->minDistP2[i].x()= DBL_MAX;
		  	it->minDistP2[i].y()= DBL_MAX;
		  	it->minDistP2[i].z()= DBL_MAX;  
	}



  for(int i = 0; i<16; i++)
  {
      request.gjk_solver_type = fcl::GJKSolverType::GST_INDEP;
      //request.gjk_solver_type = fcl::GJKSolverType::GST_LIBCCD;

	

      for(int j = 0; j < 4; j++)
	  {
			distance(cylinder[j], cylinder_joints[i], request, result);

			if (minDistances[j] > result.min_distance)
			{
			  minDistances[j] = result.min_distance;
			  it->minDistP1[j] = result.nearest_points [0];
			  it->minDistP2[j] = result.nearest_points [1];
			}
			
			#if 1
			
			// if the closest ones to the robot are to be selected among all the people in the environment, minDistances_all has the shortest lengths.
			//minDistP1_all and minDistP2_all specify start and end points.
			if(minDistances_all[j] > minDistances[j])
			{
				minDistances_all[j] = minDistances[j];
				minDistP1_all[j] = result.nearest_points [0];
			  	minDistP2_all[j] = result.nearest_points [1];
			
			}
			
			#endif
			
			result.clear();
      }
  }
  
  it->setMinDistances(minDistances);
  
  
  
  int id = it->getId(); 
  for(int i = 0; i<16; i++)
  {  
	  PublishCylinderMarker((arr[id]*10)+i, vect_middle_points[i][0], vect_middle_points[i][1], vect_middle_points[i][2], 0.0, 1.0, 0.0 , joints_distances[i], q_[i],i); // r,g,b
  }
  
  
  
  
  //visualizeDistances(it);
  
  /*  
  for(int i = 0; i<6; i++)
  {
	std::cout << "MIN DISTANCE: " << i << " - " << minDistances[i] << std::endl;
  }
  */
  
	
  
}

vector<Human> HumanDistanceCalculation::getHumans()
{
	return humans;
	
}

void HumanDistanceCalculation::setHumans(vector<Human> h)
{
	humans = h;
	
}

std::vector<double> HumanDistanceCalculation::getMinDistances_all()
{
	return minDistances_all;
}

void HumanDistanceCalculation::PublishCylinderMarker(int id, float x, float y, float z, 
                       float color_r, float color_g, float color_b, float d , Eigen::Quaterniond q, int i)
{
      
	      q.normalize();	

	      visualization_msgs::Marker marker;
	      marker.header.frame_id = camera_depth_frame_;
	      marker.header.stamp = ros::Time::now();
	
	      string str = "joint-" + to_string(id);
	      marker.ns = str.c_str();
	      marker.id = id; // This must be id unique for each marker

	      uint32_t shape = visualization_msgs::Marker::CYLINDER;
	      marker.type = shape;

	      // Set the marker action.  Options are ADD, DELETE, and DELETEALL
	      marker.action = visualization_msgs::Marker::ADD;
	      marker.color.r = color_r;
	      marker.color.g = color_g; 
	      marker.color.b = color_b;
	      marker.color.a = 1.0;
	      
		  
		  if (i==2 || i==3)
		  {
			marker.scale.x = 0.4; // size of marker in meters
			marker.scale.y = 0.4;
		  }
		  else
		  {
			marker.scale.x = 0.2; // size of marker in meters
			marker.scale.y = 0.2;
		  }
		  
	    
	      marker.scale.z = d;  
	      
	      marker.pose.position.x = x;
	      marker.pose.position.y = y;
	      marker.pose.position.z = z;
	      
	      //std::cout << "---------orientation "<< id << ": " << q.x() <<" / " << q.y() <<" / "<< q.z() <<" / " << q.w() <<" / " << std::endl;
	     
	      marker.pose.orientation.x = q.x();
	      marker.pose.orientation.y = q.y();
	      marker.pose.orientation.z = q.z();
	      marker.pose.orientation.w = q.w();
	 	 
	      // ROS_INFO("DBG: Publishing Marker");
	      marker_pub_.publish(marker);

}


/*
void HumanDistanceCalculation::visualizeDistances(Human* it)
{
  visualization_msgs::Marker marker[6];

  double dx, dy, dz;
  geometry_msgs::Point p;

  for(int i = 0; i < 6; i++){
    marker[i].header.frame_id = "odom";
    marker[i].header.stamp = ros::Time::now();
    string str = "human" + to_string(it->getId()) + "_dist-" + to_string(i);
    marker[i].ns = str.c_str();
    marker[i].id = 100*(it->getId())+i;

    marker[i].type = visualization_msgs::Marker::LINE_STRIP;
    marker[i].action = visualization_msgs::Marker::ADD;
    it->getMinMarkerP1(i, dx, dy, dz);
    
    if (dx == DBL_MAX || dy == DBL_MAX || dz == DBL_MAX)
	continue;
	
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);

    it->getMinMarkerP2(i, dx, dy, dz);
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);


    marker[i].pose.orientation.w = 1.0;
    marker[i].scale.x = 0.02;

    marker[i].color.r = 255.0f;
    marker[i].color.g = 255.0f;
    marker[i].color.b = 0.0f;
    marker[i].color.a = 1.0f;

    marker[i].lifetime = ros::Duration();
    marker_pub_.publish( marker[i] );
  }
}
*/

