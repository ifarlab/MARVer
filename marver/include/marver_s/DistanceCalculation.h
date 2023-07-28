#ifndef DISTANCECALCULATION_H
#define DISTANCECALCULATION_H

#include <octomap/octomap.h>
#include <octomap/OcTree.h>

#include <iostream>
#include <stdlib.h>
#include <iomanip>
#include <vector>
#include <float.h>
#include <limits.h>
#include <algorithm>

#include <Eigen/Eigen>
#include <Eigen/Core>

#include <fcl/narrowphase/collision_object.h>
#include <fcl/narrowphase/distance.h>
#include <fcl/narrowphase/distance_request.h>
#include <fcl/narrowphase/distance_result.h>
#include <fcl/math/constants.h>
#include <fcl/narrowphase/collision.h>
#include <fcl/geometry/octree/octree.h>

#include <Map.h>
#include <RobotRepresentation.h>

using namespace std;

namespace RVServiceTool_ODT{

class DistanceCalculation { 

	private:

		Map* map; 
    octomap::OcTree* octree;
		RobotRepresentation* robotRepresentation;
    vector<double> minDistances;
    fcl::Vector3<double> minDistP1[6];
    fcl::Vector3<double> minDistP2[6];

public:

		octomap::point3d min;
		octomap::point3d max;
 
  	public:

  		DistanceCalculation(Map* map, RobotRepresentation* robotRepresentation);

  		//return the calculated min distances for each cylinder
  		vector<double> getMinDistances();

  		//for selecting leaves belong to specific area
  		void setBbx_min_max();

  		//calculation distances for six cylinder
      void calculateMinDistances();

  		//return smallest distances out of six distance value
  		double minDistance();

      //get each of cylinder min distances from to marker information
      void getMinMarkerP1(int index, double &dx, double &dy, double &dz);
      void getMinMarkerP2(int index, double &dx, double &dy, double &dz);

};

}

#endif
