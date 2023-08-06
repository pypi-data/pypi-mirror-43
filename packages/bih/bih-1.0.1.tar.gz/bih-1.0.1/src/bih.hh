/*!
 *
 * Copyright (C) 2015 Technical University of Liberec.  All rights reserved.
 * 
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License version 3 as published by the
 * Free Software Foundation. (http://www.gnu.org/licenses/gpl-3.0.en.html)
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * 
 * @file    bih_tree.hh
 * @brief   
 */

#ifndef BIH_TREE_HH_
#define BIH_TREE_HH_

#include "bih_node.hh"
//#include "mesh/mesh.h"
//#include "mesh/point.hh"
//#include <armadillo>



/**
 * @brief Class for O(log N) lookup for intersections with a set of bounding boxes.
 *
 * Notes:
 * Assumes spacedim=3. Implementation was designed for arbitrary number of childs per node, but
 * currently it supports max 2 childs per node (binary tree).
 *
 */
class BIHTree {
public:
    /// count of dimensions
    static const unsigned int dimension = 3;
    /// max count of elements to estimate median - value must be even
    static const unsigned int max_median_sample_size = 5;

    /**
	 * Constructor
	 *
	 * Set class members and call functions which create tree
	 * @param mesh  - Mesh used for creation the tree
	 * @param soft_leaf_size_limit - Maximal number of elements stored in a leaf node of BIH tree.
	 */
	BIHTree(unsigned int soft_leaf_size_limit = 20);

	void add_boxes(const std::vector<BoundingBox> &boxes);

	void construct();

	/**
	 * Destructor
	 */
	~BIHTree();

	/**
	 * Get count of elements stored in tree
	 *
	 * @return Count of bounding boxes stored in elements_ member
	 */
    unsigned int get_element_count() const;

    /**
     * Main bounding box of the whole tree.
     */
    const BoundingBox &tree_box() const;

	/**
	 * Gets elements which can have intersection with bounding box
	 *
	 * @param boundingBox Bounding box which is tested if has intersection
	 * @param result_list vector of ids of suspect elements
	 * @param full_list put to result_list all suspect elements found in leaf node or add only those that has intersection with boundingBox
	 */
    void find_bounding_box(const BoundingBox &boundingBox, std::vector<unsigned int> &result_list, bool full_list = false) const;

	/**
	 * Gets elements which can have intersection with point
	 *
	 * @param point Point which is tested if has intersection
	 * @param result_list vector of ids of suspect elements
	 * @param full_list put to result_list all suspect elements found in leaf node or add only those that has intersection with point
	 */
    void find_point(const Point &point, std::vector<unsigned int> &result_list, bool full_list = false) const;

    /**
     * Get vector of mesh elements bounding boxes
     *
     * @return elements_ vector
     */
    std::vector<BoundingBox> &get_elements() { return elements_; }
    
    /// Gets bounding box of element of given index @p ele_index.
    const BoundingBox & ele_bounding_box(unsigned int ele_idx) const;

protected:
    /// required reduction in size of box to allow further splitting
    static const double size_reduce_factor;

    /// create bounding boxes of element
    //void element_boxes();

    /// split tree node given by node_idx, distribute elements to child nodes
    void split_node(const BoundingBox &node_box, unsigned int node_idx);

    /// create child nodes of node given by node_idx
    void make_node(const BoundingBox &box, unsigned int node_idx);

    /**
     * For given node takes projection of centers of bounding boxes of its elements to axis given by
     * @p node::axis()
     * and estimate median of these values. That is optimal split point.
     * Precise median is computed for sets smaller then @p max_median_sample_size
     * estimate from random sample is used for larger sets.
     */
    double estimate_median(unsigned char axis, const BIHNode &node);

    /// mesh
    //Mesh* mesh_;
	/// vector of mesh elements bounding boxes (from mesh)
    std::vector<BoundingBox> elements_;
    /// Main bounding box. (from mesh)
    BoundingBox main_box_;

    /// vector of tree nodes
    std::vector<BIHNode> nodes_;
    /// Maximal number of elements stored in a leaf node of BIH tree.
    unsigned int leaf_size_limit;
    /// Maximal count of BIH tree levels
    unsigned int max_n_levels;

    /// vector stored element indexes in leaf nodes
    std::vector<unsigned int> in_leaves_;
    /// temporary vector stored values of coordinations for calculating median
    std::vector<double> coors_;

    // random generator
    //std::mt19937	r_gen;


};

#endif /* BIH_TREE_HH_ */
