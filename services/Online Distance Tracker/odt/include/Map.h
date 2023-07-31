#ifndef MAP_H
#define MAP_H

#include <iostream>
#include <octomap/octomap.h>
#include <octomap/OcTree.h>
#include <string>
#include <vector>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fstream>
#include <filesystem>

#include <eigen3/Eigen/Eigen>
#include <eigen3/Eigen/Core>

using namespace std;

namespace RVServiceTool_ODT{

class Map{ 
	
	private:

		octomap::OcTree* tree;
		
	public:

		Map ();

		void load(string inputFilename);

		void insertPointCloud(string PCDFiles);		

		octomap::OcTree* getTree();
};

}

#endif
