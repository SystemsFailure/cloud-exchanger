import typer

def validation_password(vl: str):
    if vl != 'Eric':
        return vl
    else:
        raise typer.BadParameter('You not to write param, check...')

def validation_path(vl: str):
    if vl == '':
        return False
    else:
        return vl

def validation_path_file_from_cloud(vl:str):
    if vl == '':
        return False
    else:
        return vl

def validation_bucket_name(vl: str):
    if vl == '':
        return False
    else:
        return vl

def validation_list(list_: list):
    if list_.__len__ == 0:
        return False
    else:
        return list_