#include <ros/ros.h>

#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/Float32MultiArray.h>
#include "std_msgs/Float32.h"
#include <std_msgs/String.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>

#include <RobotRepresentation.h>
#include <HumanDistanceCalculation.h>
#include "oht/OhtDistance.h"
#include "oht/minDistance.h"
#include "oht/OhtHuman.h"
#include "oht/OhtHumanInfo.h"

#include <iostream>
#include <cmath>
#include <math.h>


using namespace RVServiceTool_OHT;



void visualizeDistances(Human* it);
void visualizeDistances_2(HumanDistanceCalculation *it);
visualization_msgs::Marker visualizeCylinder( PrimitiveGeometry* cylinder, int linkNo);

HumanDistanceCalculation *h_distCalculation;

int main(int argc, char *argv[])
{
  //INITIALIZATION
  ros::init(argc, argv, "oht");
  ros::NodeHandle nh;

  ros::Rate loopRate(15);

  RobotRepresentation *representation = new RobotRepresentation;
  
  
  // this line will be used when the robot will work with xml
  representation->loadGeometry("/home/esogu-ifarlab/catkin_ws/src/oht/robot.xml"); // robot xml ile calisacagi zaman bu satir kullanilacak
  //It is used when information about the robot is in the function.
  //representation->loadGeometry();
  
  //Giving the camera's transform information according to the odom
  tf::StampedTransform transform;
  tf::Vector3 T;
  

  //translation
  T.setValue(34/100, 105/100, 135/100);
  //rotation
  
  double qz = (22*M_PI)/180 ;
  
  Eigen::Matrix3d a {{ cos(qz), sin(qz), 0},
		       { -sin(qz), cos(qz), 0},
		       { 0, 0, 1}};		      		       
  
  

  Eigen::Quaterniond q (a);
  
  tf::Quaternion R (q.x(), q.y(), q.z(), q.w());
  
  transform.setOrigin(T);
  transform.setRotation(R);
 
  

  
  h_distCalculation = new HumanDistanceCalculation(representation, "odom", transform);
  
  std::string configPath = "";
  // get nuitrack configuration file extension
  configPath=ros::this_node::getName();
  //set nuitrack config file location
  h_distCalculation->init(configPath);
	


  //SUBSCRUIPTION AND ADVERTISEMENT
  ros::Publisher cylinder_publisher = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  //cylinder_pub = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);

  ros::Publisher oht_topic_publisher = nh.advertise<oht::OhtDistance>("oht_distances", 4);
  
  //reports the distance of the cylinder with the smallest distance
  //ros::Publisher min_distance_publisher = nh.advertise<oht::minDistance>("oht", 1);
  
  ros::Publisher min_distance_publisher = nh.advertise<std_msgs::Float32>("oht", 1);
  std_msgs::Float32 oht;

  ros::Publisher human_torso_publisher = nh.advertise<std_msgs::Float32MultiArray>("oht_human_info", 4);
  std_msgs::Float32MultiArray humanMsg;
  
  // ros::Publisher human_torso_publisher = nh.advertise<std_msgs::String>("oht_human_info", 4);
  // std_msgs::String humanMsg;
  
  

  //robot frames
  string frame[11] =  {"odom", "ota_base_link", "manipulator_base_link", "base_link", "link1",
                      "link2", "link3", "link4", "link5", "link6",
                      "link7"};

  tf::TransformListener listener;
  vector<tf::StampedTransform> frameTransforms(4);

  double duration = 3.0;

  vector<double> minHumanDistances;
  
  

  while (ros::ok()) {

    if(nh.ok()){
    
      
      //update frame transform
      try{

       listener.waitForTransform(frame[0], frame[4], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[4], ros::Time(0), frameTransforms[0]);

       listener.waitForTransform(frame[0], frame[5], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[5], ros::Time(0), frameTransforms[1]);

       listener.waitForTransform(frame[0], frame[7], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[7], ros::Time(0), frameTransforms[2]);

       listener.waitForTransform(frame[0], frame[8], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[8], ros::Time(0), frameTransforms[3]);
        
	
	/*	
	
		for(int i = 0; i < representation->getRobot().size(); i++){

          listener.waitForTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), ros::Duration(duration));
          listener.lookupTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), frameTransforms[i]);
        }
        
        */
		

      }
      catch(tf::TransformException &ex) {
        ROS_ERROR("%s",ex.what());
      }
      representation->updateTransform(frameTransforms);
      
      
      //nuitrack
      h_distCalculation->update();
	  
 
       //visualization
        for(int i = 0; i<4; i++){
  
          cylinder_publisher.publish(visualizeCylinder(representation->representations[i], i));
       }
       
       

	     
      //std::cout << "Number of existing people in the environment: " << h_distCalculation->getHumans().size() << std::endl;   
	  
        #if 1
            
        vector<double> all_min = h_distCalculation->getMinDistances_all();
        
        oht::OhtDistance distanceHumanMsg;

        distanceHumanMsg.C0 = floor(all_min[0]*1000)/1000;
        distanceHumanMsg.C1 = floor(all_min[1]*1000)/1000;
        distanceHumanMsg.C2 = floor(all_min[2]*1000)/1000;
        distanceHumanMsg.C3 = floor(all_min[3]*1000)/1000;
       

        oht_topic_publisher.publish(distanceHumanMsg);
        
        
	
	//oht::minDistance min_distance_msg;
	
	//double min_distance = *min_element(minHumanDistances.begin(), minHumanDistances.end()); //vectorun min value ye sahip elemanini dondurur
	//cout << "min_distance: " << min_distance << endl;
	//min_distance_msg.min_distance = *min_element(minHumanDistances.begin(), minHumanDistances.end()); //orijinal degeri yazdirir
	//min_distance_msg.min_distance = floor(*min_element(all_min.begin(), all_min.end())*1000)/1000; //virgulden sonraki 3 basamagi yazdirir
	//min_distance_publisher.publish(min_distance_msg);
	
	oht.data = floor(*min_element(all_min.begin(), all_min.end())*1000)/1000; 
	min_distance_publisher.publish(oht);
	
	
	vector<Human> humans_ = h_distCalculation->getHumans();
	if (humans_.size() != 0 )
		visualizeDistances_2(h_distCalculation);
	
	if (humans_.size() != 0 )
	{
	  //oht::OhtHumanInfo data;
	  //oht::OhtHuman msg;
	  
	  for (int i=0; i<humans_.size();i++)
	  {
		humanMsg.data.clear(); 

		
		//data.human_id=i+1; data.C0=humans_[i].humanTorso[0]; data.C1=humans_[i].humanTorso[1]; data.C2=humans_[i].humanTorso[2];
		//msg.OhtHumanInfo.push_back(data);
		
		humanMsg.data.push_back(i+1); 
		//humanMsg.data[0]=(i+1);
		for (int j=0; j<3;j++)
		{
		
			humanMsg.data.push_back(humans_[i].humanTorso[j]);    
			//humanMsg.data[j+1] = humans_[i].humanTorso[j];
		}

		human_torso_publisher.publish(humanMsg);	
		  
	  }
	  
	}
	
	//human_torso_publisher.publish(msg); 
	
	
	
	
	#endif
		
        #if 0
        
        vector<Human> humans_ = h_distCalculation->getHumans();
             
      	//for (vector<Human*>::iterator it = humans_.begin(); it != humans_.end(); ++it) 
      	for (int i = 0; i < humans_.size(); i++) 
      {

        minHumanDistances = humans_[i].getMinDistances();
        
        
        oht::OhtDistance distanceHumanMsg;

        distanceHumanMsg.C0 = floor(minHumanDistances[0]*1000)/1000;
        distanceHumanMsg.C1 = floor(minHumanDistances[1]*1000)/1000;
        distanceHumanMsg.C2 = floor(minHumanDistances[2]*1000)/1000;
        distanceHumanMsg.C3 = floor(minHumanDistances[3]*1000)/1000;
       

        oht_topic_publisher.publish(distanceHumanMsg);
        		
	// Publishes the smallest distance value among the distance values of the 4 cylinder
	oht::minDistance min_distance_msg;
	//double min_distance = *min_element(minHumanDistances.begin(), minHumanDistances.end()); //vectorun min value ye sahip elemanini dondurur
	//cout << "min_distance: " << min_distance << endl;
	//min_distance_msg.min_distance = *min_element(minHumanDistances.begin(), minHumanDistances.end()); //orijinal degeri yazdirir
	min_distance_msg.min_distance = floor(*min_element(minHumanDistances.begin(), minHumanDistances.end())*1000)/1000; //virgulden sonraki 3 basamagi yazdirir
	min_distance_publisher.publish(min_distance_msg);
		
		
	visualizeDistances(&humans_[i]);
		
	

      }
	  
	#endif
    }

   
    ros::spinOnce();
    loopRate.sleep();
  }

   //nuitrack
   h_distCalculation->release();

  return 0;
}

visualization_msgs::Marker visualizeCylinder(PrimitiveGeometry* cylinder, int index){

  string r = "radius";
  string h = "height";

  visualization_msgs::Marker marker;
  marker.header.frame_id = "odom";
  marker.header.stamp = ros::Time::now();
  //marker.header.stamp = ros::Time();
  marker.id = index;

  marker.type = visualization_msgs::Marker::CYLINDER;
  marker.action = visualization_msgs::Marker::ADD;

  marker.pose.position.x = cylinder->transform2world_center.getOrigin().getX();
  marker.pose.position.y = cylinder->transform2world_center.getOrigin().getY();
  marker.pose.position.z = cylinder->transform2world_center.getOrigin().getZ();
  marker.pose.orientation.x = cylinder->transform2world_center.getRotation().getX();
  marker.pose.orientation.y = cylinder->transform2world_center.getRotation().getY();
  marker.pose.orientation.z = cylinder->transform2world_center.getRotation().getZ();
  marker.pose.orientation.w = cylinder->transform2world_center.getRotation().getW();

  marker.scale.x = cylinder->getParam(r)*2;
  marker.scale.y = cylinder->getParam(r)*2;
  marker.scale.z = cylinder->getParam(h)*2;

  switch (index) {
    case 0:
      marker.color.r = 0.8f;
      marker.color.g = 0.8f;
      marker.color.b = 0.0f;
      marker.color.a = 1.0f;
      marker.ns = "link_1";
      break;
    case 1:
      
      //marker.pose.position.x = cylinder->transform2world_center.getOrigin().getX() - cylinder->getParam(r)/2;
      marker.pose.position.x = cylinder->transform2world_center.getOrigin().getX() + cylinder->getParam(r)/2;
      marker.pose.position.y = cylinder->transform2world_center.getOrigin().getY() ;
	  marker.pose.position.z = cylinder->transform2world_center.getOrigin().getZ() + cylinder->getParam(h)/2;
	  marker.pose.orientation.x = cylinder->transform2world_center.getRotation().getX();
	  marker.pose.orientation.y = cylinder->transform2world_center.getRotation().getY();
	  marker.pose.orientation.z = cylinder->transform2world_center.getRotation().getZ();
	  marker.pose.orientation.w = cylinder->transform2world_center.getRotation().getW();

	  marker.scale.x = cylinder->getParam(r)*2;
	  marker.scale.y = cylinder->getParam(r)*2;
	  marker.scale.z = cylinder->getParam(h);
	  //marker.scale.z = cylinder->getParam(h)*2;
      
      marker.color.r = 0.0f;
      marker.color.g = 0.6f;
      marker.color.b = 0.3f;
      marker.color.a = 1.0f;
      marker.ns = "link_2";
      break;
    case 2:
    
    
      marker.pose.position.x = cylinder->transform2world_center.getOrigin().getX();
      marker.pose.position.y = cylinder->transform2world_center.getOrigin().getY();
	  marker.pose.position.z = cylinder->transform2world_center.getOrigin().getZ();
	  marker.pose.orientation.x = cylinder->transform2world_center.getRotation().getX();
	  marker.pose.orientation.y = cylinder->transform2world_center.getRotation().getY();
	  marker.pose.orientation.z = cylinder->transform2world_center.getRotation().getZ();
	  marker.pose.orientation.w = cylinder->transform2world_center.getRotation().getW();

	  marker.scale.x = cylinder->getParam(r)*2;
	  marker.scale.y = cylinder->getParam(r)*2;
	  marker.scale.z = cylinder->getParam(h);
	  
      marker.color.r = 0.0f;
      marker.color.g = 0.6f;
      marker.color.b = 0.6f;
      marker.color.a = 1.0f;
      marker.ns = "link_4";
      break;
    case 3:
    
    
    	 marker.pose.position.x = cylinder->transform2world_center.getOrigin().getX() ;
      marker.pose.position.y = cylinder->transform2world_center.getOrigin().getY() - cylinder->getParam(h)/2;
	  marker.pose.position.z = cylinder->transform2world_center.getOrigin().getZ();
	  marker.pose.orientation.x = cylinder->transform2world_center.getRotation().getX();
	  marker.pose.orientation.y = cylinder->transform2world_center.getRotation().getY();
	  marker.pose.orientation.z = cylinder->transform2world_center.getRotation().getZ();
	  marker.pose.orientation.w = cylinder->transform2world_center.getRotation().getW();

	  marker.scale.x = cylinder->getParam(r)*2;
	  marker.scale.y = cylinder->getParam(r)*2;
	  marker.scale.z = cylinder->getParam(h);
	  
      marker.color.r = 0.2f;
      marker.color.g = 0.2f;
      marker.color.b = 1.0f;
      marker.color.a = 1.0f;
      marker.ns = "link_5";
      break;
    default:
      break;
  }
  marker.lifetime = ros::Duration();

  return marker;
}

void visualizeDistances(Human* it)
{
  visualization_msgs::Marker marker[4];

  double dx, dy, dz;
  geometry_msgs::Point p;

  for(int i = 0; i < 4; i++){
    marker[i].header.frame_id = "odom";
    marker[i].header.stamp = ros::Time::now();
    string str = "human" + to_string(it->getId()) + "_dist-" + to_string(i);
    marker[i].ns = str.c_str();
    marker[i].id = 9+i;

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
    h_distCalculation->cylinder_pub.publish( marker[i] );
  }
}

void visualizeDistances_2(HumanDistanceCalculation *it)
{
  visualization_msgs::Marker marker[4];

  double dx, dy, dz;
  geometry_msgs::Point p;
  

  for(int i = 0; i < 4; i++){
    marker[i].header.frame_id = "odom";
    marker[i].header.stamp = ros::Time::now();
    string str = "humans_all_dist-" + to_string(i);
    marker[i].ns = str.c_str();
    marker[i].id = 9+i;

    marker[i].type = visualization_msgs::Marker::LINE_STRIP;
    marker[i].action = visualization_msgs::Marker::ADD;
    

    dx = it->minDistP1_all[i].x();
    dy = it->minDistP1_all[i].y();
    dz = it->minDistP1_all[i].z();
    
    if (dx == DBL_MAX || dy == DBL_MAX || dz == DBL_MAX)
	continue;
    
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);

    dx = it->minDistP2_all[i].x();
    dy = it->minDistP2_all[i].y();
    dz = it->minDistP2_all[i].z();
    
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);


    marker[i].pose.orientation.w = 1.0;
    marker[i].scale.x = 0.02;

    marker[i].color.r = 1.0f;
    marker[i].color.g = 1.0f;
    marker[i].color.b = 1.0f;
    marker[i].color.a = 1.0f;

    marker[i].lifetime = ros::Duration();
    h_distCalculation->cylinder_pub.publish( marker[i] );
  }
}
