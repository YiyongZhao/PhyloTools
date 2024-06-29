import sys, textwrap
import argparse
import time
from PhyloTree_CollapseExpand import *
from PhyloSupport_Scaler import *
from BranchLength_NumericConverter import *
from Phylo_Rooter import *
from OrthoFilter_LB import *
from OrthoFilter_Mono import *
from TreeTopology_Summarizer import *
from Tree_Visualizer import *
from GD_Detector import *
from GD_Visualizer import *
from GD_Loss_Tracker import *
from GD_Loss_Visualizer import *
from Ortho_Retriever import *
from Hybrid_Tracer import *
from Hybrid_Visualizer import *
from HaploFinder import *



from __init__ import *
##################################################################
print(textwrap.dedent("""
###############################################################################################
#                                                                                             #
# ██████╗ ██╗  ██╗██╗   ██╗██╗      ██████╗ ████████╗██████╗  █████╗  ██████╗███████╗██████╗  #
# ██╔══██╗██║  ██║╚██╗ ██╔╝██║     ██╔═══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗ #
# ██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║   ██║   ██████╔╝███████║██║     █████╗  ██████╔╝ #
# ██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██╗ #
# ██║     ██║  ██║   ██║   ███████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║ #
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝ # 
#                                                                                             #
#    PhyloTracer: A User-Friendly Toolkit for Gene Tree Rooting, Gene Duplication             #
#    Identification, Ortholog Retrieval, Phylogenetic Noise Elimination, Species              #
#    Hybridization Detection,and Visualization.                                               #
#                                                                                             #
#    Pypi: https://pypi.org/project/PhyloTracer                                               #
#    Github: https://github.com/YiyongZhao/PhyloTracer                                        #
#    Licence: MIT license                                                                     #
#    Release Date: 2023-7                                                                     #
#    Please cite: Li et al. 2024, XXXX.                                                       #
#    Contacts: Taoli(Taoli@gmail.com); Yiyong Zhao(yzhao@bwh.harvard.edu)                     #
#                                                                                             #
###############################################################################################
"""))

if sys.version_info.major==2:
    print('You are using Python 2. Please upgrade to Python 3. PhyloRoot quit now...')
    quit() 

# create a parameter parser
class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if action.dest == 'command':
            # Override the format of the subparsers
            choices = self._metavar_formatter(action, action.choices)
            return f"available programs:\n{''.join(choices)}\n"
        return super()._format_action(action)

parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter, add_help=False)
subparsers = parser.add_subparsers(dest='command', help='available programs:')


# PhyloTree_CollapseExpand command
PhyloTree_CollapseExpand_parser = subparsers.add_parser('PhyloTree_CollapseExpand', help='PhyloTree_CollapseExpand help')
PhyloTree_CollapseExpand_parser.add_argument('--input_GF_list', metavar='file', required=True, help='Input gene tree list')
PhyloTree_CollapseExpand_parser.add_argument('--support_value', type=int,required=True, help='If the support of the node is less than this value, it will be folded')
PhyloTree_CollapseExpand_parser.add_argument('--revert', action='store_true', help='Revert this comb structure back to a fully resolved binary tree')

# PhyloSupport_Scaler command
PhyloSupport_Scaler_parser = subparsers.add_parser('PhyloSupport_Scaler', help='PhyloSupport_Scaler help')
PhyloSupport_Scaler_parser.add_argument('--input_GF_list', metavar='file', required=True, help='Input gene tree list')
PhyloSupport_Scaler_parser.add_argument('--scale_to', type=str,  choices=['1', '100'],help='[1/100] you can only input 1 or 100 Whether to scale branch support information')

# BranchLength_NumericConverter command
BranchLength_NumericConverter_parser = subparsers.add_parser('BranchLength_NumericConverter', help='BranchLength_NumericConverter help')
BranchLength_NumericConverter_parser.add_argument('--input_GF_list', metavar='file', required=True, help='Input gene tree list')
BranchLength_NumericConverter_parser.add_argument('--decimal_place', type=int, help='Set how many decimal places to keep')

# Phylo_Rooter command
Phylo_Rooter_parser = subparsers.add_parser('Phylo_Rooter', help='Phylo_Rooter help')
Phylo_Rooter_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
Phylo_Rooter_parser.add_argument('--input_imap', metavar='file',  required=True, help='Input imap file')
Phylo_Rooter_parser.add_argument('--input_gene_length', metavar='file',  help='Input gene length list')
Phylo_Rooter_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree file')

# OrthoFilter_LB command
OrthoFilter_LB_parser = subparsers.add_parser('OrthoFilter_LB', help='OrthoFilter_LBr help')
OrthoFilter_LB_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
OrthoFilter_LB_parser.add_argument('--input_taxa', metavar='file',  required=True, help='Input taxa file')
OrthoFilter_LB_parser.add_argument('--long_branch_index', type=int, default=5, required=True, help='Long branch index')
OrthoFilter_LB_parser.add_argument('--visual', action='store_true', help='Visualize the results if set')

# OrthoFilter_Mono command
OrthoFilter_Mono_parser = subparsers.add_parser('OrthoFilter_Mono', help='OrthoFilter_Mono help')
OrthoFilter_Mono_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
OrthoFilter_Mono_parser.add_argument('--input_taxa', metavar='file',  required=True, help='Input taxa file')
OrthoFilter_Mono_parser.add_argument('--long_branch_index', type=int, default=5, required=True, help='Long branch index')
OrthoFilter_Mono_parser.add_argument('--insert_branch_index', type=int, default=5, required=True, help='Insert_branch_index')
OrthoFilter_Mono_parser.add_argument('--visual', action='store_true', help='Visualize the results if set')

# TreeTopology_Summarizer command
TreeTopology_Summarizer_parser = subparsers.add_parser('TreeTopology_Summarizer', help='TreeTopology_Summarizer help')
TreeTopology_Summarizer_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
TreeTopology_Summarizer_parser.add_argument('--input_imap', metavar='file',  required=True, help='Input imap file')
TreeTopology_Summarizer_parser.add_argument('--outfile', metavar='file',  required=True, help='Out filename')

# Tree_Visualizer command
Tree_Visualizer_parser = subparsers.add_parser('Tree_Visualizer', help='Tree_Visualizer help')
Tree_Visualizer_parser.add_argument('--input_GF_list', metavar='file', required=True, help='Input gene tree list')
Tree_Visualizer_parser.add_argument('--input_imap', metavar='file', required=True, help='Input imap file')
Tree_Visualizer_parser.add_argument('--species_categories', metavar='file', nargs='+',  help='Species category information')
Tree_Visualizer_parser.add_argument('--keep_branch', type=str,  choices=['1', '0'],help='[1/0] you can only input 1 or 0 Whether to preserve branch length information')
Tree_Visualizer_parser.add_argument('--tree_style',  choices=['r', 'c'],default='r', help='Tree style: [r/c] (rectangular) or (circular) (default: rectangular)')
Tree_Visualizer_parser.add_argument('--gene_family', metavar='file',  required=False, help='Input species tree file')
Tree_Visualizer_parser.add_argument('--input_sps_tree', metavar='file',  required=False, help='Input species tree file')
Tree_Visualizer_parser.add_argument('--gene_expression', metavar='file',  required=False, help='gene_expression')

# GD_Detector command
GD_Detector_parser = subparsers.add_parser('GD_Detector', help='GD_Detector help')
GD_Detector_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
GD_Detector_parser.add_argument('--input_imap', metavar='file',  required=True, help='Input imap file')
GD_Detector_parser.add_argument('--gd_support', type=int,required=True, help='GD node support [50-100]')
GD_Detector_parser.add_argument('--clade_support', type=int,required=True, help='The children support of GD node [0-100]')
GD_Detector_parser.add_argument('--dup_species_radio', type=float ,required=True,help='The proportion of species with species duplications under the GD node [0-1]')
GD_Detector_parser.add_argument('--dup_species_num', type=int ,required=True,help='The number of species with species duplications under the GD node')
GD_Detector_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree file')

# GD_Visualizer command
GD_Visualizer_parser = subparsers.add_parser('GD_Visualizer', help='GD_Visualizer help')
GD_Visualizer_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree filet')
GD_Visualizer_parser.add_argument('--gd_result', metavar='file',  required=True, help='The output of GD_Detector')

# GD_Loss_Tracker command
GD_Loss_Tracker_parser = subparsers.add_parser('GD_Loss_Tracker', help='GD_Loss_Tracker help')
GD_Loss_Tracker_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gf list')
GD_Loss_Tracker_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree filet')
GD_Loss_Tracker_parser.add_argument('--output_folder', type=str,  required=True, help='Output foldername')

# GD_Loss_Visualizer command
GD_Loss_Visualizer_parser = subparsers.add_parser('GD_Loss_Visualizer', help='GD_Loss_Visualizer help')
GD_Loss_Visualizer_parser.add_argument('--input_folder', type=str,  required=True, help='Input foldername')
GD_Loss_Visualizer_parser.add_argument('--output_folder', type=str,  required=True, help='Output foldername')

# Ortho_Retriever command
Ortho_Retriever_parser = subparsers.add_parser('Ortho_Retriever', help='Ortho_Retriever help')
Ortho_Retriever_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
Ortho_Retriever_parser.add_argument('--input_imap', metavar='file',  required=True, help='Input imap file')
Ortho_Retriever_parser.add_argument('--input_gene_length', metavar='file',  required=True, help='Input gene length list')

# Hybrid_Tracer
Hybrid_Tracer_parser = subparsers.add_parser('Hybrid_Tracer', help='Hybrid_Tracer help')
Hybrid_Tracer_parser.add_argument('--input_GF_list', metavar='file',  required=True, help='Input gene tree list')
Hybrid_Tracer_parser.add_argument('--input_Seq_GF_list', metavar='file',  required=True, help='Seq file list')
Hybrid_Tracer_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree file')
Hybrid_Tracer_parser.add_argument('--input_imap', metavar='file',  required=True, help='Input imap file')

# Hybrid_Visualizer
Hybrid_Visualizer_parser = subparsers.add_parser('Hybrid_Visualizer', help='Hybrid_Visualizer help')
Hybrid_Visualizer_parser.add_argument('--input_hybrid_folder', type=str,  required=True, help='The results of Hybrid_Tracer')
Hybrid_Visualizer_parser.add_argument('--input_sps_tree', metavar='file',  required=True, help='Input species tree file')

#HaploFinder
HaploFinder = subparsers.add_parser('HaploFinder', help='HaploFinder help')
HaploFinder.add_argument('--input_GF_list', metavar='FILE', required=True, help='Input gene tree list file')
HaploFinder.add_argument('--input_imap', metavar='FILE', required=True, help='Input imap file')
HaploFinder.add_argument('--species_a', type=str, required=True, help='Name of species A')
HaploFinder.add_argument('--species_b', type=str, required=True, help='Name of species B')
HaploFinder.add_argument('--species_a_gff', metavar='FILE', required=True, help='GFF file of species A')
HaploFinder.add_argument('--species_b_gff', metavar='FILE', required=True, help='GFF file of species B')
HaploFinder.add_argument('--species_a_lens', metavar='FILE', required=True, help='Lens file of species A')
HaploFinder.add_argument('--species_b_lens', metavar='FILE', required=True, help='Lens file of species B')
HaploFinder.add_argument('--blastp_result', metavar='FILE', required=True, help='Blastp result between species A and species B')
HaploFinder.add_argument('--synteny_result', metavar='FILE', required=True, help='Synteny result between species A and species B')
HaploFinder.add_argument('--blastp_limit', type=int, required=True, help='Limit number of targets per gene pair in the BLASTp result')

parser.add_argument('-h', '--help', action='store_true', help=argparse.SUPPRESS)
# Analyze command line parameters


args = parser.parse_args()

def format_time(seconds):
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(days)} d, {int(hours)} h, {int(minutes)} m, {seconds:.2f} s"

def main():
    if args.command == 'PhyloTree_CollapseExpand':
        # Execute the PhyloTree_CollapseExpand function
        if args.input_GF_list and args.support_value:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            support_value = args.support_value
            tre_dic = read_and_return_dict(input_GF_list)
            collapse_expand_main(tre_dic, support_value,revert=args.revert)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for PhyloTree_CollapseExpand command are missing.")


    elif args.command == 'PhyloSupport_Scaler':
        # Execute the PhyloSupport_Scaler function
        if args.input_GF_list and args.scale_to :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            scale = args.scale_to
            tre_dic = read_and_return_dict(input_GF_list)
            support_scaler_main(tre_dic,scale)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for PhyloSupport_Scaler command are missing.")


    elif args.command == 'BranchLength_NumericConverter':
        # Execute the BranchLength_NumericConverter function
        if args.input_GF_list:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            decimal_place=args.decimal_place
            tre_dic = read_and_return_dict(input_GF_list)
            branch_length_numeric_converter_main(tre_dic,decimal_place)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for BranchLength_NumericConverter command are missing.")


    elif args.command == 'Phylo_Rooter':
        # Execute the Phylo_Rooter function
        if args.input_GF_list and args.input_imap and args.input_sps_tree and args.input_gene_length:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_imap = args.input_imap
            input_sps_tree = args.input_sps_tree
            input_gene_length = args.input_gene_length
            gene2new_named_gene_dic, new_named_gene2gene_dic, voucher2taxa_dic,taxa2voucher_dic = gene_id_transfer(input_imap)
            len_dic = read_and_return_dict(input_gene_length)
            renamed_len_dic = rename_len_dic(len_dic, gene2new_named_gene_dic)
            sptree = PhyloTree(input_sps_tree)
            renamed_sptree=rename_input_tre(sptree,taxa2voucher_dic)
            tre_dic = read_and_return_dict(input_GF_list)
            root_main(tre_dic, gene2new_named_gene_dic, renamed_len_dic, new_named_gene2gene_dic, renamed_sptree,voucher2taxa_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for Phylo_Rooter command are missing.")
        
    elif args.command == 'OrthoFilter_LB':
        # Execute the OrthoFilter_LB function
        if args.input_GF_list and args.input_taxa and args.long_branch_index :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_taxa=args.input_taxa
            long_brancch_index=args.long_branch_index
            tre_dic = read_and_return_dict(input_GF_list)
            taxa_dic=read_and_return_dict(input_taxa)
            prune_main_LB(tre_dic,taxa_dic,long_brancch_index,visual=args.visual)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for OrthoFilter_LB command are missing.")


    elif args.command == 'OrthoFilter_Mono':
        # Execute the OrthoFilter_Mono function
        if args.input_GF_list and args.input_taxa and args.long_branch_index and args.insert_branch_index:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_taxa=args.input_taxa
            long_brancch_index=args.long_branch_index
            insert_branch_index=args.insert_branch_index
            tre_dic = read_and_return_dict(input_GF_list)
            taxa_dic=read_and_return_dict(input_taxa)
            prune_main_Mono(tre_dic,taxa_dic,long_brancch_index,insert_branch_index,visual=args.visual)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for OrthoFilter_Mono command are missing.")


    elif args.command == 'TreeTopology_Summarizer':
        # Execute the TreeTopology_Summarizer function
        if args.input_GF_list and args.input_imap :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_imap = args.input_imap
            outfile=args.outfile
            gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic= gene_id_transfer(input_imap)
            tre_dic = read_and_return_dict(input_GF_list)
            statistical_main(tre_dic,outfile,gene2new_named_gene_dic,voucher2taxa_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for TreeTopology_Summarizer command are missing.")


    # Perform the corresponding functions according to the parameters
    elif args.command == 'Tree_Visualizer':
        # Execute the Tree_Visualizer function
        if args.input_GF_list and args.input_imap :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_imap = args.input_imap
            tree_style = args.tree_style
            species_categories = args.species_categories
            keep_branch = args.keep_branch
            species_category_list = [read_and_return_dict(i) for i in species_categories]
            gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic= gene_id_transfer(input_imap)
            tre_dic = read_and_return_dict(input_GF_list)
            if args.gene_family and args.input_sps_tree:
                input_gene2fam = args.gene_family
                gene2fam = read_and_return_dict(input_gene2fam)
                input_sps_tree = args.input_sps_tree
                sptree = Tree(input_sps_tree)
                mark_gene_to_sptree_main(tre_dic,species_category_list,sptree,gene2fam)
                view_main(tre_dic, gene2new_named_gene_dic, voucher2taxa_dic, species_category_list, tree_style, keep_branch,new_named_gene2gene_dic,gene2fam)
            if args.gene_expression:
                gene2fam=None
                df=pd.read_excel(args.gene_expression, index_col=0) 
                view_main(tre_dic, gene2new_named_gene_dic, voucher2taxa_dic, species_category_list, tree_style, keep_branch,new_named_gene2gene_dic,gene2fam,df)
            else:
                gene2fam=None
                view_main(tre_dic, gene2new_named_gene_dic, voucher2taxa_dic, species_category_list, tree_style, keep_branch,new_named_gene2gene_dic,gene2fam)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for Tree_Visualizer command are missing.")

    
    elif args.command == 'GD_Detector':
        # Execute the GD_Detector function
        if args.input_GF_list and args.input_imap and args.input_sps_tree and args.gd_support and args.clade_support is not None and args.dup_species_radio is not None and args.dup_species_num :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_imap = args.input_imap
            input_sps_tree = args.input_sps_tree
            gd_support=args.gd_support
            clade_support=args.clade_support
            dup_species_percent = args.dup_species_radio
            dup_species_num = args.dup_species_num
            gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic= gene_id_transfer(input_imap)
            sptree=PhyloTree(args.input_sps_tree)
            num_tre_node(sptree)
            sptree.write(outfile='numed_sptree.nwk',format=1)
            renamed_sptree=rename_input_tre(sptree, taxa2voucher_dic)
            tre_dic = read_and_return_dict(input_GF_list)
            filename = 'gd_detector_result.txt'
            write_gd_result(filename, tre_dic, gd_support,clade_support,dup_species_percent, dup_species_num,renamed_sptree,gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for GD_Detector command are missing.")


    elif args.command == 'GD_Visualizer':
        # Execute the GD_Visualizer function
        if args.input_sps_tree and args.gd_result :
            start_time = time.time()
            sptree=Tree(args.input_sps_tree,format=1)
            gd_result = args.gd_result
            gd_visualizer_main(sptree,gd_result)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for GD_Visualizer command are missing.")


    elif args.command == 'GD_Loss_Tracker':
        # Execute the GD_Loss_Tracker function
        if args.input_GF_list and args.input_sps_tree and args.output_folder :
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_sps_tree = args.input_sps_tree
            out_dir=args.output_folder
            sptree=PhyloTree(input_sps_tree,format=1)
            num_sptree(sptree)
            tre_dic=read_and_return_dict(input_GF_list)

            os.makedirs(out_dir, exist_ok=True)
            sp_dic=get_path_str_num_dic(tre_dic,sptree)
            split_dicts=split_dict_by_first_last_char(sp_dic)
            divide_path_results_into_individual_files_by_species(split_dicts,out_dir)
            write_total_lost_path_counts_result(sp_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for GD_Loss_Tracker command are missing.")

    elif args.command == 'GD_Loss_Visualizer':
        # Execute the GD_Loss_Visualizer function
        if args.input_folder and  args.output_folder :
            start_time = time.time()
            input_dir=args.input_folder
            out_dir=args.output_folder
            os.makedirs(out_dir, exist_ok=True)
            generate_plt(input_dir,out_dir)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for GD_Loss_Visualizer command are missing.")

    elif args.command == 'Ortho_Retriever':
        # Execute the Ortho_Retriever function
        if args.input_GF_list and args.input_imap  and args.input_gene_length:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_imap = args.input_imap
            input_gene_length = args.input_gene_length
            gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic= gene_id_transfer(input_imap)
            tre_dic = read_and_return_dict(input_GF_list)
            len_dic = read_and_return_dict(input_gene_length)
            renamed_len_dic = rename_len_dic(len_dic, gene2new_named_gene_dic)
            split_main(tre_dic, gene2new_named_gene_dic, new_named_gene2gene_dic,renamed_len_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for Ortho_Retriever command are missing.")


    elif args.command == 'Hybrid_Tracer':
        # Execute the Hybrid_Tracer function
        if args.input_GF_list and args.input_Seq_GF_list  and args.input_sps_tree and args.input_imap:
            start_time = time.time()
            input_GF_list = args.input_GF_list
            input_Seq_GF_list = args.input_Seq_GF_list
            input_sps_tree = args.input_sps_tree
            input_imap= args.input_imap
            tre_dic = read_and_return_dict(input_GF_list)
            seq_path_dic = read_and_return_dict(input_Seq_GF_list)
            gene2new_named_gene_dic,new_named_gene2gene_dic,voucher2taxa_dic,taxa2voucher_dic= gene_id_transfer(input_imap)
            sptree=read_phylo_tree(input_sps_tree)
            rename_sptree=rename_input_tre(sptree,taxa2voucher_dic)
            num_tre_node(rename_sptree)
            hyde_main(tre_dic,seq_path_dic,rename_sptree,gene2new_named_gene_dic,voucher2taxa_dic,taxa2voucher_dic,new_named_gene2gene_dic)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for Hybrid_Tracer command are missing.")

    elif args.command == 'Hybrid_Visualizer':
        # Execute the Hybrid_Visualizer function
        if args.input_hybrid_folder  and args.input_sps_tree :
            start_time = time.time()
            input_hybrid_folder=args.input_hybrid_folder
            input_sps_tree = args.input_sps_tree
            sptree=read_tree(input_sps_tree)
            hyde_visual_main(input_hybrid_folder,sptree)
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for Hybrid_Visualizer command are missing.")

    elif args.command == 'HaploFinder':
        required_args = [args.input_GF_list, args.input_imap, args.species_a, args.species_b,
                     args.species_a_gff, args.species_b_gff, args.species_a_lens, args.species_b_lens,
                     args.blastp_result, args.synteny_result, args.blastp_limit]
    
        if all(required_args):
            start_time = time.time()
            
            # Process results
            process_blastp_pairs = process_blastp_result(args.blastp_result, args.blastp_limit)
            process_synteny_pairs = process_synteny_result(args.synteny_result)
            process_gd_pairs = process_gd_result(args.input_GF_list, args.input_imap, args.species_a, args.species_b)
            
            # GFF and lens variables
            gff1, gff2 = args.species_a_gff, args.species_b_gff
            lens1, lens2 = args.species_a_lens, args.species_b_lens
            spe1, spe2 = args.species_a, args.species_b
            
            # Helper function to generate dotplots
            def generate_and_print_dotplot(pairs, label):
                generate_dotplot(gff1, gff2, lens1, lens2, pairs, spe1, spe2, label)
                print('-' * 30)
            
            # Generate dotplots
            generate_and_print_dotplot(process_blastp_pairs, 'blastp_pairs')
            generate_and_print_dotplot(process_synteny_pairs, 'synteny_pairs')
            generate_and_print_dotplot(process_gd_pairs, 'gd_pairs')
            
            total_pairs = process_blastp_pairs + process_synteny_pairs + process_gd_pairs
            generate_and_print_dotplot(total_pairs, 'total_pairs')
            
            # Calculate and print execution time
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_time(execution_time)
            print("Program execution time:", formatted_time)
        else:
            print("Required arguments for HaploFinder command are missing.")
     
    else:
        print("Usage: python PhyloTracer.py  [-h]  {BranchLength_NumericConverter, GD_Detector, GD_Loss_Tracker, GD_Loss_Visualizer, GD_Visualizer, HaploFinder, Hybrid_Tracer, Hybrid_Visualizer, OrthoFilter_LB, OrthoFilter_Mono, Ortho_Retriever, PhyloSupport_Scaler, PhyloTree_CollapseExpand, Phylo_Rooter, TreeTopology_Summarizer, Tree_Visualizer}")
        print()
        print("optional arguments:")
        print('  -h, --help            show this help message and exit')
        print()
        print('available programs::')
        print('  {BranchLength_NumericConverter, GD_Detector, GD_Loss_Tracker, GD_Loss_Visualizer, GD_Visualizer, HaploFinder, Hybrid_Tracer, Hybrid_Visualizer, OrthoFilter_LB, OrthoFilter_Mono, Ortho_Retriever, PhyloSupport_Scaler, PhyloTree_CollapseExpand, Phylo_Rooter, TreeTopology_Summarizer, Tree_Visualizer}')


if __name__ == "__main__":
    main()

