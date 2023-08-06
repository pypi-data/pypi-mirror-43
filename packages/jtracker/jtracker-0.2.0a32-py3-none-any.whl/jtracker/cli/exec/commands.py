import click
from jtracker.execution import Executor


@click.command()
@click.option('-q', '--queue-id', help='Job queue ID')
@click.option('-k', '--parallel-workers', type=int, default=2, help='Max number of parallel workers')
@click.option('-p', '--parallel-jobs', type=int, default=1, help='Max number of parallel running jobs')
@click.option('-m', '--max-jobs', type=int, default=0, help='Max number of jobs to be run by the executor')
@click.option('-d', '--min-disk', type=int, default=0, help='Min required free disk space (in GB)')
@click.option('-b', '--job-id', help='Execute specified job')
@click.option('-j', '--job-file', type=click.Path(exists=True), help='Execute local job file')
@click.option('-w', '--workflow-name', help='Specify registered workflow name in format: [{owner}/]{workflow}:{ver}')
@click.option('-t', '--retries', type=click.IntRange(0, 3), default=2, help='Set retry attempts (0-3) for failed task')
@click.option('-f', '--force-restart', is_flag=True, help='Force executor restart, set previous running jobs to cancelled')
@click.option('-r', '--resume-job', is_flag=True, help='Force executor restart, set previous running jobs to resume')
@click.option('-i', '--polling-interval', type=int, default=10, help='Time interval the executor checks for new task')
@click.pass_context
def run(ctx, job_file, job_id, queue_id, force_restart, resume_job,
             workflow_name, parallel_jobs, max_jobs, min_disk, parallel_workers, retries,
             polling_interval):
    """
    Launch JTracker executor
    """
    jt_executor = None
    try:
        jt_executor = Executor(jt_home=ctx.obj['JT_CONFIG'].get('jt_home'),
                               jt_account=ctx.obj['JT_CONFIG'].get('jt_account'),
                               ams_server=ctx.obj['JT_CONFIG'].get('ams_server'),
                               wrs_server=ctx.obj['JT_CONFIG'].get('wrs_server'),
                               jess_server=ctx.obj['JT_CONFIG'].get('jess_server'),
                               job_file=job_file,
                               job_id=job_id,
                               queue_id=queue_id,
                               workflow_name=workflow_name,
                               parallel_jobs=parallel_jobs,
                               max_jobs=max_jobs,
                               min_disk=min_disk * 1000000000,
                               parallel_workers=parallel_workers,
                               retries=retries,
                               force_restart=force_restart,
                               resume_job=resume_job,
                               polling_interval=polling_interval,
                               logger=ctx.obj.get('LOGGER')
                               )
    except Exception as e:
        click.echo(str(e))
        click.echo('For usage: jt exec run --help')
        ctx.abort()

    if jt_executor:
        jt_executor.run()


@click.command()
@click.pass_context
def ls(ctx, job_file, job_id, queue_id, executor_id):
    click.echo('Listing executors not implemented yet')
