import scipy as sp
import pdb
import sys
import copy

if __package__ is None:
    __package__ = 'modules.core'

from ..reads import *
from ..helpers import *
from ..editgraph import *
from ..merge import *

def gen_graphs(genes, CFG=None):
    # [genes, inserted] = gen_graphs(genes, CFG)

    if CFG is None and isinstance(genes, dict):
        PAR = genes
        genes  = PAR['genes']
        CFG = PAR['CFG']

    if CFG['fd_log'].closed:
         CFG['fd_log'] = sys.stdout

    ### init the stats for inserted elements
    inserted = dict()
    inserted['cassette_exon'] = 0
    inserted['intron_retention'] = 0
    inserted['intron_in_exon'] = 0
    inserted['alt_53_prime'] = 0
    inserted['exon_skip'] = 0
    inserted['gene_merge'] = 0
    inserted['new_terminal_exon'] = 0

    # build splice graph for all genes 
    ##############################################################################%%
    print >> CFG['fd_log'], 'Generating splice graph ...'
    ### merge exons if possible / reduce graph
    ### originially implemented for ESTs, reduces complexity, 
    ### but removes alternative transcript starts and ends !
    if CFG['do_infer_splice_graph']:
        genes = infer_splice_graph(genes)

    ### sort exons by start position in ascending order
    for ix in range(genes.shape[0]):
        genes[ix].splicegraph.sort()

    ### label alternative and constitutive genes
    for ix in range(genes.shape[0]):
        genes[ix].label_alt()
    if CFG['verbose']:
        print >> CFG['fd_log'],'\nTotal genes:\t\t\t\t\t\t\t%d' % genes.shape[0]
        print >> CFG['fd_log'],'Total genes with alternative isoforms:\t\t\t\t%d' % sp.sum([x.is_alt for x in genes])
        print >> CFG['fd_log'],'Total genes alternatively spliced:\t\t\t\t%d' % sp.sum([x.is_alt_spliced for x in genes])
        print >> CFG['fd_log'],'Total constitutively spliced:\t\t\t\t\t%d' % (genes.shape[0] - sp.sum([x.is_alt_spliced for x in genes]))

    ### update terminals, start terminals in row 1, end terminals in row 2
    for i in range(genes.shape[0]):
        genes[i].splicegraph.update_terminals()

    ### reset gene start and gene stop according to exons and splice graph
    for i in range(genes.shape[0]):
        genes[i].start = min([x.min() for x in genes[i].exons])
        genes[i].stop = max([x.max() for x in genes[i].exons])
    print >> CFG['fd_log'], '...done.\n'

    ### sort genes by positions
    s_idx = sp.argsort([x.stop for x in genes])
    genes = genes[s_idx]
    s_idx = sp.argsort([x.start for x in genes], kind='mergesort')
    genes = genes[s_idx]
    s_idx = sp.argsort([x.chr for x in genes], kind='mergesort')
    genes = genes[s_idx]

    # append list of introns supported by RNA-seq data to 
    # the genes structure (only in case we want to augment the graph)
    ##############################################################################%%
    if (CFG['do_insert_cassette_exons'] or CFG['do_insert_intron_retentions'] or CFG['do_insert_intron_edges']): 
        print >> CFG['fd_log'], 'Loading introns from file ...'
        introns = get_intron_list(genes, CFG)
        print >> CFG['fd_log'], '...done.\n'

        ### clean intron list
        ### remove all introns that overlap more than one gene on the same strand
        print >> CFG['fd_log'], 'Filtering introns for ambiguity ...'
        introns = filter_introns(introns, genes, CFG)
        print >> CFG['fd_log'], '...done.\n'

        ### check feasibility
        ### TODO when working exclusively with sparse bam, we need to skip this ...
        print >> CFG['fd_log'], 'Testing for infeasible genes ...'
        introns = make_introns_feasible(introns, genes, CFG)
        print >> CFG['fd_log'], '...done.\n'

        for i in range(genes.shape[0]):
            genes[i].introns = introns[i, :]

    if CFG['do_insert_cassette_exons']:
        print >> CFG['fd_log'], 'Inserting cassette exons ...'
        CFG_ = dict()
        if 'cassette_exon' in CFG and 'read_filter' in CFG['cassette_exon']:
            CFG_['read_filter'] = CFG['read_filter'].copy()
            CFG['read_filter'] = CFG['cassette_exon']['read_filter']
        genes, inserted_ = insert_cassette_exons(genes, CFG)
        inserted['cassette_exon'] = inserted_
        for key in CFG_:
            CFG[key] = CFG_[key].copy()
        print >> CFG['fd_log'], '\n... inserted %i casette exons ....\n... done.\n' % inserted['cassette_exon']

    if CFG['do_insert_intron_retentions']:
        print >> CFG['fd_log'], 'Inserting intron retentions ...'
        CFG_ = dict()
        if 'read_filter' in CFG['intron_retention']:
            CFG_['read_filter'] = CFG['read_filter'].copy()
            CFG['read_filter'] = CFG['intron_retention']['read_filter']
        genes, inserted_ = insert_intron_retentions(genes, CFG)
        inserted['intron_retention'] = inserted_
        for key in CFG_:
            CFG[key] = CFG_[key].copy()
        print >> CFG['fd_log'], '\n... inserted %i new intron retentions ...\n...done.\n' % inserted['intron_retention']

    if CFG['do_remove_short_exons']:
        print >> CFG['fd_log'], 'Removing short exons ...'
        genes = remove_short_exons(genes, CFG)
        for i in range(genes.shape[0]):
            if sp.any(genes[i].splicegraph.vertices[:, 1] - genes[i].splicegraph.vertices[:, 0] < CFG['remove_exons']['min_exon_len_remove']):
                print >> sys.stderr, 'WARNING: could not remove all short exons'
        print >> CFG['fd_log'], '... done.\n'


    # test all exons if the reading frame is larger if exon is skipped
    ##############################################################################%%
    #print >> CFG['fd_log'], 'find exons to skip to elongate reading frame'
    #genes = insert_cds_exon_skips(genes, genome_info)
    #genes = splice_graph(genes)


    # sanity checking
    for g in genes:
        assert(all(g.splicegraph.vertices[0, :] <= g.splicegraph.vertices[1, :]))

    if CFG['do_insert_intron_edges']:
        # re-set list of introns supported by RNA-seq data to 
        # the genes structure
        ##############################################################################%%
        for i in range(genes.shape[0]):
            genes[i].introns = introns[i, :]

        print >> CFG['fd_log'], 'Inserting new intron edges ...'
        chrms = sp.array([x.chr for x in genes], dtype='str')
        for chr_idx in sp.unique(chrms):
            genes_before = genes[sp.where(chrms == chr_idx)[0]]
            tmp_genes = copy.deepcopy(genes_before)
            #
            ##############################################################################%%
            if not 'insert_intron_iterations' in CFG:
                CFG['insert_intron_iterations'] = 5
            for iter in range(1, CFG['insert_intron_iterations'] + 1):
                print >> CFG['fd_log'], '... chr %s - iteration %i/%i\n' % (chr_idx, iter, CFG['insert_intron_iterations'])

                genes_mod, inserted_ = insert_intron_edges(tmp_genes, CFG)

                inserted['intron_in_exon'] += inserted_['intron_in_exon']
                inserted['alt_53_prime'] += inserted_['alt_53_prime']
                inserted['exon_skip'] += inserted_['exon_skip']
                inserted['gene_merge'] += inserted_['gene_merge']
                inserted['new_terminal_exon'] += inserted_['new_terminal_exon']

                # in case any exon was inserted that already existed, we merge them into one exon 
                print >> CFG['fd_log'], '... removing duplicate exons ...'
                genes_mod = merge_duplicate_exons(genes_mod, CFG)

                # inserted
                if isequal(genes_mod, genes_before):
                    break
                tmp_genes = genes_mod
            chrms = sp.array([x.chr for x in genes], dtype='str')
            genes[sp.where(chrms == chr_idx)[0]] = copy.deepcopy(genes_mod)
        print >> CFG['fd_log'], '... done.\n'

    print >> CFG['fd_log'], 'Re-labeleling new alternative genes ...'
    for ix in range(genes.shape[0]):
        genes[ix].start = genes[ix].splicegraph.vertices.min()
        genes[ix].stop = genes[ix].splicegraph.vertices.max()
        genes[ix].label_alt()
    print >> CFG['fd_log'], '... done.\n'

    ### print summary to log file
    print >> CFG['fd_log'], 'Inserted:'
    for fn in inserted:
        print >> CFG['fd_log'], '\t%s:\t%i' % (fn, inserted[fn])

    if CFG['fd_log'] != sys.stdout:
        CFG['fd_log'].close()

    return (genes, inserted)

