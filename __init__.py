import logging
import pandas as pd
from ete3 import PhyloTree,Tree,NodeStyle,TreeStyle,TextFace,RectFace
import random
import numpy as np
import os
import shutil
from tqdm import tqdm

def generate_sps_voucher(sps_num:int) -> list:
    characters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
    unique_strings = set()

    while len(unique_strings) < sps_num:
        unique_strings.add(''.join(random.sample(characters, 3)))

    return sorted(list(unique_strings))


def gene_id_transfer(gene2taxa_list:str) -> dict:
    gene2taxa_dic = read_and_return_dict(gene2taxa_list)
    sorted_gene2taxa_dic = dict(sorted(gene2taxa_dic.items())) 
    
    taxa_list = list(set(sorted_gene2taxa_dic.values()))
    taxa2voucher_dic = dict(zip(taxa_list, generate_sps_voucher(len(taxa_list))))
    voucher2taxa_dic = {value: key for key, value in taxa2voucher_dic.items()}
    gene_count = {}

    for species in sorted_gene2taxa_dic.values():
        gene_count[species] = gene_count.get(species, 0) + 1

    new_gene_names = [f"{taxa2voucher_dic[species]}_{i}" for species, count in gene_count.items() for i in range(1, count + 1)]
    gene2new_named_gene_dic = dict(zip(sorted_gene2taxa_dic.keys(), new_gene_names))
    new_named_gene2gene_dic = {value: key for key, value in gene2new_named_gene_dic.items()}
    return gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic
#gene2new_named_gene_dic, new_named_gene2gene_dic,voucher2taxa_dic=gene_id_transfer("gene2taxa.list")

def read_and_return_dict(filename, separator="\t") -> dict:
    df=pd.read_csv(filename,sep=separator,header=None)
    return df.set_index([0])[1].to_dict()

def rename_input_tre(Phylo_t:object, gene2new_named_gene_dic:dict) -> object:
    Phylo_t1=Phylo_t.copy('newick')
    for node in Phylo_t1.traverse():
        if node.name in gene2new_named_gene_dic.keys():
            node.name = gene2new_named_gene_dic[node.name]
    return Phylo_t1

def read_tree(tre_path:str) -> object:
    return Tree(tre_path)

def read_phylo_tree(tre_path:str) -> object:
    return PhyloTree(tre_path)
######################################################################################################################
def is_rooted(Phylo_t:object)->bool:#Translate the function that determines whether the input phylogenetic tree has a negated root.
    if len(Phylo_t.get_children()) ==2:
        return True

def root_tre_with_midpoint_outgroup(Phylo_t:object)->object:#Rooting the phylogenetic tree using the midpoint outgroup method.
    Phylo_t1=Phylo_t.copy('newick')
    mid_node=Phylo_t1.get_midpoint_outgroup()
    Phylo_t1.set_outgroup(mid_node)
    return Phylo_t1

def find_dup_node(Phylo_t:object)->list:#After searching for duplication events, the list of node names where duplication events occurred is as follows:
    events = Phylo_t.get_descendant_evol_events()
    dup_node_name_list = []
    for ev in events:
        if ev.etype == "D":
            i = ",".join(ev.in_seqs) + ',' + ",".join(ev.out_seqs)
            events_node_name_list = i.split(',')
            common_ancestor_node_name = Phylo_t.get_common_ancestor(events_node_name_list)
            dup_node_name_list.append(common_ancestor_node_name.name)
    return dup_node_name_list

def num_tre_node(Phylo_t:object)->object:#Numbering the nodes in the tree.
    i = 0
    for node in Phylo_t.traverse('postorder'):
        if not node.is_leaf():
            node.name = "N" + str(i)
            i += 1
    return Phylo_t

def get_species_list(node):
    if node is None:
        return []  # or any other appropriate default value
    return [leaf.name.split('_')[0] for leaf in node.iter_leaves()]

def get_species_set(Phylo_t:object)->set:
    return set(get_species_list(Phylo_t))

def get_max_deepth(root:object)->int:
    if not root:
        return 0
    
    max_child_depth = 0
    for child in root.children:
        child_depth = get_max_deepth(child)
        max_child_depth = max(max_child_depth, child_depth)
    
    return max_child_depth + 1

def compute_tip_to_root_branch_length_variance(tree:object)->int:
    tip_to_root_branch_lengths = []
    for leaf in tree.iter_leaves():
        branch_length = tree.get_distance(leaf)
        tip_to_root_branch_lengths.append(branch_length)

    branch_length_variance = 0
    if len(tip_to_root_branch_lengths) > 1:
        variance=float(np.var(tip_to_root_branch_lengths))
        branch_length_variance = variance

    return branch_length_variance

def calculate_species_overlap(gene_tree:object)->int:
    up_clade=gene_tree.children[1]
    down_clade=gene_tree.children[0]
    species_list_a = get_species_list(up_clade)
    species_list_b = get_species_list(down_clade)
    overlap_ratio = len(set(species_list_a) & set(species_list_b)) / len(set(species_list_a) | set(species_list_b))

    return overlap_ratio

def calculate_species_num(node:object)->int:# Obtain the number of species under a node
    species_num=len(get_species_set(node))
    return species_num

def calculate_gd_num(Phylo_t:object)->int:
    gd_num=0
    gd_node_names=find_dup_node(Phylo_t)
    for node in gd_node_names:
        clade=Phylo_t&node
        sps=[leaf.split('_')[0] for leaf in clade.get_leaf_names()]
        unique_sps=set(sps)
        if len(unique_sps) >5:
            if sps_dup_num(sps,unique_sps) > len(unique_sps)*0.2:
                gd_num+=1
        else:
            if sps_dup_num(sps,unique_sps) >=1:
                gd_num+=1
    
    return gd_num

def sps_dup_num(sps_list: list, unique_sps: list) -> int:
    sps_num_dic = {i: 0 for i in unique_sps}
    sps_dups = 0

    for sps in sps_list:
        if sps in sps_num_dic:
            sps_num_dic[sps] += 1
            if sps_num_dic[sps] == 2:
                sps_dups += 1

    return sps_dups


def find_tre_dup(Phylo_t:object) -> list:   #seperator either "@" or "_"
    tre_ParaL=[]
    GF_leaves_S = set(Phylo_t.get_leaf_names())
    events = Phylo_t.get_descendant_evol_events()
    for ev in events:
        if ev.etype == "D":
            tre_ParaL.append(",".join(ev.in_seqs)+"<=>"+",".join(ev.out_seqs))
    return tre_ParaL,GF_leaves_S
