#!/usr/bin/env python2.7
"""
Generate a VCF from a GAM and XG by splitting into GAM/VG chunks.
"""
from __future__ import print_function
import argparse, sys, os, os.path, random, subprocess, shutil, itertools, glob
import json, timeit, errno, copy, time
from uuid import uuid4
import logging
from collections import defaultdict

from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore

logger = logging.getLogger(__name__)

def call_subparser(parser):
    """
    Create a subparser for calling.  Should pass in results of subparsers.add_parser()
    """

    # Add the Toil options so the job store is the first argument
    Job.Runner.addToilOptions(parser)

    # General options
    parser.add_argument("xg_path", type=make_url,
                        help="input xg file")
    parser.add_argument("sample_name", type=str,
                        help="sample name (ex NA12878)")
    parser.add_argument("out_store",
                        help="output store.  All output written here. Path specified "
                        "using same syntax as toil jobStore")
    parser.add_argument("--chroms", nargs='+', required=True,
                        help="Name(s) of reference path in graph(s) (separated by space)."
                        " Must be same length/order as --gams")
    # todo: move to chunked_call_parse_args and share with toil-vg run
    parser.add_argument("--gams", nargs='+', required=True, type=make_url,
                        help="GAMs to call.  One per chromosome in the same order as --chroms, or just one. "
                        " Indexes (.gai) will be used if found.")
    
    # Add common options shared with everybody
    add_common_vg_parse_args(parser)

    # Add common calling options shared with toil_vg pipeline
    chunked_call_parse_args(parser)

    # Add common docker options shared with toil_vg pipeline
    add_container_tool_parse_args(parser)
                        

def chunked_call_parse_args(parser):
    """ centralize calling parameters here """
    parser.add_argument("--overlap", type=int,
                        help="overlap option that is passed into make_chunks and call_chunk")
    parser.add_argument("--call_chunk_size", type=int,
                        help="chunk size")
    parser.add_argument("--call_opts", type=str,
                        help="arguments to pass to vg call (wrapped in \"\")")
    parser.add_argument("--genotype", action="store_true",
                        help="use vg genotype instead of vg call")
    parser.add_argument("--genotype_opts", type=str,
                        help="arguments to pass to vg genotype (wrapped in \"\")")
    parser.add_argument("--filter_opts", type=str,
                        help="argument to pass to vg filter (wrapped in \"\")")
    parser.add_argument("--calling_cores", type=int,
                        help="number of threads during the variant calling step")
    parser.add_argument("--calling_mem", type=str,
                        help="memory alotment during the variant calling step")
    parser.add_argument("--call_chunk_cores", type=int,
                        help="number of threads used for extracting chunks for calling")
    parser.add_argument("--call_chunk_mem", type=str,
                        help="memory alotment for extracting chunks for calling")
    parser.add_argument("--vcf_offsets", nargs='+', default=[],
                        help="offset(s) to apply to output vcfs(s). (order of --chroms)")
    parser.add_argument("--recall", action="store_true",
                        help="only call variants present in the graph")

def validate_call_options(options):    
    require(len(options.chroms) == len(options.gams) or len(options.gams) == 1,
            'Number of --chroms must be 1 or same as number of --gams')
    require(not options.vcf_offsets or len(options.vcf_offsets) == len(options.chroms),
            'Number of --vcf_offsets if specified must be same as number of --chroms')
    require(not options.genotype or not options.recall,
            '--recall not yet supported with --genotype')
    
def sort_vcf(job, drunner, vcf_path, sorted_vcf_path):
    """ from vcflib """
    vcf_dir, vcf_name = os.path.split(vcf_path)
    with open(sorted_vcf_path, "w") as outfile:
        drunner.call(job, [['bcftools', 'view', '-h', vcf_name]], outfile=outfile,
                     work_dir=vcf_dir)
        drunner.call(job, [['bcftools', 'view', '-H', vcf_name],
                      ['sort', '-k1,1d', '-k2,2n']], outfile=outfile,
                     work_dir=vcf_dir)

def run_vg_call(job, context, sample_name, vg_id, gam_id, xg_id = None,
                path_names = [], seq_names = [], seq_offsets = [], seq_lengths = [],
                chunk_name = 'call', genotype = False, recall = False):
    """ Run vg call or vg genotype on a single graph.

    Returns (vcf_id, pileup_id, xg_id, gam_id, augmented_graph_id). pileup_id and xg_id
    can be same as input if they are not computed.  If pileup/xg/augmented are 
    computed, the returned ids will be None unless appropriate keep_flag set
    (to prevent sending them to the file store if they aren't wanted)

    User is responsible to make sure that options passed in context.config.*_opts don't conflict
    with seq_names, seq_offsets, seq_lengths etc. If not provided, the pileup is computed.

    gam filtering is only done if filter_opts are passed in. 

    chunk_name option is only for working filenames (to make more readable)
    
    When running vg genotype, we can't recall (since recall in vg genotype needs a VCF). 

    """
    
    work_dir = job.fileStore.getLocalTempDir()

    filter_opts = context.config.filter_opts if not recall else context.config.recall_filter_opts
    augment_opts = context.config.augment_opts
    if genotype:
        call_opts = context.config.genotype_opts
    else:
        call_opts = context.config.call_opts if not recall else context.config.recall_opts

    # Read our input files from the store
    vg_path = os.path.join(work_dir, '{}.vg'.format(chunk_name))
    job.fileStore.readGlobalFile(vg_id, vg_path)
    gam_path = os.path.join(work_dir, '{}.gam'.format(chunk_name))
    job.fileStore.readGlobalFile(gam_id, gam_path)
    xg_path = os.path.join(work_dir, '{}.xg'.format(chunk_name))
    defray = filter_opts and ('-D' in filter_opts or '--defray-ends' in filter_opts)
    if xg_id and defray:
        job.fileStore.readGlobalFile(xg_id, xg_path)
        
    # Define paths for all the files we might make
    pu_path = os.path.join(work_dir, '{}.pu'.format(chunk_name))
    trans_path = os.path.join(work_dir, '{}.trans'.format(chunk_name))
    support_path = os.path.join(work_dir, '{}.support'.format(chunk_name))
    aug_path = os.path.join(work_dir, '{}_aug.vg'.format(chunk_name))
    aug_gam_path = os.path.join(work_dir, '{}_aug.gam'.format(chunk_name))
    vcf_path = os.path.join(work_dir, '{}_call.vcf'.format(chunk_name))

    timer = TimeTracker()

    # we only need an xg if using vg filter -D
    if not xg_id and defray:
        timer.start('chunk-xg')
        context.runner.call(job, ['vg', 'index', os.path.basename(vg_path), '-x',
                                   os.path.basename(xg_path), '-t', str(context.config.calling_cores)],
                             work_dir = work_dir)
        timer.stop()

    # optional gam filtering
    gam_filter_path = gam_path + '.filter'
    filter_command = None
    if filter_opts:
        filter_command = ['vg', 'filter', os.path.basename(gam_path), '-t', '1'] + filter_opts
        if defray:
            filter_command += ['-x', os.path.basename(xg_path)]
        if genotype:
            with open(gam_filter_path, 'w') as gam_filter_file:
                context.runner.call(job, filter_command, work_dir = work_dir, outfile = gam_filter_file)
            filter_command = None
    else:
        gam_filter_path = gam_path

    # augmentation
    augment_command = []
    augment_generated_opts = []
    if filter_command is not None:
        aug_gam_input = '-'
        augment_command.append(filter_command)
    else:
        aug_gam_input = os.path.basename(gam_filter_path)

    if genotype:
        augment_generated_opts = ['--augmentation-mode', 'direct',
                                  '--alignment-out', os.path.basename(aug_gam_path)]
        augment_opts = []
    else:
        augment_generated_opts = ['--augmentation-mode', 'pileup',
                                  '--translation', os.path.basename(trans_path),
                                  '--support', os.path.basename(support_path)]
        if recall:
            augment_opts = []
            augment_generated_opts += ['--recall']
                
    augment_command.append(['vg', 'augment', os.path.basename(vg_path), aug_gam_input,
                    '-t', str(context.config.calling_cores)] + augment_opts + augment_generated_opts)

    try:
        with open(aug_path, 'w') as aug_stream:
            timer.start('call-filter-augment')
            context.runner.call(job, augment_command, work_dir=work_dir, outfile=aug_stream)
            timer.stop()
    except Exception as e:
        logging.error("Augmentation failed. Dumping files.")
        for dump_path in [vg_path, gam_path, gam_filter_path]:
            if dump_path and os.path.isfile(dump_path):
                context.write_output_file(job, dump_path)        
        raise e

    # naming options shared between call and genotype
    name_opts = []
    for path_name in path_names:
        name_opts += ['-r', path_name]
    for seq_name in seq_names:
        name_opts += ['-c', seq_name]
    for seq_length in seq_lengths:
        name_opts += ['-l', seq_length]
    for seq_offset in seq_offsets:
        name_opts += ['-o', seq_offset]
                    
    if genotype:
        # We can't do recall (no passed VCF) 
        assert(not recall)
        
        # How do we actually genotype
        # (Genotype runs fine with its built-in augmentation, but I suspect it causes trouble
        # with some CI tests, perhaps by taking more memory, so we leave augmentation in its
        # own command)
        command = ['vg', 'genotype', os.path.basename(aug_path), '-t',
                   str(context.config.calling_cores), '-s', sample_name,
                   '-v', '-E', '-G', os.path.basename(aug_gam_path)]
                           
        if call_opts:
            command += call_opts
        command += name_opts
        
        try:
            with open(vcf_path, 'w') as vggenotype_stdout:
                timer.start('genotype')
                context.runner.call(job, command, work_dir=work_dir,
                                     outfile=vggenotype_stdout)
                timer.stop()
            vcf_id = context.write_intermediate_file(job, vcf_path)

        except Exception as e:
            logging.error("Genotyping failed. Dumping files.")
            for dump_path in [vg_path, aug_gam_path, aug_path]:
                if dump_path and os.path.isfile(dump_path):
                    context.write_output_file(job, dump_path)        
            raise e
                
    else:
        # call
        command = ['vg', 'call', os.path.basename(aug_path), '-t',
                   str(context.config.calling_cores), '-S', sample_name,
                   '-z', os.path.basename(trans_path),
                   '-s', os.path.basename(support_path),
                   '-b', os.path.basename(vg_path)]
                
        if call_opts:
            command += call_opts
        command += name_opts

        try:
            with open(vcf_path, 'w') as vgcall_stdout:
                timer.start('call')
                context.runner.call(job, command, work_dir=work_dir, outfile=vgcall_stdout)
                timer.stop()            

            vcf_id = context.write_intermediate_file(job, vcf_path)

        except Exception as e:
            logging.error("Calling failed. Dumping files.")
            for dump_path in [vg_path, pu_path, gam_filter_path,
                              aug_path, support_path, trans_path, aug_gam_path]:
                if dump_path and os.path.isfile(dump_path):
                    context.write_output_file(job, dump_path)        
            raise e
        
    return vcf_id, timer


def run_call_chunk(job, context, path_name, chunk_i, num_chunks, chunk_offset, clipped_chunk_offset,
                   xg_file_id, vg_chunk_file_id, gam_chunk_file_id, path_size, vcf_offset, sample_name,
                   genotype, recall):
    """ create VCF from a given chunk """

    # to encapsulate everything under this job
    child_job = Job()
    job.addChild(child_job)

    RealtimeLogger.info("Running call_chunk on path {} and chunk {}".format(path_name, chunk_i))
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # Run vg call
    call_job = child_job.addChildJobFn(
        run_vg_call,
        context, sample_name, vg_chunk_file_id, gam_chunk_file_id,
        xg_id = xg_file_id,
        path_names = [path_name], 
        seq_names = [path_name],
        seq_offsets = [chunk_offset + vcf_offset],
        seq_lengths = [path_size],
        chunk_name = 'chunk_{}_{}'.format(path_name, chunk_offset),
        genotype = genotype,
        recall = recall,
        cores=context.config.calling_cores,
        memory=context.config.calling_mem, disk=context.config.calling_disk)
    vcf_id, call_timer = call_job.rv(0), call_job.rv(1)

    clip_job = child_job.addFollowOnJobFn(run_clip_vcf, context, path_name, chunk_i, num_chunks, chunk_offset,
                                          clipped_chunk_offset, vcf_offset, vcf_id,
                                          cores=context.config.calling_cores,
                                          memory=context.config.calling_mem, disk=context.config.calling_disk)

    clip_file_id = clip_job.rv()
    return clip_file_id, call_timer

def run_clip_vcf(job, context, path_name, chunk_i, num_chunks, chunk_offset, clipped_chunk_offset, vcf_offset, vcf_id):
    """ clip the vcf to respect chunk """

     # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # output vcf name
    vcf_path = os.path.join(work_dir, 'chunk_{}_{}.vcf'.format(path_name, chunk_offset))
    job.fileStore.readGlobalFile(vcf_id, vcf_path + '.us')
    
    # Sort the output
    sort_vcf(job, context.runner, vcf_path + '.us', vcf_path)
    
    # do the vcf clip
    left_clip = 0 if chunk_i == 0 else context.config.overlap / 2
    right_clip = 0 if chunk_i == num_chunks - 1 else context.config.overlap / 2
    clip_path = os.path.join(work_dir, 'chunk_{}_{}_clip.vcf'.format(path_name, chunk_offset))
    with open(clip_path, "w") as clip_path_stream:
        offset = vcf_offset + 1
        command=['bcftools', 'view', '-t', '{}:{}-{}'.format(
            path_name, offset + clipped_chunk_offset + left_clip,
            offset + clipped_chunk_offset + context.config.call_chunk_size - right_clip - 1),
                 os.path.basename(vcf_path)]
        context.runner.call(job, command, work_dir=work_dir, outfile=clip_path_stream)

    # save clip.vcf files to job store
    clip_file_id = context.write_intermediate_file(job, clip_path)
    
    return clip_file_id

def run_all_calling(job, context, xg_file_id, chr_gam_ids, chr_gam_idx_ids, chroms, vcf_offsets, sample_name,
                    genotype=False, out_name=None, recall=False):
    """
    Call all the chromosomes and return a merged up vcf/tbi pair
    """
    # we make a child job so that all calling is encapsulated in a top-level job
    child_job = Job()
    job.addChild(child_job)
    vcf_tbi_file_id_pair_list = []
    call_timers_lists = []
    assert len(chr_gam_ids) > 0
    if not chr_gam_idx_ids:
        chr_gam_idx_ids = [None] * len(chr_gam_ids)
    assert len(chr_gam_ids) == len(chr_gam_idx_ids)
    for i in range(len(chr_gam_ids)):
        alignment_file_id = chr_gam_ids[i]
        alignment_index_id = chr_gam_idx_ids[i]
        if len(chr_gam_ids) > 1:
            # 1 gam per chromosome
            chr_label = [chroms[i]]
            chr_offset = [vcf_offsets[i]] if vcf_offsets else [0]
        else:
            # single gam with one or more chromosomes
            chr_label = chroms
            chr_offset = vcf_offsets if vcf_offsets else [0] * len(chroms)
        call_job = child_job.addChildJobFn(run_calling, context, xg_file_id,
                                           alignment_file_id, alignment_index_id, chr_label, chr_offset,
                                           sample_name, genotype=genotype, recall=recall,
                                           cores=context.config.call_chunk_cores,
                                           memory=context.config.call_chunk_mem,
                                           disk=context.config.call_chunk_disk)
        vcf_tbi_file_id_pair_list.append((call_job.rv(0), call_job.rv(1)))
        call_timers_lists.append(call_job.rv(2))
        
    if not out_name:
        out_name = sample_name
    return child_job.addFollowOnJobFn(run_merge_vcf, context, out_name, vcf_tbi_file_id_pair_list,
                                      call_timers_lists,
                                      cores=context.config.call_chunk_cores,
                                      memory=context.config.call_chunk_mem,
                                      disk=context.config.call_chunk_disk).rv()

def run_merge_vcf(job, context, out_name, vcf_tbi_file_id_pair_list, call_timers_lists = []):
    """ Merge up a bunch of chromosome VCFs """

    RealtimeLogger.info("Completed gam merging and gam path variant calling.")
    RealtimeLogger.info("Starting vcf merging vcf files.")

    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    timer = TimeTracker('merge-vcf')
    
    vcf_merging_file_key_list = [] 
    for i, vcf_tbi_file_id_pair in enumerate(vcf_tbi_file_id_pair_list):
        vcf_file = os.path.join(work_dir, 'vcf_chunk_{}.vcf.gz'.format(i))
        vcf_file_idx = '{}.tbi'.format(vcf_file)
        job.fileStore.readGlobalFile(vcf_tbi_file_id_pair[0], vcf_file)
        job.fileStore.readGlobalFile(vcf_tbi_file_id_pair[1], vcf_file_idx)
        vcf_merging_file_key_list.append(os.path.basename(vcf_file))

    vcf_merged_file_key = "" 
    if len(vcf_merging_file_key_list) > 1:
        # merge vcf files
        vcf_merged_file_key = "{}.vcf.gz".format(out_name)
        command = ['bcftools', 'concat', '-O', 'z', '-o', os.path.basename(vcf_merged_file_key)]
        command +=  vcf_merging_file_key_list
        context.runner.call(job, command, work_dir=work_dir)
        command=['bcftools', 'tabix', '-f', '-p', 'vcf', os.path.basename(vcf_merged_file_key)]
        context.runner.call(job, command, work_dir=work_dir)
    else:
        vcf_merged_file_key = vcf_merging_file_key_list[0]

    # save variant calling results to the output store
    out_store_key = "{}.vcf.gz".format(out_name)
    vcf_file = os.path.join(work_dir, vcf_merged_file_key)
    vcf_file_idx = vcf_file + ".tbi"
    
    vcf_file_id = context.write_output_file(job, vcf_file, out_store_path = out_store_key)
    vcf_idx_file_id = context.write_output_file(job, vcf_file_idx,
                                                out_store_path = out_store_key + '.tbi')

    # reduce all the timers here from the list of lists
    timer.stop()
    for call_timers in call_timers_lists:
        for call_timer in call_timers:
            timer.add(call_timer)

    if call_timers_lists:
        return vcf_file_id, vcf_idx_file_id, timer
    else:
        return vcf_file_id, vcf_idx_file_id

    
def run_calling(job, context, xg_file_id, alignment_file_id, alignment_index_id, path_names, vcf_offsets, sample_name,
                genotype, recall):
    """
    Call a single GAM.  Takes care of splitting the input into chunks based on one or more path,
    processing each chunk in parallel, then merging the result into a single vcf which is returned.
    """
    RealtimeLogger.info("Running variant calling on path(s) {} from alignment file {}".format(','.join(path_names), str(alignment_file_id)))
        
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # Tame for work files
    tag = path_names[0] if len(path_names) == 1 else 'chroms'

    # Download the input from the store
    xg_path = os.path.join(work_dir, 'graph.vg.xg')
    job.fileStore.readGlobalFile(xg_file_id, xg_path)
    gam_path = os.path.join(work_dir, '{}_{}.gam'.format(sample_name, tag))
    job.fileStore.readGlobalFile(alignment_file_id, gam_path)

    # Sort and index the GAM file if index not provided
    timer = TimeTracker('call-gam-index')    
    if alignment_index_id:
        gam_sort_path = gam_path
        gam_index_path = gam_sort_path + '.gai'
        job.fileStore.readGlobalFile(alignment_index_id, gam_index_path)
    else:
        gam_sort_path = gam_path + '.sorted.gam'
        gam_index_path = gam_sort_path + '.gai'
        with open(gam_sort_path, "w") as gam_sort_stream:
            gamsort_cmd = ['vg', 'gamsort', '-i', os.path.basename(gam_index_path), os.path.basename(gam_path),
                           '--threads', str(context.config.call_chunk_cores)]
            context.runner.call(job, gamsort_cmd, work_dir=work_dir, outfile=gam_sort_stream)
            # We may spend a lot of time on these, so drop them in the output store.
            context.write_output_file(job, gam_sort_path)
            context.write_output_file(job, gam_index_path)
    timer.stop()
    
    # Write a list of paths
    path_list = os.path.join(work_dir, 'path_list.txt')
    offset_map = dict()
    with open(path_list, 'w') as path_list_file:
        for i, path_name in enumerate(path_names):
            path_list_file.write(path_name + '\n')
            offset_map[path_name] = int(vcf_offsets[i]) if vcf_offsets else 0

    # Apply chunk override for recall.
    # Todo: fix vg chunk to only expand variants (not reference) so that we can leave this super high
    # all the time
    context_size = max(int(context.config.chunk_context), int(context.config.recall_context))
    
    # Chunk the graph and gam, using the xg and rocksdb indexes.
    # GAM index isn't passed but it needs to be next to the GAM file.
    output_bed_chunks_path = os.path.join(work_dir, 'output_bed_chunks_{}.bed'.format(tag))
    chunk_cmd = ['vg', 'chunk', '-x', os.path.basename(xg_path),
                 '-a', os.path.basename(gam_sort_path), '-c', str(context_size),
                 '-P', os.path.basename(path_list),
                 '-g',
                 '-s', str(context.config.call_chunk_size),
                 '-o', str(context.config.overlap),
                 '-b', 'call_chunk_{}'.format(tag),
                 '-t', str(context.config.call_chunk_cores),
                 '-E', os.path.basename(output_bed_chunks_path),
                 '-f']
    timer.start('call-chunk')
    context.runner.call(job, chunk_cmd, work_dir=work_dir)
    timer.stop()

    # Scrape the BED into memory
    bed_lines = []
    path_bounds = dict()    
    with open(output_bed_chunks_path) as output_bed:
        for line in output_bed:
            toks = line.split('\t')
            if len(toks) > 3:
                bed_lines.append(toks)
                chrom, start, end = toks[0], int(toks[1]), int(toks[2])
                if chrom not in path_bounds:
                    path_bounds[chrom] = (start, end)
                else:
                    path_bounds[chrom] = (min(start, path_bounds[chrom][0]),
                                              max(end, path_bounds[chrom][1]))

    # Infer the size of the path from our BED (a bit hacky)
    path_size = dict()
    for name, bounds in path_bounds.items():
        path_size[name] = path_bounds[name][1] - path_bounds[name][0]

    # Keep track of offset in each path
    cur_path_offset = defaultdict(int)

    # to encapsulate everything under this job
    child_job = Job()
    job.addChild(child_job)
        
    # Go through the BED output of vg chunk, adding a child calling job for
    # each chunk                
    clip_file_ids = []
    call_timers = [timer]
    for toks in bed_lines:
        chunk_bed_chrom = toks[0]
        chunk_bed_start = int(toks[1])
        chunk_bed_end = int(toks[2])
        chunk_bed_size = chunk_bed_end - chunk_bed_start
        gam_chunk_path = os.path.join(work_dir, os.path.basename(toks[3].strip()))
        assert os.path.splitext(gam_chunk_path)[1] == '.gam'
        vg_chunk_path = os.path.splitext(gam_chunk_path)[0] + '.vg'
        gam_chunk_file_id = context.write_intermediate_file(job, gam_chunk_path)
        vg_chunk_file_id = context.write_intermediate_file(job, vg_chunk_path)
        chunk_i = cur_path_offset[chunk_bed_chrom]        
        clipped_chunk_offset = chunk_i * context.config.call_chunk_size - chunk_i * context.config.overlap
        cur_path_offset[chunk_bed_chrom] += 1

        call_job =  child_job.addChildJobFn(run_call_chunk, context, chunk_bed_chrom, chunk_i,
                                            len(bed_lines),
                                            chunk_bed_start, clipped_chunk_offset,
                                            None, vg_chunk_file_id, gam_chunk_file_id,
                                            path_size[chunk_bed_chrom], offset_map[chunk_bed_chrom],
                                            sample_name, genotype, recall,
                                            cores=context.config.misc_cores,
                                            memory=context.config.misc_mem, disk=context.config.misc_disk)
        clip_file_ids.append(call_job.rv(0))
        call_timers.append(call_job.rv(1))
        
    merge_job = child_job.addFollowOnJobFn(run_merge_vcf_chunks, context, tag,
                                           clip_file_ids,
                                           cores=context.config.call_chunk_cores,
                                           memory=context.config.call_chunk_mem,
                                           disk=context.config.call_chunk_disk)
        
    vcf_out_file_id = merge_job.rv(0)
    tbi_out_file_id = merge_job.rv(1)
    
    return vcf_out_file_id, tbi_out_file_id, call_timers


def run_merge_vcf_chunks(job, context, path_name, clip_file_ids):
    """ merge a bunch of clipped vcfs created above, taking care to 
    fix up the headers.  everything expected to be sorted already """
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()
    
    vcf_path = os.path.join(work_dir, path_name + ".vcf")
    
    for chunk_i, clip_file_id in enumerate(clip_file_ids):
        
        # Download clip.vcf file from the store
        clip_path = os.path.join(work_dir, 'clip_{}.vcf'.format(chunk_i))
        job.fileStore.readGlobalFile(clip_file_id, clip_path)

        if chunk_i == 0:
            # copy everything including the header
            with open(vcf_path, "w") as outfile:
                context.runner.call(job, ['cat', os.path.basename(clip_path)], outfile=outfile,
                                     work_dir=work_dir)
        else:
            # add on everythin but header
            with open(vcf_path, "a") as outfile:
                context.runner.call(job, ['bcftools', 'view', '-H', os.path.basename(clip_path)],
                                     outfile=outfile, work_dir=work_dir)

    # add a compressed indexed version
    vcf_gz_file = vcf_path + ".gz"
    with open(vcf_gz_file, "w") as vcf_gz_file_stream:
        command=['bgzip', '-c', '{}'.format(os.path.basename(vcf_path))]
        context.runner.call(job, command, work_dir=work_dir, outfile=vcf_gz_file_stream)
    command=['bcftools', 'tabix', '-f', '-p', 'vcf', '{}'.format(os.path.basename(vcf_path+".gz"))]
    context.runner.call(job, command, work_dir=work_dir)

    # Save merged vcf files to the job store
    vcf_gz_file_id = context.write_intermediate_file(job, vcf_path+".gz")
    vcf_tbi_file_id = context.write_intermediate_file(job, vcf_path+".gz.tbi")

    RealtimeLogger.info("Completed variant calling on path {}".format(path_name))

    return vcf_gz_file_id, vcf_tbi_file_id
    
def call_main(context, options):
    """ entrypoint for calling """

    validate_call_options(options)
            
    # How long did it take to run the entire pipeline, in seconds?
    run_time_pipeline = None
        
    # Mark when we start the pipeline
    start_time_pipeline = timeit.default_timer()
    
    with context.get_toil(options.jobStore) as toil:
        if not toil.options.restart:

            importer = AsyncImporter(toil)

            # Upload local files to the job store
            inputXGFileID = importer.load(options.xg_path)
            inputGamFileIDs = []
            inputGamIndexFileIDs = []
            for inputGam in options.gams:
                inputGamFileIDs.append(importer.load(inputGam))
                try:
                    inputGamIndexID = toil.importFile(inputGam + '.gai')
                except:
                    inputGamIndexID = None
                # we allow some GAMs to have indexes and some to have None
                inputGamIndexFileIDs.append(inputGamIndexID)

            importer.wait()

            # Make a root job
            root_job = Job.wrapJobFn(run_all_calling, context, importer.resolve(inputXGFileID),
                                     importer.resolve(inputGamFileIDs), inputGamIndexFileIDs,
                                     options.chroms, options.vcf_offsets, options.sample_name,
                                     genotype=options.genotype, recall=options.recall,
                                     cores=context.config.misc_cores,
                                     memory=context.config.misc_mem,
                                     disk=context.config.misc_disk)

            # Init the outstore
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            init_job.addFollowOn(root_job)            
            
            # Run the job and store the returned list of output files to download
            toil.start(init_job)
        else:
            toil.restart()
                
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
 
    logger.info("All jobs completed successfully. Pipeline took {} seconds.".format(run_time_pipeline))
    
    
    
