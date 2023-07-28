#include <ros/ros.h>
#include <octomap/octomap.h>
#include <octomap_msgs/Octomap.h>
#include <octomap_msgs/conversions.h>
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/Float32MultiArray.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>
#include "odt/OdtDistance.h"
#include "odt/minDistance.h"

#include <RobotRepresentation.h>
#include <Map.h>
#include "DistanceCalculation.h"

using namespace RVServiceTool_ODT;

ros::Publisher cylinder_pub;

void visualizeDistances(DistanceCalculation* dist);
void visualizeBBX(DistanceCalculation* dist);
visualization_msgs::Marker visualizeCylinder( PrimitiveGeometry* cylinder, int linkNo);

int main(int argc, char** argv)
{
  //INITIALIZATION
  ros::init(argc, argv, "odt");
  ros::NodeHandle nh;

  ros::Rate loopRate(15);

  Map *map = new Map();
  RobotRepresentation *representation = new RobotRepresentation;
//  representation->loadGeometry();
  representation->loadGeometry("path//to//robot.xml"); // robot xml ile calisacagi zaman bu satir kullanilacak

  //CONSTRUCT MAP
  map->load("/home/esogu/Desktop/otokar_pcd_v3_shifted.bt");
//  map->load("/home/esra/Desktop/otokar_pcd_v3_shifted.bt");
  DistanceCalculation *distCalculation = new DistanceCalculation(map, representation);
  //octomap::OcTree* octree = new octomap::OcTree("/home/esogu/Desktop/otokar_pcd_v3_shifted.bt");
  octomap::OcTree* octree = map->getTree();
  octomap_msgs::Octomap octomap_msg;
  octomap_msgs::binaryMapToMsg(*octree, octomap_msg);
  octomap_msg.header.seq = 0;
  octomap_msg.header.stamp = ros::Time::now();
  octomap_msg.header.frame_id = "world";


  //SUBSCRUIPTION AND ADVERTISEMENT
  ros::Publisher cylinder_publisher = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  ros::Publisher octomap_publisher = nh.advertise<octomap_msgs::Octomap>("octomap_msg", 1000);
  cylinder_pub = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);

//  ros::Publisher odt_topic_publisher = nh.advertise<std_msgs::Float32MultiArray>("odt", 5);
  ros::Publisher odt_topic_publisher = nh.advertise<odt::OdtDistance>("odt", 5);

  // octree ile arasindaki mesafe en kucuk olan silindirin mesafesini yayinlar
  ros::Publisher min_distance_publisher = nh.advertise<odt::minDistance>("min_distance", 1);

//  //robot frames
//  string frame[12] =  {"world", "linear_x_link", "linear_x_actuator", "linear_z_link", "linear_z_actuator",
//                       "linear_y1_actuator", "linear_y2_actuator", "cam1_link", "cam1_actuator", "cam2_actuator",
//                       "color_cam_link", "tof_cam_link"};

  tf::TransformListener listener;
  vector<tf::StampedTransform> frameTransforms(6);

  double duration = 3.0;

//  std_msgs::Float32MultiArray distanceMsg;
  vector<double> minDistances;

  while (ros::ok()) {

    if(nh.ok()){

      //update frame transform
      try{

//        listener.waitForTransform(frame[0], frame[2], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[2], ros::Time(0), frameTransforms[0]);

//        listener.waitForTransform(frame[0], frame[4], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[4], ros::Time(0), frameTransforms[1]);

//        listener.waitForTransform(frame[0], frame[5], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[5], ros::Time(0), frameTransforms[2]);

//        listener.waitForTransform(frame[0], frame[6], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[6], ros::Time(0), frameTransforms[3]);

//        listener.waitForTransform(frame[0], frame[8], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[8], ros::Time(0), frameTransforms[4]);

//        listener.waitForTransform(frame[0], frame[9], ros::Time(0), ros::Duration(duration));
//        listener.lookupTransform(frame[0], frame[9], ros::Time(0), frameTransforms[5]);

        for(int i = 0; i < representation->getRobot().size(); i++){

          listener.waitForTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), ros::Duration(duration));
          listener.lookupTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), frameTransforms[i]);
        }

        octomap_msgs::binaryMapToMsg(*octree, octomap_msg);
        octomap_msg.header.seq = 0;
        octomap_msg.header.stamp = ros::Time::now();
        octomap_msg.header.frame_id = "world";



      }
      catch(tf::TransformException &ex) {
        ROS_ERROR("%s",ex.what());
      }
      representation->updateTransform(frameTransforms);

      //calculate distances
      distCalculation->calculateMinDistances();
      minDistances = distCalculation->getMinDistances();

      //distance publish
//      distanceMsg.data.clear();
//      for(int i = 0; i < 6; i++){
//        distanceMsg.data.push_back(minDistances[i]);
//      }

//      odt_topic_publisher.publish(distanceMsg);

      odt::OdtDistance distanceMsg;
      distanceMsg.C0 = floor(minDistances[0]*1000)/1000;
      distanceMsg.C1 = floor(minDistances[1]*1000)/1000;
      distanceMsg.C2 = floor(minDistances[2]*1000)/1000;
      distanceMsg.C3 = floor(minDistances[3]*1000)/1000;
      distanceMsg.C4 = floor(minDistances[4]*1000)/1000;
      distanceMsg.C5 = floor(minDistances[5]*1000)/1000;

      odt_topic_publisher.publish(distanceMsg);

//      //********************************* @EG: zekeriyya nin tez icin otobuse en yakin olan silindiri yayinlayan topic olusturuldu, orijinal odt ile ilgisi yoktur
//      //6 silindire ait distance degerleri arasindan en kucuk olan distance degerini yayinlar
//      odt::minDistance min_distance_msg;
////      double min_distance = *min_element(minDistances.begin(), minDistances.end()); //vectorun min value ye sahip elemanini dondurur
////      cout << "min_distance: " << min_distance << endl;
////      min_distance_msg.min_distance = *min_element(minDistances.begin(), minDistances.end()); //orijinal degeri yazdirir
//      min_distance_msg.min_distance = floor(*min_element(minDistances.begin(), minDistances.end())*1000)/1000; //virgulden sonraki 3 basamagi yazdirir
//      min_distance_publisher.publish(min_distance_msg);
//      //**********************************

        //visualization
        for(int i = 0; i<6; i++){

          cylinder_publisher.publish(visualizeCylinder(representation->representations[i], i));
       }
       //visualizeBBX(distCalculation);
        visualizeDistances(distCalculation);
    }

    octomap_publisher.publish(octomap_msg);
    ros::spinOnce();
    loopRate.sleep();
  }

  return 0;
}

visualization_msgs::Marker visualizeCylinder(PrimitiveGeometry* cylinder, int index){

  string r = "radius";
  string h = "height";

  visualization_msgs::Marker marker;
  marker.header.frame_id = "world";
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
  //marker.scale.z = cylinder->getParam(h);
  marker.scale.z = cylinder->getParam(h)*2;

  switch (index) {
    case 0:
      marker.color.r = 0.8f;
      marker.color.g = 0.8f;
      marker.color.b = 0.0f;
      marker.color.a = 1.0f;
      marker.ns = "link_0";
      break;
    case 1:
      marker.color.r = 0.0f;
      marker.color.g = 0.6f;
      marker.color.b = 0.3f;
      marker.color.a = 1.0f;
      marker.ns = "link_1";
      break;
    case 2:
      marker.color.r = 0.0f;
      marker.color.g = 0.6f;
      marker.color.b = 0.6f;
      marker.color.a = 1.0f;
      marker.ns = "link_2";
      break;
    case 3:
      marker.color.r = 0.2f;
      marker.color.g = 0.2f;
      marker.color.b = 1.0f;
      marker.color.a = 1.0f;
      marker.ns = "link_3";
      break;
    case 4:
      marker.color.r = 0.7f;
      marker.color.g = 0.4f;
      marker.color.b = 1.0f;
      marker.color.a = 1.0f;
      marker.ns = "link_4";
      break;
    case 5:
      marker.color.r = 1.0f;
      marker.color.g = 0.6f;
      marker.color.b = 0.6f;
      marker.color.a = 1.0f;
      marker.ns = "link_5";
      break;
    default:
      break;
  }
  marker.lifetime = ros::Duration();

  return marker;
}


void visualizeBBX(DistanceCalculation* dist)
{
  visualization_msgs::Marker marker1, marker2;
  marker1.header.frame_id = "world";
  marker1.header.stamp = ros::Time::now();
  //marker.header.stamp = ros::Time();
  marker1.ns = "world";

  marker1.type = visualization_msgs::Marker::CUBE;
  marker1.action = visualization_msgs::Marker::ADD;

  marker1.pose.position.x = dist->min.x();
  marker1.pose.position.y = dist->min.y();
  marker1.pose.position.z =  dist->min.z();
  marker1.pose.orientation.x = 0;
  marker1.pose.orientation.y = 0;
  marker1.pose.orientation.z = 0;
  marker1.pose.orientation.w = 1;

  marker1.scale.x = 0.5;
  marker1.scale.y = 0.5;
  marker1.scale.z = 0.5;

  marker1.color.r = 0.9f;
  marker1.color.g = 0.5f;
  marker1.color.b = 0.5f;
  marker1.color.a = 1.0f;
  marker1.ns = "min";


  marker2.header.frame_id = "world";
  marker2.header.stamp = ros::Time::now();
  //marker.header.stamp = ros::Time();
  marker2.ns = "world";


  marker2.type = visualization_msgs::Marker::CUBE;
  marker2.action = visualization_msgs::Marker::ADD;

  marker2.pose.position.x = dist->max.x();
  marker2.pose.position.y = dist->max.y();
  marker2.pose.position.z =  dist->max.z();
  marker2.pose.orientation.x = 0;
  marker2.pose.orientation.y = 0;
  marker2.pose.orientation.z = 0;
  marker2.pose.orientation.w = 1;

  marker2.scale.x = 0.5;
  marker2.scale.y = 0.5;
  marker2.scale.z = 0.5;

  marker2.color.r = 0.9f;
  marker2.color.g = 0.5f;
  marker2.color.b = 0.5f;
  marker2.color.a = 1.0f;
  marker2.ns = "max";

  //marker.lifetime = ros::Duration(0.3);
  marker1.lifetime = ros::Duration();
  cylinder_pub.publish( marker1 );

  marker2.lifetime = ros::Duration();
  cylinder_pub.publish( marker2 );
}

void visualizeDistances(DistanceCalculation* dist)
{
  visualization_msgs::Marker marker[6];

  double dx, dy, dz;
  geometry_msgs::Point p;

  for(int i = 0; i < 6; i++){
    marker[i].header.frame_id = "world";
    marker[i].header.stamp = ros::Time::now();
    string str = "dist-" + to_string(i);
    marker[i].ns = str.c_str();
    marker[i].id = 10+i;

    marker[i].type = visualization_msgs::Marker::LINE_STRIP;
    marker[i].action = visualization_msgs::Marker::ADD;

    dist->getMinMarkerP1(i, dx, dy, dz);
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);

    dist->getMinMarkerP2(i, dx, dy, dz);
    p.x = dx;
    p.y = dy;
    p.z = dz;
    marker[i].points.push_back(p);


    marker[i].pose.orientation.w = 1.0;
    marker[i].scale.x = 0.02;

    marker[i].color.r = 0.0f;
    marker[i].color.g = 0.0f;
    marker[i].color.b = 1.0f;
    marker[i].color.a = 1.0f;

    marker[i].lifetime = ros::Duration();
    cylinder_pub.publish( marker[i] );
  }
}
