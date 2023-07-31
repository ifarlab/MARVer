#ifndef CYLINDER_H
#define CYLINDER_H

#include <PrimitiveGeometry.h>

namespace RVServiceTool_OHT{

class Cylinder: public PrimitiveGeometry{

  private:
    const double radius;
    const double height;

  public:

    Cylinder(double r=0, double h=0): PrimitiveGeometry("cylinder"), radius(r), height(h) {};

    double getParam(string par);
};

}

#endif
