#ifndef HUMAN_H
#define HUMAN_H

#include <iostream>
#include <stdlib.h>
#include <iomanip>
#include <vector>
#include <float.h>
#include <limits.h>
#include <algorithm>
#include <string>

#include <Eigen/Eigen>
#include <Eigen/Core>


#include <fcl/narrowphase/collision_object.h>
#include <fcl/narrowphase/distance.h>
#include <fcl/narrowphase/distance_request.h>
#include <fcl/narrowphase/distance_result.h>
#include <fcl/math/constants.h>
#include <fcl/narrowphase/collision.h>


//for nuitrack
#include <nuitrack/Nuitrack.h>
#include <PrimitiveGeometry.h>

using namespace std;

namespace RVServiceTool_OHT{

class Human { 
	
	private:
				
		int id;
		std::vector<tdv::nuitrack::Joint> joints;
		std::vector<double> minDistances;
				
  	public:
  	
  		fcl::Vector3<double> minDistP1[4];
		fcl::Vector3<double> minDistP2[4];
		
		Human(int id_);
		~Human();

		int getId();
		std::vector<tdv::nuitrack::Joint> getJoints ();
		void setJoints (const std::vector<tdv::nuitrack::Joint>& joints);

  		//return the calculated min distances for each cylinder
  		std::vector<double> getMinDistances();
  		void setMinDistances(std::vector<double> vec);
	
  		
  		//return smallest distances out of six distance value
  		double minDistance();
		
		//get each of cylinder min distances from to marker information
		void getMinMarkerP1(int index, double &dx, double &dy, double &dz);
		void getMinMarkerP2(int index, double &dx, double &dy, double &dz);
		
		
		std::vector<double> humanTorso;
		

};

}

#endif
