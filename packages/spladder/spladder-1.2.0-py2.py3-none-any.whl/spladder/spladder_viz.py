#! /usr/bin/env python
import sys
import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import cPickle
import pdb

from . import settings
from .viz.graph import *
from .viz.coverage import *
from .viz.genelets import *
from .viz import axes as vax
from .identity import *

def parse_options(argv):

    """Parses options from the command line """

    from optparse import OptionParser, OptionGroup

    parser = OptionParser()
    required = OptionGroup(parser, 'MANDATORY')
    required.add_option('-o', '--outdir', dest='outdir', metavar='DIR', help='spladder directory containing the spladder results', default='-')
    optional = OptionGroup(parser, 'OPTIONAL')
    optional.add_option('-b', '--bams', dest='bams', metavar='FILE1A,FILE2A:FILE1B,FILE2B,,...', help='alignment files in BAM format (comma separated list,colon separated groups)', default='-')
    optional.add_option('-L', '--labels', dest='labels', metavar='LABEL_A,LABEL_B,...', help='group labels for alignment files groups (comma separated list)', default='')
    optional.add_option('-g', '--gene_name', dest='gene_name', metavar='STR', help='gene_name to be plotted', default=None)
    optional.add_option('-e', '--event_id', dest='event_id', metavar='STR', help='event to be plotted', default=None)
    optional.add_option('--test-result', dest='test_result', metavar='INT', type='int', help='plot top k significant events from test', default=0)
    optional.add_option('--test-labels', dest='test_labels', metavar='STR', type='str', help='labels used for the groups in the test (order matters) [condA:condB]', default='condA:condB')
    optional.add_option('-t', '--event_types', dest='event_types', metavar='EVENT1,EVENT2,...', help='list of alternative splicing events to extract [exon_skip,intron_retention,alt_3prime,alt_5prime,mult_exon_skip,mutex_exons]', default='exon_skip,intron_retention,alt_3prime,alt_5prime,mult_exon_skip,mutex_exons')
    optional.add_option('', '--testdir', dest='testdir', metavar='DIR', help='directory to testing output, if different from spladder outdir', default='-')

    output = OptionGroup(parser, 'OUTPUT')
    output.add_option('-m', '--mincount', dest='mincount', metavar='INT', type='int', help='minimum count of introns to be displayed in coverage plot [0]', default=0)
    output.add_option('-f', '--format', dest='format', metavar='STR', help='plot file format [pdf, png, d3]', default='pdf')
    output.add_option('', '--zoom_x', dest='zoom_x', metavar='percent_left,percent_right', help='zoom x axis from percent_left to percent_right [0.0,1.0]', default='0.0,1.0')
    output.add_option('-l', '--log', dest='log', action='store_true', help='plot coverage information in log scale [off]', default=False)

    user = OptionGroup(parser, 'USER')
    user.add_option('-u', '--user', dest='user', metavar='y|n', help='apply user mode (experimental) [off]', default='n')
    user.add_option('-T', '--transcripts', dest='transcripts', metavar='y|n', help='plot annotated transcripts', default='n')
    user.add_option('-s', '--splicegraph', dest='splicegraph', metavar='y|n', help='plot splicegraph structure', default='n')

    general = OptionGroup(parser, 'GENERAL')
    general.add_option('-c', '--confidence', dest='confidence', metavar='INT', type='int', help='confidence level (0 lowest to 3 highest) [3]', default=3)
    general.add_option('-V', '--validate_sg', dest='validate_sg', metavar='y|n', help='validate splice graph [n]', default='n')
    general.add_option('-v', '--verbose', dest='verbose', metavar='y|n', help='verbosity', default='n')
    general.add_option('-d', '--debug', dest='debug', metavar='y|n', help='use debug mode [n]', default='n')
    parser.add_option_group(required)
    parser.add_option_group(optional)
    parser.add_option_group(output)
    parser.add_option_group(user)
    parser.add_option_group(general)

    (options, args) = parser.parse_args()
    #options.event_types = options.event_types.strip(',').split(',')

    if len(argv) < 2:
        parser.print_help()
        sys.exit(2)

    options.parser = parser
    return options


def get_plot_len(CFG):
    """Identifies the number of rows we need in our plot"""

    rows = 3 # splicing graph + events + segments
    if len(CFG['bam_fnames']) > 0:
        rows += len(CFG['bam_fnames'])
        if len(CFG['bam_fnames']) > 1:
            rows += 1
    rows += int(CFG['plot_transcripts'])

    return rows



def _add_ax(fig, axes, gs):
    sharex = None if len(axes) == 0 else axes[0]
    axes.append(fig.add_subplot(gs[len(axes), 0], sharex=sharex))

def spladder_viz():

    """Main visualization code"""

    ### parse command line parameters
    options = parse_options(sys.argv)

    ### parse parameters from options object
    CFG = settings.parse_args(options, identity='viz')

    ### create plot directory if it does not exist yet
    if options.testdir != '-':
        dirname = options.testdir
    else:
        dirname = CFG['out_dirname']
    if not os.path.exists(os.path.join(dirname, 'plots')):
        os.mkdir(os.path.join(dirname, 'plots'))

    if options.format == 'd3':
        try:
            import mpld3
            from mpld3 import plugins
        except ImportError:
            sys.stderr.write("ERROR: missing package for output format d3. Package mpld3 required")
            sys.exit(1)

    ### load gene information
    gene_names = get_gene_names(CFG)

    rows = get_plot_len(CFG)
    gs = gridspec.GridSpec(rows, 1)

    ### set color maps
    cmap_cov = plt.get_cmap('jet')
    cmap_edg = plt.get_cmap('jet')

    ### plot log scale?
    log_tag = ''
    if options.log:
        log_tag = '.log'
    event_tag = ''

    ### did we get any labels?
    if CFG['plot_labels']:
        CFG['plot_labels'] = CFG['plot_labels'].strip(',').split(',')
        assert len(CFG['plot_labels']) == len(CFG['bam_fnames']), "The number of given labels (%i) needs to match the number of given bam file groups (%i)" % (len(CFG['plot_labels']), len(CFG['bam_fnames']))

    ### the user chose a specific gene for plotting
    ### create pairs of gene ids and an event_id (the latter is None by default)
    if options.gene_name is not None:
        #gid = sp.where(sp.array([x.split('.')[0] for x in gene_names]) == options.gene_name.split('.')[0])[0]
        gids = [[sp.where(sp.array(gene_names) == options.gene_name)[0][0], options.event_id]]
        if len(gids) == 0:
            sys.stderr.write('ERROR: provided gene ID %s could not be found, please check for correctness\n' % options.gene_name)
            sys.exit(1)
    ### the plotting happens on the results of spladder test
    ### the user chooses to plot the top k significant events
    ### this requires the event type to be specified
    elif options.test_result > 0:
        gene_names = []
        for event_type in CFG['event_types']:
            ### the testing script should generate a setup file for the test
            ### SETUP is structured as follows:
            ###  [gene_strains, event_strains, dmatrix0, dmatrix1, event_type, options, CFG]
            labels = options.test_labels.split(':')
            options.labels = labels
            if options.testdir != '-':
                testdir = dirname
            else:
                testdir = os.path.join(dirname, 'testing_%s_vs_%s' % (labels[0], labels[1]))
            SETUP = cPickle.load(open(os.path.join(testdir, 'test_setup_C%i_%s.pickle' % (CFG['confidence_level'], event_type)), 'r'))

            ### get strains to plot
            idx1 = sp.where(sp.in1d(SETUP[0], SETUP[6]['conditionA']))[0]
            idx2 = sp.where(sp.in1d(SETUP[0], SETUP[6]['conditionB']))[0]

            ### load test results
            for l, line in enumerate(open(os.path.join(testdir, 'test_results_C%i_%s.tsv' % (CFG['confidence_level'], event_type)), 'r')):
                if l == 0:
                    continue
                if l > options.test_result:
                    break
                sl = line.strip().split('\t')
                gene_names.append([sl[1], sl[0]])
        gids = get_gene_ids(CFG, gene_names)
    ### no gene specified but result provided - plot all genes with confirmed events
    ### if an event_id is provided, only the associated gene will be plotted
    else:
        gids = get_gene_ids(CFG)

    ### iterate over genes to plot
    for gid in gids:

        ### gather information about the gene we plot
        gene = load_genes(CFG, idx=[gid[0]])[0]
        if CFG['verbose']:
            print 'plotting information for gene %s' % gene.name
        gene.from_sparse()

        ### event to plot is specified with the gene id list
        if gid[1] is not None:
            event_info = [x[::-1] for x in re.split(r'[._]', gid[1][::-1], maxsplit=1)[::-1]]
            event_info[1] = int(event_info[1]) - 1
            event_info = sp.array(event_info, dtype='str')[sp.newaxis, :]
            event_tag = '.%s' % gid[1]
        ### get all significant events of the current gene
        else:
            event_info = get_conf_events(CFG, gid[0])

        ### go over different plotting options
        axes = []
        ### plot result of testing
        if options.test_result > 0:
            fig = plt.figure(figsize = (9, 5), dpi=200)
            gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
            _add_ax(fig, axes, gs)
            _add_ax(fig, axes, gs)
            _plot_event(CFG, event_info, fig, axes[1], gs, None, padding=100)
            start, stop = axes[1].get_xlim()
            plot_bam(options, gene, CFG['bam_fnames'], fig, axes[0], gs, None, cmap_cov, cmap_edg, single=False, sharex=axes[1], start=int(start), stop=int(stop))

        ### plot custom layout
        elif options.user == 'y':

            if options.format == 'd3':
                fig = plt.figure(figsize = (12, 2*rows), dpi=100)
            else:
                fig = plt.figure(figsize = (18, 3*rows), dpi=200)

            xlim = None
            ### plot splicing graph
            if options.splicegraph == 'y':
                _plot_splicegraph(gene, fig, axes, gs)
                xlim = axes[1].get_xlim()

            ### plot annotated transcripts
            if CFG['plot_transcripts']:
                sharex = None if len(axes) == 0 else axes[0]
                axes.append(fig.add_subplot(gs[len(axes), 0], sharex=sharex))
                multiple(gene.exons, ax=axes[-1], x_range=xlim)
                axes[-1].set_title('Annotated Transcripts')

            ### plot coverage information for a set of given samples
            if len(CFG['bam_fnames']) > 0:
                plot_bam(options, gene, CFG['bam_fnames'], fig, axes, gs, xlim, cmap_cov, cmap_edg)

                ### plot all the samples in a single plot
                if len(CFG['bam_fnames']) > 1:
                    plot_bam(options, gene, CFG['bam_fnames'], fig, axes, gs, xlim, cmap_cov, cmap_edg, single=False)

            ### plot segment counts
            if len(CFG['bam_fnames']) == 0 or False: # add option for segment plots
                if options.test_result > 0:
                    _plot_segments(CFG, gid, fig, axes, gs, options, [idx1, idx2])
                else:
                    _plot_segments(CFG, gid, fig, axes, gs, options)

            ### plot structure of a single given event
            _plot_event(CFG, event_info, fig, axes, gs, xlim)

        ### we only need to adapt the xoom for one axis object - as we share the x
        zoom_x = [float(x) for x in options.zoom_x.split(',')]
        xlim = axes[0].get_xlim()
        xdiff = xlim[1] - xlim[0]
        axes[0].set_xlim([xlim[0] + (zoom_x[0] * xdiff), xlim[0] + (zoom_x[1] * xdiff)])

        for ax in axes:
            vax.clean_axis(ax)

        plt.tight_layout()
        ### save plot into file
        if options.format == 'd3':
            out_fname = os.path.join(dirname, 'plots', 'gene_overview_C%i_%s%s%s.html' % (options.confidence, gene.name, event_tag, log_tag))
            plugins.clear(fig)
            plugins.connect(fig, plugins.Zoom(enabled=True))
            mpld3.save_html(fig, open(out_fname, 'w'))
        else:
            if options.test_result > 0:
                out_fname = os.path.join(dirname, 'plots', 'gene_overview_C%i_%s%s%s.%s' % (options.confidence, gene.name, event_tag, log_tag, options.format))
            else:
                out_fname = os.path.join(dirname, 'plots', 'gene_overview_C%i_%s%s%s.%s' % (options.confidence, gene.name, event_tag, log_tag, options.format))
            plt.savefig(out_fname, format=options.format, bbox_inches='tight')
        plt.close(fig)


def plot_bam(options, gene, samples, fig, axes, gs, xlim, cmap_cov, cmap_edg, single=True, subsample_size=5, sharex=None, start=None, stop=None):

    min_sample_size = min(subsample_size, min([len(x) for x in samples]))
    if start is None:
        start = gene.splicegraph.vertices.min()
    if stop is None:
        stop = gene.splicegraph.vertices.max()

    norm = plt.Normalize(0, len(samples))
    caxes = []
    labels = []

    if sharex is None:
        sharex = None if len(axes) == 0 else axes[0]
    for s, bams in enumerate(samples):

        if options.labels != '':
            label = options.labels[s]
        else:
            label = 'group %i' % (s + 1)

        if single:
            axes.append(fig.add_subplot(gs[len(axes), 0], sharex=sharex))
            title = 'Expression (%s)' % label
            color_cov = cmap_cov(norm(0)) # '#d7191c'
            color_edg = cmap_edg(norm(0)) # '#1a9641'
            ax = axes[-1]
        else:
            if s == 0:
                if hasattr(axes, '__iter__'):
                    axes.append(fig.add_subplot(gs[len(axes), 0], sharex=sharex))
                    ax = axes[-1]
                else:
                    ax = axes
            title = 'Expression all Sample Groups'
            color_cov = cmap_cov(norm(s))
            color_edg = cmap_edg(norm(s))

        caxes.append(cov_from_bam(gene.chr, start, stop, bams, subsample=min_sample_size, ax=ax, intron_cnt=True,
                     log=options.log, title=title, xlim=xlim, color_cov=color_cov, color_intron_edge=color_edg,
                     grid=True, min_intron_cnt=options.mincount, return_legend_handle=True, label=label))
        labels.append(label)
        ax.set_xlabel('')

    if not single:
        ax.legend(caxes, labels)


def _plot_event(CFG, event_info, fig, axes, gs, xlim, padding=None):
    """This function takes the event_id given in the CFG object and 
    plots it into ax."""

    axes.append(fig.add_subplot(gs[len(axes), 0]))
    event_list = [_ for event in load_events(CFG, event_info) for _ in [event.exons1, event.exons2]]
    multiple(event_list, ax=axes[-1], x_range=xlim, color='green', padding=padding) 
    #ax.set_title('Alt event structure') # of %s' % options.event_id)
    vax.clean_axis(axes[-1], allx=True)


def _plot_splicegraph(gene, fig, axes, gs):
    """Append a new object to the axes list, and into the gridspec
       at the current position and plot a splicing graph"""

    axes.append(fig.add_subplot(gs[len(axes), 0]))
    plot_graph(gene.splicegraph.vertices, gene.splicegraph.edges, axes[-1])
    axes[-1].set_title('Splicing graph for %s' % gene.name)


def _plot_segments(CFG, gid, fig, axes, gs, options, seg_sample_idx=None):

    print 'get segment counts'
    (segments, edges, edge_idx, strains) = get_seg_counts(CFG, gid[0])
    seg_sample_idx = None
    if len(CFG['strains']) > 0:
        seg_sample_idx = []
        for group in CFG['strains']:
            seg_sample_idx.append(sp.where(sp.in1d(strains, group))[0])
    axes.append(fig.add_subplot(gs[len(axes), 0], sharex=axes[0]))
    print 'plot segment counts'
    if identity() == 'matlab':
        cov_from_segments(gene, segments, edges, edge_idx, axes[-1], xlim=xlim, log=options.log, grid=True, order='F')
    else:
        cov_from_segments(gene, segments, edges, edge_idx, axes[-1], xlim=xlim, log=options.log, grid=True, order='C', sample_idx=seg_sample_idx)
    axes[-1].set_title('Segment counts')



if __name__ == "__main__":
    spladder_viz()

