#include <PrimitiveGeometry.h>
#include <tf/transform_listener.h>

//using namespace std;
using namespace RVServiceTool_ODT;

PrimitiveGeometry::PrimitiveGeometry(string _type){
  type = _type;
}

//tf::StampedTransform PrimitiveGeometry::getTransform(){

//  return transform2frames;
//}


string PrimitiveGeometry::getType(){

  return type;
}

