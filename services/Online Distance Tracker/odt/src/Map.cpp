#include "Map.h"

#include <iostream>
#include <octomap/octomap.h>
#include <octomap/OcTree.h>
#include <string>
#include <vector>

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
using namespace RVServiceTool_ODT;

Map::Map()
{

}

void Map::load(string inputFilename)
{
	octomap::OcTree* tree_ = new octomap::OcTree(inputFilename);
        
        if(!tree_)
        {
		cout << "------ ERROR" << endl;
        }
	
	tree = tree_;		
}

void Map::insertPointCloud(string PCDFiles)
{
//	string saveFilename = "otokar_pcd_v2.bt";
//	octomap::OcTree* tree_;

//	string PCDFiles = PCDFiles;
//	vector<string> PCDfileList;
			
//	DIR *d;
//	struct dirent *dir;
//	string readFileName;

//	d=opendir(PCDFiles.c_str());
//	if(d!=NULL){
//		while ((dir = readdir(d)) != NULL) {
//			readFileName.assign(dir->d_name);
//			if(readFileName!="." && readFileName!=".."){
//				readFileName=PCDFiles+"/"+readFileName;
//				PCDfileList.push_back(readFileName);
//			}
//		}
//		closedir(d);
//	}

//	tree_ = new octomap::OcTree(0.05);

//	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);

//	for(unsigned long i=0;i<PCDfileList.size();i++){

//		if(pcl::io::loadPCDFile<pcl::PointXYZ> (PCDfileList[i].c_str(), *cloud) == -1){ //* load the file
//			PCL_ERROR ("Couldn't read file test_pcd.pcd \n");
//			return (-1);
//		}

//		for (const auto& point: *cloud){
//			tree_->updateNode(static_cast<double>(point.x/1000),static_cast<double>(point.y/1000),static_cast<double>(point.z/1000),true,true);
//		}
		
//		cloud->clear();
//		cout<<"FILE: "<<PCDfileList[i]<<" loaded... "<<i<<"/"<<PCDfileList.size()<<endl;
//	}

//	tree_->updateInnerOccupancy();
//	tree_->writeBinary(saveFilename);
			
//	tree = tree_;

}

octomap::OcTree* Map::getTree()
{
	return tree;		
}

