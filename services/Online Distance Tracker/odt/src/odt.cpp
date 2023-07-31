#include <ros/ros.h>
#include <octomap/octomap.h>
#include <octomap_msgs/Octomap.h>
#include <octomap_msgs/conversions.h>
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>
#include "odt/OdtDistance.h"
#include "odt/minDistance.h"
#include <chrono>
#include <RobotRepresentation.h>
#include <Map.h>
#include "DistanceCalculation.h"
#include <jsoncpp/json/json.h>
using namespace RVServiceTool_ODT;

ros::Publisher cylinder_pub;

void visualizeDistances(DistanceCalculation* dist);
void visualizeBBX(DistanceCalculation* dist);
visualization_msgs::Marker visualizeCylinder( PrimitiveGeometry* cylinder, int linkNo);
Json::Value cylinder2Json(Json::Value json_data, PrimitiveGeometry* cylinder, int index);
Json::Value dist2Json(Json::Value json_data, DistanceCalculation* dist);

int main(int argc, char** argv)
{
  //INITIALIZATION
  ros::init(argc, argv, "odt");
  ros::NodeHandle nh;

  ros::Rate loopRate(15);

  std::string strData = "{\"cylinder1\":{\"pose\":{\"x\":0,\"y\":0,\"z\":0,\"or_x\":0,\"or_y\":0,\"or_z\":0,\"or_w\":0}},\"cylinder2\":{\"pose\":{\"x\":0,\"y\":0,\"z\":0,\"or_x\":0,\"or_y\":0,\"or_z\":0,\"or_w\":0}},\"cylinder3\":{\"pose\":{\"x\":0,\"y\":0,\"z\":0,\"or_x\":0,\"or_y\":0,\"or_z\":0,\"or_w\":0}},\"cylinder4\":{\"pose\":{\"x\":0,\"y\":0,\"z\":0,\"or_x\":0,\"or_y\":0,\"or_z\":0,\"or_w\":0}},\"dist1\":{\"strt_pose\":{\"x\":0,\"y\":0,\"z\":0},{\"fin_pose\":{\"x\":0,\"y\":0,\"z\":0}}},\"dist2\":{\"strt_pose\":{\"x\":0,\"y\":0,\"z\":0},{\"fin_pose\":{\"x\":0,\"y\":0,\"z\":0}}},\"dist3\":{\"strt_pose\":{\"x\":0,\"y\":0,\"z\":0},{\"fin_pose\":{\"x\":0,\"y\":0,\"z\":0}}},\"dist4\":{\"strt_pose\":{\"x\":0,\"y\":0,\"z\":0},{\"fin_pose\":{\"x\":0,\"y\":0,\"z\":0}}}}";
  Json::Reader reader;
  Json::Value jsonData;
  std::string odtMsg;
  Json::FastWriter fastWriter;
  std_msgs::String stringMsg;

  reader.parse(strData, jsonData, false);

  Map *map = new Map();
  RobotRepresentation *representation = new RobotRepresentation;
  //representation->loadGeometry();
  representation->loadGeometry("/home/s216/catkin_ws/src/odt/robot.xml"); // robot xml ile calisacagi zaman bu satir kullanilacak

  //CONSTRUCT MAP
  //map->load("/home/s216/Desktop/otokar_pcd_v3_shifted.bt");
  map->load("/home/s216/catkin_ws/src/odt/ifarlab_moved_origin_with_windows_0_01.bt");
  
  DistanceCalculation *distCalculation = new DistanceCalculation(map, representation);
  //octomap::OcTree* octree = new octomap::OcTree("/home/s216/Desktop/otokar_pcd_v3_shifted.bt");
  octomap::OcTree* octree = map->getTree();
  octomap_msgs::Octomap octomap_msg;
  octomap_msgs::binaryMapToMsg(*octree, octomap_msg);
  octomap_msg.header.seq = 0;
  octomap_msg.header.stamp = ros::Time::now();
  octomap_msg.header.frame_id = "odom";


  //SUBSCRUIPTION AND ADVERTISEMENT
  ros::Publisher cylinder_publisher = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  ros::Publisher octomap_publisher = nh.advertise<octomap_msgs::Octomap>("octomap_msg", 1000);
  cylinder_pub = nh.advertise<visualization_msgs::Marker>("visualization_marker", 1);

//  ros::Publisher odt_topic_publisher = nh.advertise<std_msgs::Float32MultiArray>("odt", 5);
  // ros::Publisher odt_topic_publisher = nh.advertise<odt::OdtDistance>("odt", 3);
  ros::Publisher odt_topic_publisher = nh.advertise<odt::minDistance>("odt", 3);

  // octree ile arasindaki mesafe en kucuk olan silindirin mesafesini yayinlar
  ros::Publisher min_distance_publisher = nh.advertise<odt::minDistance>("min_distance", 1);

  ros::Publisher odt_json_publisher = nh.advertise<std_msgs::String>("odt_json", 1);

 //robot frames
 string frame[11] =  {"odom", "ota_base_link", "manipulator_base_link", "base_link", "link1",
                      "link2", "link3", "link4", "link5", "link6",
                      "link7"};

  tf::TransformListener listener;
  vector<tf::StampedTransform> frameTransforms(4);

  double duration = 3.0;

//  std_msgs::Float32MultiArray distanceMsg;
  vector<double> minDistances;

  while (ros::ok()) {

    if(nh.ok()){

      //update frame transform
      try
      {

       listener.waitForTransform(frame[0], frame[4], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[4], ros::Time(0), frameTransforms[0]);

       listener.waitForTransform(frame[0], frame[5], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[5], ros::Time(0), frameTransforms[1]);

       listener.waitForTransform(frame[0], frame[7], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[7], ros::Time(0), frameTransforms[2]);

       listener.waitForTransform(frame[0], frame[8], ros::Time(0), ros::Duration(duration));
       listener.lookupTransform(frame[0], frame[8], ros::Time(0), frameTransforms[3]);

   
        // for(int i = 0; i < representation->getRobot().size(); i++){

        //   listener.waitForTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), ros::Duration(duration));
        //   listener.lookupTransform(representation->getRootFrame(), representation->getRobot()[i].frameName, ros::Time(0), frameTransforms[i]);
        // }

        octomap_msgs::binaryMapToMsg(*octree, octomap_msg);
        octomap_msg.header.seq = 0;
        octomap_msg.header.stamp = ros::Time::now();
        octomap_msg.header.frame_id = "odom";



      }
      catch(tf::TransformException &ex) {
        ROS_ERROR("%s",ex.what());
      }
      representation->updateTransform(frameTransforms);
      auto start2 = std::chrono::high_resolution_clock::now();
      //calculate distances
      distCalculation->calculateMinDistances();
      minDistances = distCalculation->getMinDistances();
      auto stop2 = std::chrono::high_resolution_clock::now();
      auto duration2 = std::chrono::duration_cast<std::chrono::microseconds>(stop2 - start2);

      double run_time = duration2.count();
      cout << endl;
      cout <<"*** Calculation duration (microseconds): " << run_time  << endl;
      cout <<"*** Calculation duration (seconds): " << run_time/1000000  << endl;
      cout << endl;


      //distance publish
//      distanceMsg.data.clear();
//      for(int i = 0; i < 6; i++){
//        distanceMsg.data.push_back(minDistances[i]);
//      }

//      odt_topic_publisher.publish(distanceMsg);

      // odt::OdtDistance distanceMsg;
      // distanceMsg.c0 = floor(minDistances[0]*1000)/1000;
      // distanceMsg.c1 = floor(minDistances[1]*1000)/1000;
      // distanceMsg.c2 = floor(minDistances[2]*1000)/1000;
      // distanceMsg.c3 = floor(minDistances[3]*1000)/1000;
      //distanceMsg.c4 = floor(minDistances[4]*1000)/1000;
      //distanceMsg.c5 = floor(minDistances[5]*1000)/1000;

      // odt_topic_publisher.publish(distanceMsg);

//      //********************************* @EG: zekeriyya nin tez icin otobuse en yakin olan silindiri yayinlayan topic olusturuldu, orijinal odt ile ilgisi yoktur
//      //6 silindire ait distance degerleri arasindan en kucuk olan distance degerini yayinlar
    odt::minDistance min_distance_msg;
    double min_distance = *min_element(minDistances.begin(), minDistances.end()); //vectorun min value ye sahip elemanini dondurur
    //  cout << "min_distance: " << min_distance << endl;
    min_distance_msg.minDistance = *min_element(minDistances.begin(), minDistances.end()); //orijinal degeri yazdirir
    min_distance_msg.minDistance = floor(*min_element(minDistances.begin(), minDistances.end())*1000)/1000; //virgulden sonraki 3 basamagi yazdirir
    // min_distance_publisher.publish(min_distance_msg);
    odt_topic_publisher.publish(min_distance_msg);
//      //**********************************

        //visualization
        for(int i = 0; i<4; i++){

          // cylinder_publisher.publish(visualizeCylinder(representation->representations[i], i)); // didem yorum yapti
          jsonData = cylinder2Json(jsonData, representation->representations[i], i);
       }
       //visualizeBBX(distCalculation);
        // visualizeDistances(distCalculation); // didem yorum yapti
        jsonData = dist2Json(jsonData, distCalculation);
        stringMsg.data = fastWriter.write(jsonData);
        odt_json_publisher.publish(stringMsg);
    }

    octomap_publisher.publish(octomap_msg);
    ros::spinOnce();
    loopRate.sleep();
  }

  return 0;
}

Json::Value cylinder2Json(Json::Value jsonData, PrimitiveGeometry* cylinder, int index){
  jsonData["cylinder"+std::to_string(index)]["pose"]["x"] = cylinder->transform2world_center.getOrigin().getX();
  jsonData["cylinder"+std::to_string(index)]["pose"]["y"] = cylinder->transform2world_center.getOrigin().getY();
  jsonData["cylinder"+std::to_string(index)]["pose"]["z"] = cylinder->transform2world_center.getOrigin().getZ();// + cylinder->getParam(h);
  jsonData["cylinder"+std::to_string(index)]["pose"]["or_x"] = cylinder->transform2world_center.getRotation().getX();
  jsonData["cylinder"+std::to_string(index)]["pose"]["or_y"] = cylinder->transform2world_center.getRotation().getY();
  jsonData["cylinder"+std::to_string(index)]["pose"]["or_z"] = cylinder->transform2world_center.getRotation().getZ();
  jsonData["cylinder"+std::to_string(index)]["pose"]["or_w"] = cylinder->transform2world_center.getRotation().getW();
  return jsonData;
}
Json::Value dist2Json(Json::Value jsonData, DistanceCalculation* dist){
  double dx, dy, dz;
  for(int i = 0; i < 4; i++){
    dist->getMinMarkerP1(i, dx, dy, dz);
    jsonData["dist"+std::to_string(i)]["strt_pose"]["x"] = dx;
    jsonData["dist"+std::to_string(i)]["strt_pose"]["y"] = dy;
    jsonData["dist"+std::to_string(i)]["strt_pose"]["z"] = dz;// + cylinder->getParam(h);
    dist->getMinMarkerP2(i, dx, dy, dz);
    jsonData["dist"+std::to_string(i)]["fin_pose"]["x"] = dx;
    jsonData["dist"+std::to_string(i)]["fin_pose"]["y"] = dy;
    jsonData["dist"+std::to_string(i)]["fin_pose"]["z"] = dz;
  }
  return jsonData;
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
  marker.pose.position.z = cylinder->transform2world_center.getOrigin().getZ();// + cylinder->getParam(h);
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
      marker.ns = "link_1";
      break;
    case 1:
      
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


void visualizeBBX(DistanceCalculation* dist)
{
  visualization_msgs::Marker marker1, marker2;
  marker1.header.frame_id = "odom";
  marker1.header.stamp = ros::Time::now();
  //marker.header.stamp = ros::Time();
  marker1.ns = "odom";

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


  marker2.header.frame_id = "odom";
  marker2.header.stamp = ros::Time::now();
  //marker.header.stamp = ros::Time();
  marker2.ns = "odom";


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
  visualization_msgs::Marker marker[4];

  double dx, dy, dz;
  geometry_msgs::Point p;

  for(int i = 0; i < 4; i++){
    marker[i].header.frame_id = "odom";
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
