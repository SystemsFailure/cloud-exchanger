import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class StoreInstance:
    cred = credentials.Certificate('/home/leonhard/Desktop/exchangefiles/secret_key/exchangefiles-ae5e7-firebase-adminsdk-rnx2p-151c4ed367.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    def __init__(self) -> None:
        pass

    def setInstanceObjectToStore(self, filename, size, filepath, index):

        data = {
            'filename': filename,
            'size': size,
            'filepath': filepath,
            'index': index
        }
        self.db.collection('filesInstances').add(data)


    def getListObjectsFromStore(self) -> list:
        lst_docs = []
        docs = self.db.collection('filesInstances').stream()
        for doc in docs:
            data = {
                'filename': doc.to_dict()['filename'] or None,
                # 'filepath': doc.to_dict()['filepath'] or None,
                'size': doc.to_dict()['size'] or None,
                'index': doc.to_dict()['index'] or None,
            }
            lst_docs.append(data)
        return lst_docs

    def increment(self):
        ref = self.db.collection('indexFile').document('lGF6R9FebHGhzu89h2W9')
        ref.update({'index': firestore.Increment(1)})
        doc = ref.get()
        if doc.exists:
            return doc.to_dict()['index']
        else:
            return False

