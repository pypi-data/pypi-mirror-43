from os import path

import bglogs
import click

from bgsignature import main, file


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def check_kmer_size(ctx, param, value):
    if value < 3 or value % 2 == 0:
        raise click.BadParameter('Not an odd value')
    else:
        return value


def check_file_not_exists(ctx, param, value):
    if value is not None and path.exists(value):
        raise click.BadParameter('Output file cannot exists: {}'.format(value))
    else:
        return value


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', default=False, help='Give more output (verbose)')
@click.version_option()
def cli(debug):
    """Compute the k-mer signature of a mutation or a regions file.
    If both are provided, the signature is computed from the
    mutation that map to the regions

    When grouping the signature, you can use SAMPLE, CANCER_TYPE, SIGNATURE
    for mutation and ELEMENT or SYMBOL for regions provided that
    those columns exist in the corresponding inpu file"""
    bglogs.configure(debug=debug)
    bglogs.configure('bgparsers')


@cli.command()
@click.option('--mutations', '-m', default=None, type=click.Path(exists=True), help='Mutations file')
@click.option('--regions', '-r', default=None, type=click.Path(exists=True), help='Regions file')
@click.option('--size', '-s', 'kmer', default=3, type=int, callback=check_kmer_size, help='Size of the kmer to analyze')
@click.option('--genome', '-g', default='hg19', help='Reference genome')
@click.option('--collapse/--no-collapse', 'collapse', default=True, help='Add reverse complementaries')
@click.option('--group', default=None, type=click.Choice(['SAMPLE', 'CANCER_TYPE', 'SIGNATURE', 'ELEMENT', 'SYMBOL']), help='Field to group the signature by')
@click.option('--include-N/--exclude-N', 'includeN', default=False, help="Include k-mers with N nucleotides")
@click.option('--cores', default=None, type=int, help='Cores for paralellization. Default no parallelization')
@click.option('--output', '-o', default=None, type=click.Path(), callback=check_file_not_exists, help="Output file. Default to STDOUT.")
def count(mutations, regions, kmer, genome, collapse, includeN, group, cores, output):
    """Get the counts of the k-mers in regions or mutations file"""
    result = main.count(mutations, regions, kmer, genome, collapse=collapse, includeN=includeN, group=group, cores=cores)
    file.save(result, output)


@cli.command()
@click.option('--mutations', '-m', default=None, type=click.Path(exists=True), help='Mutations file')
@click.option('--regions', '-r', default=None, type=click.Path(exists=True), help='Regions file')
@click.option('--size', '-s', 'kmer', default=3, type=int, callback=check_kmer_size, help='Size of the kmer to analyze')
@click.option('--genome', '-g', default='hg19', help='Reference genome')
@click.option('--collapse/--no-collapse', 'collapse', default=True, help='Add reverse complementaries')
@click.option('--group', default=None, type=click.Choice(['SAMPLE', 'CANCER_TYPE', 'SIGNATURE', 'ELEMENT', 'SYMBOL']), help='Field to group the signature by')
@click.option('--include-N/--exclude-N', 'includeN', default=False, help="Include k-mers with N nucleotides")
@click.option('--cores', default=None, type=int, help='Cores for paralellization. Default no parallelization')
@click.option('--output', '-o', default=None, type=click.Path(), callback=check_file_not_exists, help="Output file. Default to STDOUT.")
def frequency(mutations, regions, kmer, genome, collapse, includeN, group, cores, output):
    """Get the relative frequency of the k-mers in regions or mutations"""
    result = main.relative_frequency(mutations, regions, kmer, genome, collapse=collapse, includeN=includeN, group=group, cores=cores)
    file.save(result, output)


@cli.command()
@click.option('--mutations', '-m', default=None, type=click.Path(exists=True), help='Mutations file')
@click.option('--regions', '-r', default=None, type=click.Path(exists=True), help='Regions file')
@click.option('--size', '-s', 'kmer', default=3, type=int, callback=check_kmer_size, help='Size of the kmer to analyze')
@click.option('--genome', '-g', default='hg19', help='Reference genome')
@click.option('--normalize', 'norm', default=None, type=click.Path(exists=True), help="Normalized the counts. Default normalize by the counts in regions")
@click.option('--collapse/--no-collapse', 'collapse', default=True, help='Add reverse complementaries')
@click.option('--group', default=None, type=click.Choice(['SAMPLE', 'CANCER_TYPE', 'SIGNATURE', 'ELEMENT', 'SYMBOL']), help='Field to group the signature by')
@click.option('--include-N/--exclude-N', 'includeN', default=False, help="Include k-mers with N nucleotides")
@click.option('--cores', default=None, type=int, help='Cores for paralellization. Default no parallelization')
@click.option('--output', '-o', default=None, type=click.Path(), callback=check_file_not_exists, help="Output file. Default to STDOUT.")
def normalize(mutations, regions, kmer, genome, norm, collapse, includeN, group, cores, output):
    """Get the probability of k-mers in regions or mutations normalized by the counts in certain regions"""
    result = main.normalize(mutations, regions, kmer, genome, normalize_file=norm, collapse=collapse, includeN=includeN, group=group, cores=cores)
    file.save(result, output)


if __name__ == "__main__":
    cli()
