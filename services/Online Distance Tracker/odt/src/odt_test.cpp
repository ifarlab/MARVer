//for testing online distance calculation

#include <octomap/octomap.h>
#include <octomap/OcTree.h>


#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string.h>
#include <iomanip>
#include <sstream>

#include <Eigen/Eigen>
#include <Eigen/Core>

//#include <Map.h>
#include <DistanceCalculation.h>
#include <RobotRepresentation.h>

#include <fcl/narrowphase/collision_object.h>
#include <fcl/narrowphase/distance.h>
#include <fcl/narrowphase/distance_request.h>
#include <fcl/narrowphase/distance_result.h>
#include <fcl/math/constants.h>
#include <fcl/narrowphase/collision.h>
#include <fcl/geometry/octree/octree.h>

#include <chrono>
using namespace std::chrono;

using namespace std;
using namespace fcl;
using namespace RVServiceTool_ODT;



int main(int /*argc*/, char** /*argv*/)
{
  // default values:
  string inputFilename = "/home/s216/project/src/otokar_pcd_v3_shifted.bt";
  cout << "--" << inputFilename << endl;
  
  Map* map = new Map();
  map->load(inputFilename);

  RobotRepresentation* robotRepresentation();

  DistanceCalculation *calc = new DistanceCalculation(map, robotRepresentation);
  
  auto start2 = high_resolution_clock::now();
  
  calc->minDistances ();
		
  auto stop2 = high_resolution_clock::now();
  auto duration2 = duration_cast<microseconds>(stop2 - start2);
   
  double run_time = duration2.count();
  cout << endl;
  cout <<"*** Calculation duration (microseconds): " << run_time  << endl;	
  cout <<"*** Calculation duration (seconds): " << run_time/1000000  << endl;
  cout << endl;	
  
  cout << "---Calculated minimum distance: " << calc->minDistance() << endl;

  return 0;
}

