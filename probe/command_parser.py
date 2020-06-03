#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/22 1:26 PM
__author__ = 'Zhou Ran'

import os
import sys
import argparse
import textwrap
from Bio.SeqUtils import MeltingTemp as mt

from .GeneToTrans import generateinfo
from .GenerateBlock import runSequenceCrawler
from .AlignmentFilter import BlockParser, JuncParser
from .Junc import fetchjunc, fetchcirc
from .version import __version__


def transcript(args):
    """
    too many parameters!!!
    :param args:
    :return:
    """
    fasta = args.fastaC
    targetfile = args.target
    outputprefix = args.outprefix
    l = args.minLength
    L = args.maxLength
    gcPercent = args.min_GC
    GCPercent = args.max_GC
    tm = args.min_Tm
    TM = args.max_Tm
    X = args.prohibitedSeqs
    sal = args.salt
    form = args.formamide
    sp = args.Spacing
    OverlapModeVal = args.OverlapMode
    verbocity = args.verbose
    index = args.index
    probelength = args.probelength
    entropy = args.entropy
    hytemp = args.hytemp
    mfold = args.mfold
    thread = args.thread
    detG = args.detG
    cDNA = args.cDNA
    vargibbs = args.vargibbs
    par = args.par
    saltscheme = args.saltscheme
    ct = args.ct

    if args.dnac1 >= args.dnac2:
        conc1 = args.dnac1
        conc2 = args.dnac2

    else:
        conc1 = args.dnac2
        conc2 = args.dnac1

    exec('nn_table = mt.%s' % args.nn_table, None, globals())
    falist = generateinfo(fasta, targetfile, outputprefix)
    for sub in falist:
        subprefix = os.path.splitext(sub)[0]
        runSequenceCrawler(sub, l, L, gcPercent, GCPercent, nn_table, tm, TM, X, sal, form, sp, conc1, conc2,
                           OverlapModeVal, subprefix, entropy, vargibbs, par, saltscheme, ct)

        BlockParser('.'.join([subprefix, 'fastq']), index, '.'.join([outputprefix, 'layerinfo.txt']),
                    '.'.join([subprefix, 'result']), sal, form, probelength, hytemp, thread, detG, cDNA, mfold_=mfold,
                    verbose=verbocity)


def junction(args):
    # fastaC = args.fastaC
    fastaG = args.fastaG
    targetfile = args.target
    outputprefix = args.outprefix
    l = args.minLength
    L = args.maxLength
    gcPercent = args.min_GC
    GCPercent = args.max_GC
    tm = args.min_Tm
    TM = args.max_Tm
    X = args.prohibitedSeqs
    sal = args.salt
    form = args.formamide
    sp = args.Spacing
    OverlapModeVal = args.OverlapMode
    verbocity = args.verbose
    index = args.index
    probelength = args.probelength
    entropy = args.entropy
    hytemp = args.hytemp
    thread = args.thread
    mfold = args.mfold
    detG = args.detG
    cDNA = args.cDNA
    vargibbs = args.vargibbs
    par = args.par
    saltscheme = args.saltscheme
    ct = args.ct

    if args.dnac1 >= args.dnac2:
        conc1 = args.dnac1
        conc2 = args.dnac2

    else:
        conc1 = args.dnac2
        conc2 = args.dnac1

    exec('nn_table = mt.%s' % args.nn_table, None, globals())
    falist = fetchjunc(fastaG, targetfile, outputprefix)
    for sub in falist:
        subprefix = os.path.splitext(sub)[0]
        runSequenceCrawler(sub, l, L, gcPercent, GCPercent, nn_table, tm, TM, X, sal, form, sp, conc1, conc2,
                           OverlapModeVal, subprefix, entropy,vargibbs, par, saltscheme, ct)

        JuncParser('.'.join([subprefix, 'fastq']), index, os.path.join(outputprefix, 'config.txt'),
                   '.'.join([subprefix, 'result']), sal, form, probelength, hytemp, thread, detG, cDNA, mfold_=mfold,
                   verbose=verbocity)


def circ(args):
    fastaG = args.fastaG
    targetfile = args.target
    outputprefix = args.outprefix
    l = args.minLength
    L = args.maxLength
    gcPercent = args.min_GC
    GCPercent = args.max_GC
    tm = args.min_Tm
    TM = args.max_Tm
    X = args.prohibitedSeqs
    sal = args.salt
    form = args.formamide
    sp = args.Spacing
    OverlapModeVal = args.OverlapMode
    verbocity = args.verbose
    index = args.index
    probelength = args.probelength
    entropy = args.entropy
    hytemp = args.hytemp
    thread = args.thread
    mfold = args.mfold
    detG = args.detG
    cDNA = args.cDNA
    vargibbs = args.vargibbs
    par = args.par
    saltscheme = args.saltscheme
    ct = args.ct

    if args.dnac1 >= args.dnac2:
        conc1 = args.dnac1
        conc2 = args.dnac2

    else:
        conc1 = args.dnac2
        conc2 = args.dnac1

    exec('nn_table = mt.%s' % args.nn_table, None, globals())
    falist = fetchcirc(fastaG, targetfile, outputprefix)
    for sub in falist:
        subprefix = os.path.splitext(sub)[0]
        runSequenceCrawler(sub, l, L, gcPercent, GCPercent, nn_table, tm, TM, X, sal, form, sp, conc1, conc2,
                           OverlapModeVal, subprefix, entropy, vargibbs, par, saltscheme, ct)

        JuncParser('.'.join([subprefix, 'fastq']), index, os.path.join(outputprefix, 'config.txt'),
                   '.'.join([subprefix, 'result']), sal, form, probelength, hytemp, thread, detG, cDNA, mfold_=mfold,
                   verbose=verbocity)


def arg():
    probedesign = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False,
                                          description=textwrap.dedent("""
__________              ___.          ________                .__               
\______   \_______  ____\_ |__   ____ \______ \   ____   _____|__| ____   ____  
 |     ___/\_  __ \/  _ \| __ \_/ __ \ |    |  \_/ __ \ /  ___/  |/ ___\ /    \ 
 |    |     |  | \(  <_> ) \_\ \  ___/ |    `   \  ___/ \___ \|  / /_/  >   |  \

 |____|     |__|   \____/|___  /\___  >_______  /\___  >____  >__\___  /|___|  /
                             \/     \/        \/     \/     \/  /_____/      \/                              """))

    probedesign.add_argument('-ta', '--target', action='store',
                             type=str, required=True,
                             help='A config file')
    probedesign.add_argument('-op', '--outprefix', action='store',
                             type=str, required=True,
                             help='output folder prefix')
    probedesign.add_argument('-index', '--index', action='store',
                             type=str, required=True,
                             help='bowtie2 index files, generate by modified cDNA fasta.')
    probedesign.add_argument('-l', '--minLength', action='store', default=36,
                             type=int,
                             help='The minimum allowed probe length; default is '
                                  '36')
    probedesign.add_argument('-L', '--maxLength', action='store', default=41,
                             type=int,
                             help='The maximum allowed probe length, default is '
                                  '41')
    probedesign.add_argument('-g', '--min_GC', action='store', default=20,
                             type=int,
                             help='The minimum allowed percent G + C, default is '
                                  '20')
    probedesign.add_argument('-G', '--max_GC', action='store', default=80,
                             type=int,
                             help='The maximum allowed percent  G + C, default '
                                  'is 80')
    probedesign.add_argument('-t', '--min_Tm', action='store', default=54,
                             type=int,
                             help='The minimum allowed Tm, default is 54')
    probedesign.add_argument('-T', '--max_Tm', action='store', default=60,
                             type=int,
                             help='The maximum allowed Tm, default is 60')
    probedesign.add_argument('-X', '--prohibitedSeqs', action='store',
                             default='AAAAA,TTTTT,CCCCC,GGGGG', type=str,
                             help='Prohibited sequence list (separated by commas '
                                  'with no spaces), default is '
                                  '\'AAAAA,TTTTT,CCCCC,GGGGG\'')
    probedesign.add_argument('-s', '--salt', action='store', default=390,
                             type=int,
                             help='The mM Na+ concentration, default is 390')
    probedesign.add_argument('-F', '--formamide', action='store', default=50,
                             type=float,
                             help='The percent formamide being used, default is '
                                  '50')
    probedesign.add_argument('-c', '--dnac1', action='store', default=25,
                             type=float,
                             help='Concentration of higher concentration strand '
                                  '[nM] -typically the probe- to use for '
                                  'thermodynamic calculations. Default is 25')
    probedesign.add_argument('-C', '--dnac2', action='store', default=25,
                             type=float,
                             help='Concentration of lower concentration strand '
                                  '[nM] -typically the target- to use for '
                                  'thermodynamic calculations. Default is 25')
    probedesign.add_argument('-S', '--Spacing', action='store', default=0,
                             type=int,
                             help='The minimum spacing between adjacent probes, '
                                  'default is 0 bases')
    probedesign.add_argument('-n', '--nn_table', action='store',
                             default='DNA_NN3',
                             type=str,
                             help='The nearest neighbor table of thermodynamic '
                                  'parameters to be used. See options in '
                                  'Bio.SeqUtils.MeltingTemp. Default is DNA_NN3')
    probedesign.add_argument('-H', '--header', action='store', type=str,
                             help='Allows the use of a custom header in the '
                                  'format chr:start-stop. E.g. '
                                  '\'chr2:12500-13500\'')
    probedesign.add_argument('-O', '--OverlapMode', action='store_true',
                             default=False,
                             help='Turn on Overlap Mode, which returns all '
                                  'possible candidate probes in a block of '
                                  'sequence including overlaps. Off by default. '
                                  'Note, if selecting this option, the '
                                  '-S/--Spacing value will be ignored')
    probedesign.add_argument('-v', '--verbose', action='store_true',
                             default=False,
                             help='Verbose mode. Output the alignment results.')
    probedesign.add_argument('-pl', '--probelength', action='store', type=int, default=70,
                             help='PLP length,default:70')
    probedesign.add_argument('-ep', '--entropy', action='store', type=float, default=1.0,
                             help='Shannon entropy, default:1.0')

    probedesign.add_argument('-ht', '--hytemp', action='store', default=37.0,
                             type=float,
                             help='The temperature at which you want to '
                                  'hybridize your probes')
    probedesign.add_argument('-mf', '--mfold', action='store_true', default=False,
                             help='')
    probedesign.add_argument('-dG', '--detG', action='store', type=float, default=0.0,
                             help='Accept detG value filtering for secondary structure check using mfold. \
                             Probes with absolute values of detG lower than this argument will be kept.')
    probedesign.add_argument('-td', '--thread', action='store', type=int, default=4,
                             help='Multipleprocess to speed the mfold')
    probedesign.add_argument('-bwp', '--bw_param', action='store',
                             default='bw_param',
                             type=str,
                             help='bowtie2 parameters')
    probedesign.add_argument('-cD', '--cDNA', action='store_true', default=False,
                             help='cDNA mode, if true, padlock probes will be hybridized to cDNA instead of RNA')
    probedesign.add_argument('--vargibbs', action='store', type=str,
                             help='vargibbs location')
    probedesign.add_argument('--par', action='store', type=str,
                             help='vargibbs par file')
    probedesign.add_argument('--saltscheme', action='store', type=str,
                             help='saltscheme')
    probedesign.add_argument('--ct', action='store',type=float,default=0.3,
                             help='ct value')

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent("""
__________              ___.          ________                .__               
\______   \_______  ____\_ |__   ____ \______ \   ____   _____|__| ____   ____  
 |     ___/\_  __ \/  _ \| __ \_/ __ \ |    |  \_/ __ \ /  ___/  |/ ___\ /    \ 
 |    |     |  | \(  <_> ) \_\ \  ___/ |    `   \  ___/ \___ \|  / /_/  >   |  \\
 |____|     |__|   \____/|___  /\___  >_______  /\___  >____  >__\___  /|___|  /
                             \/     \/        \/     \/     \/  /_____/      \/                             """))

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help, version: {}'.format(__version__),
                                       dest='action')

    transcript_parse = subparsers.add_parser('transcripts', parents=[probedesign], help='For transcripts ID')
    transcript_parse.add_argument('-faC', '--fastaC', action='store',
                                  type=str,
                                  help='cDNA fasta file, must be modified')
    transcript_parse.set_defaults(func=transcript)

    junction_parse = subparsers.add_parser('junction', parents=[probedesign], help='For splicing junction')
    junction_parse.add_argument('-faG', '--fastaG', action='store', required=True,
                                type=str,
                                help='whole genome fasta file')
    junction_parse.add_argument('-faC', '--fastaC', action='store',
                                type=str,
                                help='cDNA fasta file, must be modified')

    junction_parse.set_defaults(func=junction)

    circ_parse = subparsers.add_parser('circ', parents=[probedesign], help='For circRNA junction')
    circ_parse.add_argument('-faG', '--fastaG', action='store', required=True,
                            type=str,
                            help='whole genome fasta file')
    circ_parse.set_defaults(func=circ)

    # index_parse = subparsers.add_parser('index', parents=[probedesign], help='For index, still in test')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main():
    args = arg()
    args.func(args)


if __name__ == '__main__':
    main()
