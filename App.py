import streamlit as st
import numpy as np
from SessionState import SessionState, get
import pyrebase
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re

class App:
    def __init__(self):
        self.state = get(firebase=None, auth=None, db=None, loggedIn=False, user=None, fName=None)
        self._connect_to_api()

    def run(self):
        if self.state.loggedIn:
            self.displayUserContent()
        else:
            self.displayLoginDetails()

            # display a wordcloud of all family data.
            st.title("Thanksgiving Reflections")
            st.write("Join to keep track of what you are thankful for this year!")
            familyCount = self._getFamilyCount()
            st.write("So far ", familyCount, " families have joined.\n\n ")
            if familyCount > 0:
                st.write("_Here is a sneak peak of what everyone is thankful for._")

                # display word cloud
                self.displayAllFamiliesData()
            else:
                st.write("You could be the first to join. ")


    def _connect_to_api(self):
        firebaseConfig = {
            "apiKey": " AIzaSyAK1RGl-WK5hTU1xDKMjJL6qG8bMG0_xy4 ",
            "authDomain": "thankful-10af0.firebaseapp.com",
            "databaseURL": "https://thankful-10af0.firebaseio.com",
            "projectId": "thankful-10af0",
            "storageBucket": "thankful-10af0.appspot.com",
            "messagingSenderId": "495459381997",
            "appId": "1:495459381997:web:5a879bf5b32e5c4be752e4",
            "serviceAccount": "./firebase_service_account.json"
        }
        self.state.firebase = pyrebase.initialize_app(firebaseConfig)
        self.state.auth = self.state.firebase.auth()
        self.state.db = self.state.firebase.database()

    def displayLoginDetails(self):
        st.sidebar.markdown("""
        # Log in with your family to keep track of what everyone is thankful for!
        New here? come up with a fun and unique family name. If you already have one, welcome back!

        Feel free to share these log in details with your extended family so they can join the fun.
         Come back after Thanksgiving to see what everyone entered.
         """)
        familyName = st.sidebar.text_input("What is your family name?")
        email = st.sidebar.text_input("Enter new or pre-registered email")
        newFam = st.sidebar.button("New Fam Enter Here")
        oldFam = st.sidebar.button("Existing Fam Enter Here")

        if newFam and len(familyName) > 0 and len(email) > 0:
            self._createNewFamily(email, familyName)

        elif oldFam and len(familyName) > 0 and len(email) > 0:
            user = self._signInFamily(email, familyName)
        else:
            self.state.loggedIn = False

    def displayUserContent(self):
        st.write("# Welcome ", self.state.fName, " we're glad you're here.")
        st.write("Thanksgiving is the season to reflect before the beginning of the new year. "
                 "Let your mind pleasantly wonder over the good memories, moments you laughed hard, tried new things, "
                 " explored new places, and spent quality time with friends and family. \n\nEven if times were not always good, "
                 "remember you have perservered and made it to the place you are today. In the face of grief or hardship "
                 "there are always small lessons and blessings to be thankful for. \n\nTo end this thoughtful journey reflect "
                 "on the things you love most, who or what inspired you, and what your future goals may be.  \n\n\n"
                 "Finally, sit down as a family and think of a couple things you are all grateful for this season. :)")
        st.sidebar.markdown("Enter your responses here")

        userList = st.sidebar.text_input("Enter items as a comma separated list or one at a time")
        thanks = st.sidebar.button("Give thanks")
        if thanks and len(userList) > 0:
            self._updateUserThanfulList(userList)

        self.displayFamilyData()

        st.subheader("Feel free to share your family log in information with extended family."
                     " You will be able to see a mixture of what people are thankful for.")

        # refresh user token if needed
        if self.state.user != None and self.state.user["expiresIn"] == 0:
            self.state.user = self.state.auth.refresh(self.state.user['refreshToken'])

    def _displayWordCloud(self, data, maskImage):
        mask = np.array(Image.open(maskImage))
        wordcloud = WordCloud(colormap="OrRd", stopwords=STOPWORDS, background_color='white', mask=mask).generate(data)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.margins(x=0, y=0)
        st.pyplot()

    def displayFamilyData(self):
        thankfulItems = self._getFamilyData()
        if thankfulItems != None:
            key = next(iter(thankfulItems))
            if len(thankfulItems[key]) > 0:
                self._displayWordCloud(thankfulItems[key], "mask1.png")
        else:
            st.write("Try adding some items in the sidebar for a fun surprise.")

    def displayAllFamiliesData(self):
        thankfulItems = self._getAllFamilyData()
        if thankfulItems != None:
            self._displayWordCloud(thankfulItems, "mask1.png")

    """User creation and authentication"""
    def _initializeFamilyInDatabase(self):
        root = self._getUserDbRoot()
        root.child("familyInfo").push(self.state.fName, self.state.user["idToken"])
        root = self._getUserDbRoot()
        root.child("thankfulList").push("", self.state.user["idToken"])

    def _createNewFamily(self, email: str, familyName: str):
        self.state.user = self.state.auth.create_user_with_email_and_password(email, familyName)
        # add them to the database
        self._initializeFamilyInDatabase()
        self.state.fName = familyName
        self.state.loggedIn = True

    def _signInFamily(self, email: str, familyName: str):
        self.state.user = self.state.auth.sign_in_with_email_and_password(email, familyName)
        self.state.fName = familyName
        self.state.loggedIn = True

    """saving user data/manipulating data"""
    def _preprocessUserInput(self, thankful: str):
        # remove possible unwanted input.
        thankful = thankful.lower()
        temp = re.sub('[^a-z,]+', "", thankful).split(",")
        while ("" in temp):
            temp.remove("")
        return " ".join(temp)

    def _getUserDbRoot(self):
        return self.state.db.child("users").child(f"{self.state.user['localId']}")

    def _updateUserThanfulList(self, thankful):
        # remove bad input and empty string list items.
        thankful = self._preprocessUserInput(thankful)

        root = self._getUserDbRoot()
        temp = root.child("thankfulList").get(self.state.user["idToken"]).val()
        if temp == None:
            root = self._getUserDbRoot()
            root.child("thankfulList").push(thankful, self.state.user["idToken"])
        else:
            key = next(iter(temp))
            root = self._getUserDbRoot()
            temp[key] = temp[key] + " " + thankful
            root.child("thankfulList").update({key: temp[key]}, self.state.user['idToken'])

    """Useful functions:"""
    def _getFamilyCount(self):
        familyList = self.state.db.child("users").get().val()
        if familyList == None:
            return 0
        return len(familyList.keys())

    def _getFamilyData(self):
        root = self._getUserDbRoot()
        data = root.child("thankfulList").get(self.state.user["idToken"]).val()
        return data

    def _getAllFamilyData(self):
        data = ""
        familyList = self.state.db.child("users").get().val()
        if familyList == None:
            return familyList
        else:
            for family in familyList:
                key = next(iter(familyList[family]["thankfulList"]))
                data += familyList[family]["thankfulList"][key]
            return data