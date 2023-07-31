#ifndef PRIMITIVEGEOMETRY_H
#define PRIMITIVEGEOMETRY_H

//#include <fcl/narrowphase/collision_object.h>
#include <tf/transform_datatypes.h>

using namespace std;

namespace RVServiceTool_OHT{

class PrimitiveGeometry{

  private:

    string type;

  public:

    PrimitiveGeometry(string _type);

    string getType();

    virtual double getParam(string) = 0;

//    fcl::Transform3d getTransform();

//    fcl::Transform3d transform2world;

//    tf::StampedTransform getTransform();

//    tf::StampedTransform transform2world_base;

    tf::StampedTransform transform2world_center;

//    tf::StampedTransform transform2frames_base;

    tf::StampedTransform transform2frames_center;

};


}

#endif
