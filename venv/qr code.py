
import firebase.firebase as firebase
path = firebase.FirebaseApplication("https://rapidstore.firebaseio.com/")

data = {"Name":"haha"}

path.post("Users", data)