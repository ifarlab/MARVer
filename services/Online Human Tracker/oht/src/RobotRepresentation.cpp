#include <RobotRepresentation.h>
#include <Cylinder.h>
#include <rapidxml/rapidxml.hpp>
#include <rapidxml/rapidxml_utils.hpp>
#include <rapidxml/rapidxml_print.hpp>

using namespace rapidxml;
using namespace RVServiceTool_OHT;

vector<double> split(string str){

  vector<double> tokens;
  string temp;

  stringstream token(str);

  while(getline(token, temp, ' ')){
    tokens.push_back(stod(temp));
  }
  return tokens;
}

void RobotRepresentation::parseXML(string fileName){

  file<> xmlFile(fileName.c_str());

  // Create & parse document
  xml_document<> doc;
  doc.parse<0>(xmlFile.data());

  // Find root node
  xml_node<> * root_node = doc.first_node("robot");

  robotBrand = root_node->first_attribute("brand")->value();
  robotModel = root_node->first_attribute("model")->value();
  rootFrameName = root_node->first_attribute("root_frame_name")->value();

//   cout << "robot brand: " << robotBrand << " model: " << robotModel << " root frame: " << rootFrameName << endl;

  //          <robot>               <cylinders>
  root_node = root_node->first_node("cylinders");

  robotInfo r_info;
//  vector<robotInfo> robot;

  for(xml_node<> * cylinder_node = root_node->first_node("cylinder"); cylinder_node; cylinder_node = cylinder_node->next_sibling()){

    r_info.cylinderId = cylinder_node->first_attribute("id")->value();
    r_info.cylinderName = cylinder_node->first_attribute("name")->value();
    r_info.radius = stod(cylinder_node->first_attribute("radius")->value()); //convert string to double using stod
    r_info.height = stod(cylinder_node->first_attribute("height")->value()); //convert string to double using stod

    for(xml_node<> * robot_frame_node = cylinder_node->first_node("robot_frame"); robot_frame_node; robot_frame_node = robot_frame_node->next_sibling()){

      r_info.frameId = robot_frame_node->first_attribute("id")->value();
      r_info.frameName = robot_frame_node->first_attribute("name")->value();
      r_info.rotation = split(robot_frame_node->first_attribute("rotation")->value());
      r_info.translation = split(robot_frame_node->first_attribute("translation")->value());
    }

    robot.push_back(r_info);
  }

}

void RobotRepresentation::loadGeometry(string fileName){

  parseXML(fileName);

//  cout << "inside loadGeometry" << endl << "robotsize: " << robot.size() << endl;
//  for(int i = 0; i < robot.size(); i++ ){

//    cout << i << ". cylinder\n" << "id: " << robot[i].cylinderId << endl << "name: " << robot[i].cylinderName << endl
//         << "radius: " << robot[i].radius << endl << "height: " << robot[i].height << endl
//         << "frame_id: " << robot[i].frameId << endl << "frame_name: " << robot[i].frameName << endl
//         << "rotation0: " << robot[i].rotation[0] << endl
//         << "rotation1: " << robot[i].rotation[1] << endl
//         << "rotation2: " << robot[i].rotation[2] << endl
//         << "translation0: " << robot[i].translation[0] << endl
//         << "translation1: " << robot[i].translation[1] << endl
//         << "translation2: " << robot[i].translation[2] << endl;
//  }

  tf::StampedTransform transform;
  tf::Vector3 T;
  tf::Quaternion R;

  for(int i = 0; i < robot.size(); i++){

    representations.push_back(new Cylinder(robot[i].radius, robot[i].height));

    T.setValue(robot[i].translation[0], robot[i].translation[1], robot[i].translation[2]);
    R.setRPY(robot[i].rotation[0], robot[i].rotation[1], robot[i].rotation[2]);

    transform.setOrigin(T);
    transform.setRotation(R);
    representations[i]->transform2frames_center = transform;
  }

}

int RobotRepresentation::loadGeometry(){

//  representations.push_back(new Cylinder(0.295, 4.20));
//  representations.push_back(new Cylinder(0.0825, 1.505));
//  representations.push_back(new Cylinder(0.1725, 1.5));
//  representations.push_back(new Cylinder(0.1425, 1.66));
//  representations.push_back(new Cylinder(0.134, 0.342));
//  representations.push_back(new Cylinder(0.13, 0.095));

 
  representations.push_back(new Cylinder(0.295, 2.1));
  representations.push_back(new Cylinder(0.0825, 0.7525));
  representations.push_back(new Cylinder(0.1725, 0.75));
  representations.push_back(new Cylinder(0.124, 0.83));//original -> (0.1425, 1.66))
  representations.push_back(new Cylinder(0.134, 0.171));
  representations.push_back(new Cylinder(0.13, 0.0475));

  tf::StampedTransform transform;
  tf::Vector3 T;
  tf::Quaternion R;

  //referance frame is BASE  
//  for(int i = 0; i<6; i++){
//    if(i == 0 ){
//      T.setValue(0, 0, 2.13 - 2.1);
//      R.setRPY(0, 0, 0);
//    }
//    if(i == 1){
//      T.setValue(-0.25, 0.239 + 0.7525, -0.14);
//      R.setRPY(M_PI/2, 0, 0);
//    }
//    if(i == 2){
//      T.setValue(0, -0.1648 - 0.75, 0);
//      R.setRPY(M_PI/2, 0, 0);
//    }
//    if(i == 3){
//      T.setValue(0, -0.0465 - 0.83, 0);
//      R.setRPY(M_PI/2, 0, 0);
//    }
//    if(i == 4){
//      T.setValue(0, -0.0473 - 0.171, 0);
//      R.setRPY(M_PI/2, 0, 0);
//    }
//    if(i == 5){
//      T.setValue(0.063 + 0.0475, 0.184, 0.07);
//      R.setRPY(0, M_PI/2, 0);
//    }
//    transform.setOrigin(T);
//    transform.setRotation(R);
//    representations[i]->transform2frames_base = transform;
//  }

  //referance frame is COM
  for(int i = 0; i<6; i++){
    if(i == 0 ){
      T.setValue(0, 0, 2.13);
      R.setRPY(0, 0, 0);
    }
    if(i == 1){
      T.setValue(-0.25, 0.239, -0.14);
      R.setRPY(M_PI/2, 0, 0);
    }
    if(i == 2){
      T.setValue(0, -0.1648, 0);
      R.setRPY(M_PI/2, 0, 0);
    }
    if(i == 3){
//      T.setValue(0, -0.0465, 0); //original
      T.setValue(0.031, -0.0465, -0.053);
      R.setRPY(M_PI/2, 0, 0);
    }
    if(i == 4){
      T.setValue(0, -0.0473, 0);
      R.setRPY(M_PI/2, 0, 0);
    }
    if(i == 5){
      T.setValue(0.063, 0.184, 0.07);
      R.setRPY(0, M_PI/2, 0);
    }
    transform.setOrigin(T);
    transform.setRotation(R);
    representations[i]->transform2frames_center = transform;
  }

  return 6;
}

int RobotRepresentation::getParam(int index, string par){

  return representations[index]->getParam(par);
}

vector<RobotRepresentation::robotInfo> RobotRepresentation::getRobot(){

  return robot;
}

string RobotRepresentation::getRootFrame(){

  return rootFrameName;
}

//tf::StampedTransform RobotRepresentation::getTransform(int index){

//  return representations[index]->getTransform();
//}

void RobotRepresentation::updateTransform(vector<tf::StampedTransform> robotFrames){

  for(int i=0; i<4; i++){
//    representations[i]->transform2world_base.mult(robotFrames[i], representations[i]->transform2frames_base);
    representations[i]->transform2world_center.mult(robotFrames[i], representations[i]->transform2frames_center);
  }
}
