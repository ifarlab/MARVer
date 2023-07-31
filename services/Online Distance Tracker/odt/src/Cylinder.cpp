#include <Cylinder.h>

using namespace RVServiceTool_ODT;

double Cylinder::getParam(string par){

  if(par == "radius")
      return radius;
  else if(par == "height")
      return height;
  else
    return -1;
}

