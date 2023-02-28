from rich.console import Console
from src.controllers.files_controller import upload_blob, download_as_file, LocalStoreInstance
import typer
from time import sleep
from halo import Halo
from src.commands.validations.valid_ import validation_path_file_from_cloud, validation_list

proj_id = 'exchangefiles-ae5e7'
bucket_name = 'exchangefiles-ae5e7.appspot.com'
street_group = "[green]LIST CLOUD METHODS[gren]"


app = typer.Typer(rich_markup_mode='rich')
console = Console()
loader = Halo(text='uploading...', spinner='dots')

@app.command('create', rich_help_panel="[blue]Secondary Arguments[blue]")
def create_function(username: str = typer.Argument(..., help="the last ooopppss")):
    """
        [green]Active[green]
    """
    console.print("[turquoise2]{}[turquoise2]".format(username))

@app.command('delete-confirm')
def delete_confirm(username):
    """name user is greet"""
    delete = typer.confirm('Are you sure that want to del this user?', abort=True)
    if delete:
        console.print("[turquoise2]{}".format(username))
    else:
        console.print("[red]No choice")

@app.command('cl')
def cl(panel: str = typer.Option(..., '--pl', '-p')):
    loader.start()
    sleep(3)
    loader.stop_and_persist(symbol='✅', text='successful scan')
    console.print('[turquoise2] panel - {} start...'.format(panel))

@app.command('upload', rich_help_panel=street_group)
def upload(filename: str, filepath: str = typer.Option(..., '--path', '-p', prompt='fil field 1 - filename, 2 - path to file')):
    if filename != '':
        if filepath != '':
            loader.start()
            upload_blob(
                    project_id=proj_id,
                    bucket_name=bucket_name,
                    source_file_name=filepath,
                    location_blob_name=filename
                )
            loader.stop_and_persist(symbol='✅', text='upload of file is success')
        else: 
            # raise typer.BadParameter('check params which you sended above.')
            console.print('BadParameter : [red]Failure[red] - check params which you sended above.')
    else: 
        # raise typer.BadParameter('check params which you sended above.')
        console.print('BadParameter : [red]Failure[red] - check params which you sended above.')

@app.command('list', rich_help_panel=street_group)
def get_list(beuty:bool = typer.Option(True, '--beutyout', '-bo')):
    if beuty == False:
        return
    else:
        loader.start()
        loader.text = 'getting list files...'
        loader.spinner = 'dots'
        cloud = LocalStoreInstance()
        lst = cloud.get_list_blobs()
        valid_lst = validation_list(lst)
        if lst == False:
            return
        loader.stop_and_persist(symbol='✅', text='list got is success')
        for it in valid_lst:
            console.print(f'file - {it}')


@app.command('download', rich_help_panel=street_group)
def download(
            path_to_blob_cloud_file: str = typer.Option(..., '--blob_path', '-bp', prompt='name or path to cloud file'),
            location_: str = typer.Option(..., '--location', '-l')
        ):
            loader.start()
            loader.text = 'downloading...'
            valid_path = validation_path_file_from_cloud(path_to_blob_cloud_file)
            if not valid_path:
                return
            download_as_file(source_blob_name=valid_path, location_file=location_)
            loader.stop_and_persist(symbol='✅', text='download of file is success')


if __name__ == "__main__":
    app()