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
#include <HumanDistanceCalculation.h>
#include <Human.h>

using namespace std;
using namespace fcl;
using namespace RVServiceTool_OHT;
using namespace tdv::nuitrack;


Human::Human(int id_)
{
	id = id_;

}

Human::~Human()
{
	 
}

int Human::getId()
{
	return id;
	
}

std::vector<tdv::nuitrack::Joint> Human::getJoints ()
{
	return joints;
	
}

void Human::setJoints (const std::vector<tdv::nuitrack::Joint>& joints_)
{
	joints = joints_;
	
}

double Human::minDistance()
{
	double smallest = *min_element(minDistances.begin(), minDistances.end());
	return smallest;		
}


void Human::getMinMarkerP1(int index, double &dx, double &dy, double &dz)
{
  //usage min_marker_from[0][0], min_marker_from[0][1], min_marker_from[0][2]
  //      min_marker_from[1][0], min_marker_from[1][1], min_marker_from[1][2]
  // ...
  //return minDistP1[index];
  dx = minDistP1[index].x();
  dy = minDistP1[index].y();
  dz = minDistP1[index].z();
}

void Human::getMinMarkerP2(int index, double &dx, double &dy, double &dz)
{
  //usage min_marker_to[0][0], min_marker_to[0][1], min_marker_to[0][2]
  //      min_marker_to[1][0], min_marker_to[1][1], min_marker_to[1][2]
  // ...
  dx = minDistP2[index].x();
  dy = minDistP2[index].y();
  dz = minDistP2[index].z();
}

std::vector<double> Human::getMinDistances()
{
	return this->minDistances;
}


void Human::setMinDistances(const std::vector<double> vec)
{
  this->minDistances = vec;
}











