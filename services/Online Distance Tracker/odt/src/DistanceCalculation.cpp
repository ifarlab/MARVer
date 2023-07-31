#include "DistanceCalculation.h"

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

using namespace std;
using namespace fcl;
using namespace RVServiceTool_ODT;

DistanceCalculation::DistanceCalculation(Map* _map, RobotRepresentation* robotRepresentation_)
{
  map = _map;
	robotRepresentation = robotRepresentation_;
	for (int i = 0; i < 4; i++)
		minDistances.push_back(DBL_MAX); 

  octree = map->getTree();
}

vector<double> DistanceCalculation::getMinDistances()
{
	return minDistances;
}

void DistanceCalculation::setBbx_min_max()
{
	//double width = 4.2; 
	//double depth = 1.4;
	//double height = 4.4;

  double x_min = -0.2;
  double y_min = -1.7;
//  double y_min = -5;
	double z_min = -0.2;
		
  double x_max = 0.3;
//  double x_max = 14;
  double y_max = 0.5;
	double z_max = 1.5;
	
	
  Matrix3d rotation(
                    AngleAxisd(0, Eigen::Vector3d::UnitX())
                  * AngleAxisd(0, Eigen::Vector3d::UnitY())
                  * AngleAxisd(0, Eigen::Vector3d::UnitZ()));


	
  Transform3d tf_min;
  Transform3d tf_max;
  Transform3d tf_result;
  	//düzenlenecek: cylinder 
  Transform3d tf_center;
  //tf::StampedTransform tf_center_tmp = robotRepresentation->getTransform(0);
  tf::StampedTransform tf_center_tmp = robotRepresentation->representations[0]->transform2world_center;

  tf_center.setIdentity();
  tf_center.translation() = Eigen::Vector3d (tf_center_tmp.getOrigin().getX(),
                                             tf_center_tmp.getOrigin().getY(),
                                             tf_center_tmp.getOrigin().getZ());

//  tf_center.linear() = (Eigen::Quaterniond (tf_center_tmp.getRotation().getX(),
//                                            tf_center_tmp.getRotation().getY(),
//                                            tf_center_tmp.getRotation().getZ(),
//                                            tf_center_tmp.getRotation().getW())).toRotationMatrix();

  tf_center.linear() = (Eigen::Quaterniond (tf_center_tmp.getRotation())).toRotationMatrix();

//   std::cout << "tf_center linear()\n" << tf_center.linear() << std::endl;

  tf_min.setIdentity();
  tf_min.linear() = rotation;
  tf_min.translation() = Vector3d (x_min, y_min, z_min);

  tf_max.setIdentity();
  tf_max.linear() = rotation;
  tf_max.translation() = Vector3d (x_max, y_max, z_max);

  tf_result.setIdentity();
  tf_result.linear() = rotation;
  tf_result.translation() = Vector3d (0, 0, 0);

  tf_result = tf_min*tf_center;

  octomap::point3d min_ ((double)tf_result.translation().x(), (double)tf_result.translation().y(), (double)tf_result.translation().z());
	min =  min_;
	
	tf_result = tf_max*tf_center;
	
	octomap::point3d max_ ((double)tf_result.translation().x(), (double)tf_result.translation().y(), (double)tf_result.translation().z());
	max = max_;
  	
}

void DistanceCalculation::calculateMinDistances()
{
	//get tree
  //octomap::OcTree* tree = map->getTree();
//	if(!tree)
//	{
//		cout << "------ ERROR" << endl;
//	}
	  
  setBbx_min_max();
	  
	//düzenlenecek
  double radius;
  double height;
  fcl::Transform3d tf_center;
  CollisionObject<double>* cylinder[4];

  for(int i = 0; i<4; i++){

    radius = robotRepresentation->representations[i]->getParam("radius");
    //height = 2*robotRepresentation->representations[i]->getParam("height");
    height = robotRepresentation->representations[i]->getParam("height");

//    if(i == 5)
//      height = 2*height;

    //tf::StampedTransform tf_center_tmp = robotRepresentation->getTransform(i);
    //tf::StampedTransform tf_center_tmp = robotRepresentation->representations[i]->transform2world_base;
    tf::StampedTransform tf_center_tmp = robotRepresentation->representations[i]->transform2world_center;

//    if(i == 8){
//      tf_center_tmp = robotRepresentation->representations[i]->transform2world_center;
//    }

    tf_center.setIdentity();
    tf_center.translation() = Eigen::Vector3d (tf_center_tmp.getOrigin().getX(),
                                               tf_center_tmp.getOrigin().getY(),
                                               tf_center_tmp.getOrigin().getZ());

//    tf_center.linear() = (Eigen::Quaterniond (tf_center_tmp.getRotation().getX(),
//                                              tf_center_tmp.getRotation().getY(),
//                                              tf_center_tmp.getRotation().getZ(),
//                                              tf_center_tmp.getRotation().getW())).toRotationMatrix();

    tf_center.linear() = (Eigen::Quaterniond (tf_center_tmp.getRotation())).toRotationMatrix();

    std::shared_ptr<fcl::CollisionGeometry<double>> cylinder_geometry(new fcl::Cylinder<double>(radius, height));
    cylinder[i] = new CollisionObject<double>(cylinder_geometry, tf_center);
  }

  DistanceRequest<double> request;
  DistanceResult<double> result;

//  octomap::OcTreeKey minKey, maxKey;
//   if (!octree->coordToKeyChecked(min, minKey) || !octree->coordToKeyChecked(max, maxKey)){

//   }

//   for(octomap::OcTree::leaf_iterator it = octree->begin_leafs(),end=octree->end_leafs(); it!= end; ++it){
//      // check if outside of bbx:
//      octomap::OcTreeKey k = it.getKey();
//      if  (k[0] > minKey[0] || k[1] > minKey[1] || k[2] > minKey[2]
//          || k[0] < maxKey[0] || k[1] < maxKey[1] || k[2] < maxKey[2]){
//          cout << "icerde***"<< endl;
//      }
//    }

//  double temp_x, temp_y, temp_z;
//  octree->getMetricMin(temp_x, temp_y, temp_z);
//  octomap::point3d bbx_min(temp_x, temp_y, temp_z);
//  octree->getMetricMax(temp_x, temp_y, temp_z);
//  octomap::point3d bbx_max(temp_x, temp_y, temp_z);

  octomap::OcTree::leaf_bbx_iterator it = octree->begin_leafs_bbx(min,max);
  octomap::OcTree::leaf_bbx_iterator end = octree->end_leafs_bbx();

  for (int i = 0; i < 4; i++)
    minDistances[i]=DBL_MAX;

  if(it == end){

    cout << "it == end***"<< endl;
  }
  
  
  //for(octomap::OcTree::leaf_iterator it = octree->begin_leafs(),end=octree->end_leafs(); it!= end; ++it)
  for(; it!= end; ++it)
  {

    if(octree->isNodeOccupied(*it))
    {
      octomap::point3d point = it.getCoordinate();

      double x = point.x();
      double y = point.y();
      double z = point.z();
      double size = it.getSize();
      double cost = (*it).getOccupancy();
      double threshold = octree->getOccupancyThres();

      Box<double>* box = new Box<double>(size, size, size);
      box->cost_density = cost;
      box->threshold_occupied = threshold;
      CollisionObject<double>* box_ = new CollisionObject<double>(std::shared_ptr<CollisionGeometry<double>>(box), Transform3d(Translation3d(Vector3d(x, y, z))));

      request.gjk_solver_type = fcl::GJKSolverType::GST_INDEP;
      //request.gjk_solver_type = fcl::GJKSolverType::GST_LIBCCD;

//EG: bu comment leri acip calistirdigimizda sonucta degisiklik olmadi ya da farkedemedim.
//Tam olarak ne yaptiklari arastirilacak, internetteki orneklerde hep kullanilmis
//      request.enable_nearest_points = true;
//      request.enable_signed_distance = true;

      for(int i = 0; i < 4; i++){
//      for(int i = 0; i < 1; i++){

        distance(cylinder[i], box_, request, result);

        if (minDistances[i] > result.min_distance){

          minDistances[i] = result.min_distance;
          minDistP1[i] = result.nearest_points [0];
          minDistP2[i] = result.nearest_points [1];
        }
        result.clear();
      }
//      distance(cylinder[0], box_, request, result);
//      if (minDistances.at(0) > result.min_distance){
//        minDistances.at(0) = result.min_distance;
//        minDistP1[0] = result.nearest_points [0];
//        minDistP2[0] = result.nearest_points [1];
//      }
//      result.clear();
//      distance(cylinder[1], box_, request, result);
//      if (minDistances.at(1) > result.min_distance){
//        minDistances.at(1) = result.min_distance;
//        minDistP1[1] = result.nearest_points [0];
//        minDistP2[1] = result.nearest_points [1];
//      }
//        result.clear();
//      distance(cylinder[2], box_, request, result);
//      if (minDistances.at(2) > result.min_distance)
//        minDistances.at(2) = result.min_distance;
//      result.clear();
//      distance(cylinder[3], box_, request, result);
//      if (minDistances.at(3) > result.min_distance)
//        minDistances.at(3) = result.min_distance;
//      result.clear();
//      distance(cylinder[4], box_, request, result);
//      if (minDistances.at(4) > result.min_distance)
//        minDistances.at(4) = result.min_distance;
//      result.clear();
//      distance(cylinder[5], box_, request, result);
//      if (minDistances.at(5) > result.min_distance)
//        minDistances.at(5) = result.min_distance;
//      result.clear();

    }
  }
}

double DistanceCalculation::minDistance()
{
	double smallest = *min_element(minDistances.begin(), minDistances.end());
	return smallest;		
}


void DistanceCalculation::getMinMarkerP1(int index, double &dx, double &dy, double &dz)
{
  //usage min_marker_from[0][0], min_marker_from[0][1], min_marker_from[0][2]
  //      min_marker_from[1][0], min_marker_from[1][1], min_marker_from[1][2]
  // ...
  //return minDistP1[index];
  dx = minDistP1[index].x();
  dy = minDistP1[index].y();
  dz = minDistP1[index].z();
}

void DistanceCalculation::getMinMarkerP2(int index, double &dx, double &dy, double &dz)
{
  //usage min_marker_to[0][0], min_marker_to[0][1], min_marker_to[0][2]
  //      min_marker_to[1][0], min_marker_to[1][1], min_marker_to[1][2]
  // ...
  dx = minDistP2[index].x();
  dy = minDistP2[index].y();
  dz = minDistP2[index].z();
}


