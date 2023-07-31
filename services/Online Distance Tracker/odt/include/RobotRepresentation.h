#ifndef ROBOTREPRESENTATION_H
#define ROBOTREPRESENTATION_H

#include <PrimitiveGeometry.h>

//using namespace std;

namespace RVServiceTool_ODT{

class RobotRepresentation{

  private:

//    string robotName;
//    string configFile;
    string robotBrand;
    string robotModel;
    string rootFrameName;

    struct robotInfo{

      string cylinderName;
      string cylinderId;
      double radius;
      double height;
      string frameName;
      string frameId;
      vector<double> rotation;
      vector<double> translation;
    } robot_info;

    vector<robotInfo> robot;

  public:

    int loadGeometry();

    void loadGeometry(string fileName); //*

    void parseXML(string fileName); //*

    vector<robotInfo> getRobot(); //*

    string getRootFrame(); //*

    int getParam(int index, string par);

//    fcl::Transform3d getTransform(int index);
//    tf::StampedTransform getTransform(int index);

    void updateTransform(vector<tf::StampedTransform> robotFrames);

    vector<PrimitiveGeometry*> representations;

};

}

#endif
